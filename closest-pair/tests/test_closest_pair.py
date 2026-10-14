import random
import unittest
from brute_force import closest_pair as brute
from divide_conquer import closest_pair as divide


class ClosestPairTests(unittest.TestCase):
    def check(self, points):
        a, b = brute(points), divide(points)
        self.assertAlmostEqual(a.distance, b.distance, places=12)
        self.assertAlmostEqual(a.distance, ((a.pair[0][0]-a.pair[1][0])**2 + (a.pair[0][1]-a.pair[1][1])**2)**0.5)
        self.assertAlmostEqual(b.distance, ((b.pair[0][0]-b.pair[1][0])**2 + (b.pair[0][1]-b.pair[1][1])**2)**0.5)

    def test_n_two(self): self.check([(0, 0), (3, 4)])
    def test_too_few_rejected(self):
        for points in ([], [(1, 2)]):
            with self.assertRaises(ValueError): brute(points)
            with self.assertRaises(ValueError): divide(points)
    def test_duplicates_zero(self):
        self.check([(1, 2), (5, 5), (1, 2), (8, 9)])
        self.assertEqual(divide([(1, 2), (1, 2)]).distance, 0)
    def test_collinear(self): self.check([(-5, -5), (0, 0), (1, 1), (8, 8)])
    def test_equal_x(self): self.check([(2, y) for y in (9, 4, 1, -3, 7, 5)])
    def test_equal_y(self): self.check([(x, 2) for x in (9, 4, 1, -3, 7, 5)])
    def test_equal_minima(self): self.check([(0, 0), (1, 0), (5, 5), (6, 5)])
    def test_negative_float_close(self): self.check([(-1.0, -1.0), (-1.000001, -1.0), (9.2, 7.3)])
    def test_uneven(self): self.check([(0, 0), (0.01, 0), (1000, 900), (-500, 700), (2000, -300)])
    def test_random_small_sets(self):
        rng=random.Random(42)
        for n in range(2, 45):
            self.check([(rng.uniform(-20,20), rng.uniform(-20,20)) for _ in range(n)])


if __name__ == "__main__": unittest.main()
