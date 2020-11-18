from .vecN import Vec3
from .Planet import Planet
from .utils import assertType


class Universe:
    """Represents the universe, its state and physics"""

    def __init__(self, dt, gravConst=6.67408e-11):
        assertType('time step', dt, [int, float])
        assertType('gravitational constant', gravConst, [int, float])

        self.dt = float(dt)
        self.gravConst = float(gravConst)
        self._planets = []

    @property
    def planets(self):
        return self._planets

    def setPlanets(self, planets):
        """Set the list of planets existing in the universe"""
        assertType('planets', planets, list)
        assertType('planets element', planets[0], Planet)
        self._planets = sorted(planets, key=lambda p: p.pos.z)

    def addPlanet(self, planet):
        """Add a planet to the universe"""
        assertType('planet', planet, Planet)
        self._planets.append(planet)
        self._planets = sorted(self._planets, key=lambda p: p.pos.z)

    def removePlanet(self, planet_idx):
        """Remove a planet from the universe"""
        if planet_idx >= len(self._planets):
            return

        self._planets = self._planets[:planet_idx] + \
            self._planets[planet_idx + 1:]

    def stepTime(self):
        """Steps the simlation one time step"""
        gravFields = [
            self._fieldOnPlanet(i, p) for i, p in enumerate(self._planets)
        ]

        for idx_planet, planet in enumerate(self._planets):
            planet.update(gravFields[idx_planet], self.dt)

    def _gravitationalField(self, m, r):
        """Newton's gravitational field equation"""
        return (self.gravConst * m / r.norm2()) * r.versor()

    def _fieldOnPlanet(self, idx_target, target_planet):
        """Calculates the grav. field acting on a planet by the others"""
        field = Vec3()

        for idx_planet, planet in enumerate(self._planets):
            if idx_planet == idx_target:
                continue

            field += self._gravitationalField(
                planet.mass,
                planet.pos - target_planet.pos
            )

        return field
