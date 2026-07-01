import math
import unittest

import pkmodel


class TestOneCompartment(unittest.TestCase):
    def test_ke_half_life_roundtrip(self):
        ke = pkmodel.ke_from_half_life(6.0)
        self.assertAlmostEqual(pkmodel.half_life(ke), 6.0)

    def test_initial_concentration(self):
        # At t=0 concentration is just dose/Vd.
        self.assertAlmostEqual(pkmodel.concentration(1000, 100, 0.1, 0), 10.0)

    def test_halving_at_one_half_life(self):
        ke = pkmodel.ke_from_half_life(5.0)
        c0 = pkmodel.concentration(1000, 100, ke, 0)
        self.assertAlmostEqual(pkmodel.concentration(1000, 100, ke, 5.0), c0 / 2)

    def test_clearance(self):
        self.assertAlmostEqual(pkmodel.clearance(0.1, 10), 1.0)

    def test_loading_dose(self):
        self.assertAlmostEqual(pkmodel.loading_dose(2.0, 200, 1.0), 400.0)
        # Lower bioavailability needs a proportionally larger dose.
        self.assertAlmostEqual(pkmodel.loading_dose(2.0, 200, 0.5), 800.0)


class TestSteadyState(unittest.TestCase):
    def test_peak_matches_c0_times_accumulation(self):
        c0 = 100 / 10
        ar = pkmodel.accumulation_ratio(0.1, 6.0)
        self.assertAlmostEqual(
            pkmodel.steady_state_peak(100, 10, 0.1, 6.0), c0 * ar
        )

    def test_accumulation_ratio_value(self):
        expected = 1.0 / (1 - math.exp(-0.1 * 6.0))
        self.assertAlmostEqual(pkmodel.accumulation_ratio(0.1, 6.0), expected)


class TestTwoCompartment(unittest.TestCase):
    def test_sum_at_zero(self):
        # At t=0 both exponentials are 1, so C = dose*(A+B).
        self.assertAlmostEqual(
            pkmodel.two_compartment(100, 0.6, 0.5, 0.4, 0.05, 0), 100.0
        )

    def test_decays(self):
        c0 = pkmodel.two_compartment(100, 0.6, 0.5, 0.4, 0.05, 0)
        later = pkmodel.two_compartment(100, 0.6, 0.5, 0.4, 0.05, 4.0)
        self.assertLess(later, c0)


class TestInputGuards(unittest.TestCase):
    def test_nonpositive_inputs_raise(self):
        with self.assertRaises(ValueError):
            pkmodel.ke_from_half_life(0)
        with self.assertRaises(ValueError):
            pkmodel.half_life(-1)
        with self.assertRaises(ValueError):
            pkmodel.concentration(100, 0, 0.1, 1)
        with self.assertRaises(ValueError):
            pkmodel.steady_state_peak(100, 10, 0.1, 0)
        with self.assertRaises(ValueError):
            pkmodel.accumulation_ratio(0.1, 0)


if __name__ == "__main__":
    unittest.main()
