import unittest

from simple_permutation_parity import permutation_parity, parity_from_cycles


class TestPermutationParity(unittest.TestCase):
    def test_identity_is_even(self):
        self.assertEqual(permutation_parity([0, 1, 2, 3]), 1)

    def test_empty_is_even(self):
        self.assertEqual(permutation_parity([]), 1)

    def test_single_transposition_is_odd(self):
        # swap 0 and 1
        self.assertEqual(permutation_parity([1, 0, 2]), -1)

    def test_three_cycle_is_even(self):
        # (0 1 2) -> [1, 2, 0]; a 3-cycle is 2 transpositions -> even
        self.assertEqual(permutation_parity([1, 2, 0]), 1)

    def test_two_disjoint_transpositions_is_even(self):
        # (0 1)(2 3)
        self.assertEqual(permutation_parity([1, 0, 3, 2]), 1)

    def test_long_cycle_of_even_length_is_odd(self):
        # 4-cycle = 3 transpositions -> odd
        self.assertEqual(permutation_parity([1, 2, 3, 0]), -1)

    def test_long_cycle_of_odd_length_is_even(self):
        # 5-cycle = 4 transpositions -> even
        self.assertEqual(permutation_parity([1, 2, 3, 4, 0]), 1)

    def test_returns_int_type(self):
        result = permutation_parity([0, 1])
        self.assertIsInstance(result, int)

    def test_invalid_value_out_of_range(self):
        with self.assertRaises(ValueError):
            permutation_parity([0, 5])

    def test_duplicate_value(self):
        with self.assertRaises(ValueError):
            permutation_parity([0, 0, 1])

    def test_non_int_entry(self):
        with self.assertRaises(ValueError):
            permutation_parity([0, 1, 2.0])

    def test_bool_entry_rejected(self):
        # bool is a subclass of int but is not a valid permutation entry.
        with self.assertRaises(ValueError):
            permutation_parity([0, True])


class TestParityFromCycles(unittest.TestCase):
    def test_all_fixed_points_is_even(self):
        self.assertEqual(parity_from_cycles([1, 1, 1, 1]), 1)

    def test_empty_is_even(self):
        self.assertEqual(parity_from_cycles([]), 1)

    def test_single_two_cycle_is_odd(self):
        self.assertEqual(parity_from_cycles([2, 1, 1]), -1)

    def test_two_two_cycles_is_even(self):
        self.assertEqual(parity_from_cycles([2, 2]), 1)

    def test_three_cycle_is_even(self):
        self.assertEqual(parity_from_cycles([3, 1]), 1)

    def test_four_cycle_is_odd(self):
        self.assertEqual(parity_from_cycles([4]), -1)

    def test_negative_length_rejected(self):
        with self.assertRaises(ValueError):
            parity_from_cycles([-1, 2])

    def test_non_int_length_rejected(self):
        with self.assertRaises(ValueError):
            parity_from_cycles([2, 3.0])

    def test_bool_length_rejected(self):
        with self.assertRaises(ValueError):
            parity_from_cycles([True, 2])


if __name__ == "__main__":
    unittest.main()
