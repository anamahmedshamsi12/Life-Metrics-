import unittest
import sys
import os

# Make sure Python can import from ../src just like the example test file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from typing import Dict, Any, List

import simulation  # type: ignore
import metrics    # type: ignore


class TestLifeMetrics(unittest.TestCase):
    """Unit tests for the core Life Metrics helper functions."""

    def __check_dict_keys(
        self,
        actual: Dict[str, Any],
        expected_keys: List[str],
    ) -> None:
        """Helper to check that a dictionary contains exactly the expected keys.

        Args:
            actual (Dict[str, Any]): The dictionary produced by the code.
            expected_keys (List[str]): The list of keys I expect to see.

        This ignores order but requires that there are no missing or extra keys.
        """
        self.assertEqual(
            set(expected_keys),
            set(actual.keys()),
            "Dictionary does not contain the expected keys.",
        )

    # ------------------------------------------------------------------
    # metrics.py helpers
    # ------------------------------------------------------------------

    def test_clamp_basic(self) -> None:
        """Tests clamp() keeps values inside [0, 100]."""
        self.assertEqual(simulation.clamp(-10), 0)
        self.assertEqual(simulation.clamp(50), 50)
        self.assertEqual(simulation.clamp(150), 100)

    def test_apply_deltas_and_clamp(self) -> None:
        """Tests apply_deltas() updates values and clamps them correctly."""
        start = {"Energy": 60, "Finances": 40}
        deltas = {
            "Energy": 50,      # should clamp to 100
            "Finances": -100,  # should clamp to 0
            "Unknown": 10,     # should be ignored
        }

        updated = metrics.apply_deltas(start, deltas)

        self.assertEqual(updated["Energy"], 100)
        self.assertEqual(updated["Finances"], 0)
        self.assertNotIn("Unknown", updated)

    def test_average_score_normal_and_empty(self) -> None:
        """Tests average_score() for a normal dict and for empty metrics."""
        data = {"A": 80, "B": 60, "C": 70}  # average = 70.0
        self.assertEqual(metrics.average_score(data), 70.0)

        empty: Dict[str, int] = {}
        self.assertEqual(metrics.average_score(empty), 0.0)

    def test_init_metrics_custom_and_blank(self) -> None:
        """Tests init_metrics() behavior for custom mode."""
        names = ["Energy", "Focus", "Connection"]
        custom = metrics.init_metrics("custom", names)

        # All provided names should be present and start at 60
        for name in names:
            self.assertIn(name, custom)
            self.assertEqual(custom[name], 60)

        # If only blanks are provided, we still get at least one metric
        custom_blank = metrics.init_metrics("custom", ["   ", ""])
        self.assertGreaterEqual(len(custom_blank), 1)

    # ------------------------------------------------------------------
    # simulation.py helpers
    # ------------------------------------------------------------------

    def test_compute_score_matches_average(self) -> None:
        """Tests compute_score() matches the rounded average and empty case."""
        metrics_dict = {"X": 71, "Y": 69}  # average = 70.0 -> round to 70
        self.assertEqual(simulation.compute_score(metrics_dict), 70)

        empty: Dict[str, int] = {}
        self.assertEqual(simulation.compute_score(empty), 0)

    def test_apply_scaled_deltas_basic(self) -> None:
        """Tests apply_scaled_deltas() applies scaled changes correctly."""
        m = {"Academics": 60, "Sleep": 60}
        deltas = {"Academics": 6, "Sleep": -1}

        # factor 0.5: +6 -> +3, -1 would be 0 but should still move by -1
        simulation.apply_scaled_deltas(m, deltas, factor=0.5)

        self.assertEqual(m["Academics"], 63)
        self.assertEqual(m["Sleep"], 59)

    def test_apply_custom_effect_patterns(self) -> None:
        """Tests apply_custom_effect() for strong, tough, and steady days."""
        base = {"M1": 70, "M2": 70}

        # strong_day: all metrics should increase
        metrics_strong = dict(base)
        simulation.apply_custom_effect(metrics_strong, "strong_day")
        self.assertGreater(metrics_strong["M1"], base["M1"])
        self.assertGreater(metrics_strong["M2"], base["M2"])

        # tough_day: all metrics should decrease
        metrics_tough = dict(base)
        simulation.apply_custom_effect(metrics_tough, "tough_day")
        self.assertLess(metrics_tough["M1"], base["M1"])
        self.assertLess(metrics_tough["M2"], base["M2"])

        # steady_day: mix of up and down
        metrics_steady = dict(base)
        simulation.apply_custom_effect(metrics_steady, "steady_day")
        values = list(metrics_steady.values())
        self.assertTrue(any(v > 70 for v in values))
        self.assertTrue(any(v < 70 for v in values))

    def test_start_profile_returns_copy(self) -> None:
        """Tests start_profile() returns a copy of metrics, not the original."""
        mode, metrics_dict, actions = simulation.start_profile("student")

        # Mode and actions should match PROFILES
        self.assertEqual(mode, simulation.PROFILES["student"]["mode"])
        self.assertEqual(actions, simulation.PROFILES["student"]["actions"])

        # Values should match initially
        self.assertEqual(
            metrics_dict,
            simulation.PROFILES["student"]["metrics"],
        )

        # Mutating the returned dict must NOT affect PROFILES
        metrics_dict["Academics"] = 999
        self.assertNotEqual(
            simulation.PROFILES["student"]["metrics"]["Academics"],
            999,
        )

    def test_build_custom_profile_filters_blanks(self) -> None:
        """Tests build_custom_profile() filters blank metric names properly."""
        raw_names = [" Energy ", "", "Focus", "   "]

        (
            mode,
            clean_names,
            metrics_dict,
            actions,
        ) = simulation.build_custom_profile(
            raw_names,
            strong_label="Strong",
            strong_desc="Strong day.",
            steady_label="Steady",
            steady_desc="Steady day.",
            tough_label="Tough",
            tough_desc="Tough day.",
        )

        self.assertEqual(mode, "custom")
        self.assertEqual(clean_names, ["Energy", "Focus"])
        self.__check_dict_keys(metrics_dict, clean_names)

        # All starting values should be 70
        for value in metrics_dict.values():
            self.assertEqual(value, 70)

        # Exactly three actions (strong / steady / tough)
        self.assertEqual(len(actions), 3)

    def test_log_check_in_non_custom_advances_time(self) -> None:
        """Tests log_check_in() for a non-custom mode.

        I check that metrics change, a log entry is added,
        and the time slot advances correctly.
        """
        mode = "student"
        metrics_dict = {"Academics": 70}
        actions = [
            {
                "id": "test_action",
                "label": "Test action",
                "deltas": {"Academics": 4},
            }
        ]
        day = 1
        moment_index = 0  # Morning
        note = "Testing one check-in."
        log_entries: List[Dict[str, Any]] = []

        new_metrics, new_log, new_day, new_moment_index = simulation.log_check_in(
            mode=mode,
            metrics=metrics_dict,
            actions=actions,
            day=day,
            moment_index=moment_index,
            action_id="test_action",
            note=note,
            log_entries=log_entries,
            scale_factor=0.5,
        )

        # Metrics should increase
        self.assertGreater(new_metrics["Academics"], 70)

        # One log entry should be added
        self.assertEqual(len(new_log), 1)
        entry = new_log[0]
        self.assertEqual(entry["day"], 1)
        self.assertEqual(entry["time_label"], simulation.TIME_SLOTS[moment_index])
        self.assertEqual(entry["note"], note)

        # Time moves from Morning (0) to the next slot
        self.assertEqual(new_day, 1)
        self.assertEqual(new_moment_index, 1)

    def test_recursive_metric_trend_basic(self) -> None:
        """Tests recursive_metric_trend() on a small synthetic log."""
        log_entries: List[Dict[str, Any]] = [
            {"snapshot": {"Energy": 60}},
            {"snapshot": {"Energy": 65}},
            {"snapshot": {"Energy": 55}},
        ]

        net_change = simulation.recursive_metric_trend(log_entries, "Energy")
        self.assertEqual(net_change, -5)


if __name__ == "__main__":
    unittest.main()
