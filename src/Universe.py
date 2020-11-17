from .vecN import Vec3
from .Planet import Planet
from .utils import assertType


class Universe:
    """Represents the universe, its state and physics"""

    def __init__(self, planets, dt, gravConst=6.67408e-11):
        assertType('planets', planets, list)
        assertType('planets element', planets[0], Planet)
        assertType('time step', dt, [int, float])
        assertType('gravitational constant', gravConst, float)

        self.planets = planets
        self.dt = float(dt)
        self.gravConst = gravConst

    def stepTime(self):
        """Steps the simlation one time step"""
        gravFields = [
            self._fieldOnPlanet(i, p) for i, p in enumerate(self.planets)
        ]

        for idx_planet, planet in enumerate(self.planets):
            planet.update(gravFields[idx_planet], self.dt)

    def _gravitationalField(self, m, r):
        """Newton's gravitational field equation"""
        return (self.gravConst * m / r.norm2()) * r.versor()

    def _fieldOnPlanet(self, idx_target, target_planet):
        """Calculates the grav. field acting on a planet by the others"""
        field = Vec3()

        for idx_planet, planet in enumerate(self.planets):
            if idx_planet == idx_target:
                continue

            field += self._gravitationalField(
                planet.mass,
                planet.pos - target_planet.pos
            )

        return field
