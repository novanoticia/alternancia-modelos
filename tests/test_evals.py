import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from compare_evals import compare


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "evals/examples/synthetic-pair.json").read_text())
        self.native = self.data["runs"]["native"]
        self.plugin = self.data["runs"]["plugin"]

    def test_quality_gain_is_scoped_and_marked_synthetic(self):
        result = compare(self.data)
        self.assertEqual(result["status"], "observed_benefit")
        self.assertEqual(result["source"], "synthetic")
        self.assertEqual(result["scope"], "single_pair")

    def test_same_quality_with_less_resources(self):
        self.plugin.update(quality=80, tokens=900, wall_seconds=90)
        self.assertEqual(compare(self.data)["status"], "observed_benefit")

    def test_equal_runs_are_not_a_benefit(self):
        self.data["runs"]["plugin"] = copy.deepcopy(self.native)
        self.assertEqual(compare(self.data)["status"], "no_clear_benefit")

    def test_cost_savings_do_not_compensate_for_quality_regression(self):
        self.plugin.update(quality=50, tokens=10, wall_seconds=10)
        self.assertEqual(compare(self.data)["status"], "regression")

    def test_failed_requirement_wins_over_high_score(self):
        self.plugin.update(quality=100, requirements_met=False)
        self.assertEqual(compare(self.data)["status"], "regression")

    def test_missing_measurement_is_not_zero(self):
        for condition in ("native", "plugin"):
            for field in ("quality", "wall_seconds", "tokens"):
                with self.subTest(condition=condition, field=field):
                    data = copy.deepcopy(self.data)
                    data["runs"][condition][field] = None
                    self.assertEqual(compare(data)["status"], "inconclusive")

    def test_setup_mismatch_prevents_comparison(self):
        for key in ("host", "primary_model", "context_id", "rubric_id", "budget_id", "effort"):
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                data["runs"]["plugin"]["setup"][key] = "different"
                self.assertEqual(compare(data)["status"], "inconclusive")

    def test_native_delegation_must_remain_available(self):
        self.native["setup"]["native_delegation_allowed"] = False
        with self.assertRaises(ValueError):
            compare(self.data)

    def test_absolute_limits_cannot_be_bought_with_quality(self):
        for field in ("tokens", "wall_seconds"):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data["runs"]["plugin"][field] = 99999
                self.assertEqual(compare(data)["status"], "regression")

    def test_relative_budget_excess_is_not_benefit(self):
        self.plugin["tokens"] = 1400
        self.assertEqual(compare(self.data)["status"], "no_clear_benefit")

    def test_cost_requires_comparable_currencies(self):
        self.data["policy"].update(resource_metric="cost", resource_limit=2, currency="USD")
        self.native.update(cost=1, currency="EUR")
        self.plugin.update(cost=1.1, currency="USD")
        self.assertEqual(compare(self.data)["status"], "inconclusive")

    def test_invalid_numbers_and_booleans_are_not_scores(self):
        for value in (True, -1, float("nan"), float("inf"), 101, "80", 10 ** 400):
            with self.subTest(value=value):
                self.plugin["quality"] = value
                with self.assertRaises(ValueError):
                    compare(self.data)

    def test_zero_baseline_does_not_divide_by_zero(self):
        self.native.update(tokens=0, wall_seconds=0)
        self.assertEqual(compare(self.data)["status"], "no_clear_benefit")

    def test_same_currency_cost_comparison(self):
        self.data["policy"].update(resource_metric="cost", resource_limit=2, currency="EUR")
        self.native.update(cost=1, currency="EUR")
        self.plugin.update(cost=1.1, currency="EUR")
        self.assertEqual(compare(self.data)["status"], "observed_benefit")

    def test_budget_in_different_currency_is_not_applied(self):
        self.data["policy"].update(resource_metric="cost", resource_limit=2, currency="EUR")
        self.native.update(cost=100, currency="USD")
        self.plugin.update(cost=110, currency="USD")
        self.assertEqual(compare(self.data)["status"], "inconclusive")

    def test_incomplete_run_is_inconclusive(self):
        self.plugin["completed"] = False
        self.assertEqual(compare(self.data)["status"], "inconclusive")

    def test_cli_rejects_duplicate_keys_and_missing_fields(self):
        for content in ('{"schema_version":1,"schema_version":1}', '{}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "record.json"
                path.write_text(content)
                process = subprocess.run([sys.executable, str(ROOT / "scripts/compare_evals.py"), str(path)],
                                         capture_output=True, text=True)
                self.assertEqual(process.returncode, 2)
                self.assertNotIn("Traceback", process.stderr)


if __name__ == "__main__":
    unittest.main()
