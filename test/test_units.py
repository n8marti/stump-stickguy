import unittest

import guesser
from app import AppBoxLayout

class TestUserInput(unittest.TestCase):

    #@unittest.skip('skipping')
    def test_input(self):
        inputs = {
            'ten': False,
            '1000': True,
            '1,000': True,
            '1.000': True,
        }
        for k, v in inputs.items():
            with self.subTest(k=k, v=v):
                result = AppBoxLayout.verify_user_max(None, k)
                if result:
                    self.assertTrue(v)
                else:
                    self.assertEqual(v, result)

class TestGuesser(unittest.TestCase):

    def test_guess_range(self):
        limits = [
            (1, 2),
            (1, 10),
            (2, 3),
            (900, 1000),
        ]
        for pair in limits:
            extremes = guesser.set_guess_range(pair[0], pair[1])
            with self.subTest(pair=pair):
                self.assertTrue(extremes[0] >= pair[0])
                self.assertTrue(extremes[1] <= pair [1])

    def test_confidence(self):
        trials = [
            (1, 1),
            (1, 2),
            (10, 1),
            (8, 4),
        ]
        for t in trials:
            c = guesser.get_confidence(t[0], t[1])
            with self.subTest(t=t, c=c):
                self.assertTrue(0 <= c <= 100)


if __name__ == '__main__':
    unittest.main()
