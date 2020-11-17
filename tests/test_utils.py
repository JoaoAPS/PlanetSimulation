from unittest import TestCase

from src.utils import assertType


class AuxClass():
    """Auxiliary class for testing"""

    def __init__(self):
        self.x = 0


class AuxClass2():
    """Auxiliary class for testing"""

    def __init__(self):
        self.x = 1


class CheckTypeTests(TestCase):
    """Test the function assertType"""

    def test_single_type_positive(self):
        """Test assertType when passing a single correct type"""
        assertType('', 1, int)
        assertType('', 1.4, float)
        assertType('', 'asd', str)
        assertType('', [1.4], list)
        assertType('', (1, 2), tuple)
        assertType('', AuxClass(), AuxClass)

    def test_multiple_types_positive(self):
        """Test assertType when passing a list containing the correct type"""
        assertType('', 1, [bool, int])
        assertType('', 1.4, [float])
        assertType('', 'asd', [str, float])
        assertType('', [1.4], (list, int))
        assertType('', (1, 2), (tuple,))
        assertType('', AuxClass(), [AuxClass])

    def test_single_type_negative(self):
        """Test assertType when passing a single incorrect type"""
        payloads = [
            ['one', 1, float],
            ['1.5', 1.5, str],
            ['lala', 'lala', float],
            ['list', [1], int],
            ['tuple', (1.1, 44.), float],
            ['Aux1', AuxClass(), AuxClass2]
        ]

        for payload in payloads:
            with self.assertRaises(TypeError):
                assertType(*payload)

    def test_multiple_types_negative(self):
        """Test assertType passing a list not containing the correct type"""
        payloads = [
            ['one', 1, [float]],
            ['1.5', 1.5, (str, int)],
            ['lala', 'lala', (bool, float)],
            ['list', [1], [int]],
            ['tuple', (1.1, 44.), [float]],
            ['Aux1', AuxClass(), (AuxClass2,)]
        ]

        for payload in payloads:
            with self.assertRaises(TypeError):
                assertType(*payload)
