import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "astro_pulse.py"
spec = importlib.util.spec_from_file_location("astro_pulse", SCRIPT)
astro_pulse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(astro_pulse)


class AstroPulseHelperTests(unittest.TestCase):
    def test_house_number_parses_kerykeion_house_names_and_numbers(self):
        self.assertEqual(astro_pulse.house_number("First_House"), 1)
        self.assertEqual(astro_pulse.house_number("Tenth_House"), 10)
        self.assertEqual(astro_pulse.house_number("12"), 12)
        self.assertEqual(astro_pulse.house_number(7), 7)

    def test_normalized_house_shift_uses_shortest_twelve_house_distance(self):
        self.assertEqual(astro_pulse.normalized_house_shift("Twelfth_House", "Second_House"), 2)
        self.assertEqual(astro_pulse.normalized_house_shift("Second_House", "Twelfth_House"), -2)
        self.assertEqual(astro_pulse.normalized_house_shift("First_House", "Eighth_House"), -5)

    def test_angular_planets_detects_wraparound_angles(self):
        planets = {
            "Sun": {"abs_degree": 358.0},
            "Moon": {"abs_degree": 92.0},
            "Mars": {"abs_degree": 180.0},
        }
        angles = {"asc": {"abs_pos": 1.0}, "mc": {"abs_pos": 90.0}}
        self.assertEqual(astro_pulse.angular_planets(planets, angles, orb=5.0), ["Moon", "Sun"])


if __name__ == "__main__":
    unittest.main()
