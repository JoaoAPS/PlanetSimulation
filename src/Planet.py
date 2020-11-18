from .vecN import Vec3
from .utils import assertType


class Planet:
    """Represents a planet"""

    def __init__(self, mass, pos, vel, color=(0, 0, 0)):
        assertType('mass', mass, [float, int])
        assertType('position', pos, Vec3)
        assertType('velocity', vel, Vec3)

        self.mass = float(mass)
        self.pos = pos
        self.vel = vel
        self.trajectory = []
        self.color = color

    def __str__(self):
        return f'Planet at ({self.pos.x}, {self.pos.y}, {self.pos.z})'

    __repr__ = __str__

    def update(self, field, dt):
        """Update properties one time step following gravitational field"""
        self.trajectory.append(self.pos)
        self.pos += self.vel * dt
        self.vel += field * dt
