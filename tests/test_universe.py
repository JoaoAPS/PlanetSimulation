from unittest import TestCase

from src.Planet import Planet
from src.Universe import Universe
from src.vecN import Vec3


class UniverseTest(TestCase):
    """Test the Universe class"""

    # Test create

    def test_fieldOnPlanet(self):
        """Test the _fieldOnPlanet method"""
        planets = [
            Planet(10, Vec3(0, 4, 0), Vec3()),
            Planet(10, Vec3(3), Vec3()),
            Planet(10, Vec3(-3), Vec3())
        ]
        u = Universe(planets, 1)

        correct = 2 * u.gravConst * 10 * 4 / 5**3 * Vec3(0, -1, 0)
        result = u._fieldOnPlanet(0, planets[0])

        self.assertEqual(round(result.x, 5), round(correct.x, 5))
        self.assertEqual(round(result.y, 5), round(correct.y, 5))
        self.assertEqual(round(result.z, 5), round(correct.z, 5))
