from unittest import TestCase

from src.Planet import Planet
from src.vecN import Vec3


class PlanetTests(TestCase):
    """Test the Planet class for successful actions"""

    def test_create_planet_positive(self):
        """Test successfully creating a planet"""
        mass = 1e10
        pos = Vec3(1, 2, 3)
        vel = Vec3(3, 2, 1)
        color = 'white'

        p = Planet(mass, pos, vel, color)

        self.assertEqual(p.mass, mass)
        self.assertEqual(p.pos, pos)
        self.assertEqual(p.vel, vel)
        self.assertEqual(p.color, color)
        self.assertEqual(str(p), f'Planet at ({pos.x}, {pos.y}, {pos.z})')

    def test_create_planet_negative(self):
        """Test raising error when trying to create with invalid arguments"""
        with self.assertRaises(TypeError):
            Planet('1e4', Vec3(), Vec3())

        with self.assertRaises(TypeError):
            Planet(1e4, 1, Vec3())

        with self.assertRaises(TypeError):
            Planet(1e4, [1, 2, 3], Vec3())

        with self.assertRaises(TypeError):
            Planet(1e4, Vec3(), [1, 2, 3])

    def test_update_planet(self):
        """Test updating planet based on a gravitational field"""
        p = Planet(10, Vec3(), Vec3(5, 0, 0))
        field = Vec3(0, 4, 0)
        dt = 0.1

        p.update(field, dt)

        self.assertEqual(p.pos, Vec3(0.5, 0, 0))
        self.assertEqual(p.vel, Vec3(5, 0.4, 0))
