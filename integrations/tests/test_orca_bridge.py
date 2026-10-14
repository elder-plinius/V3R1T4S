"""Standard-library tests of the GPT-Orca-V3R1T4S boundary."""
import importlib.util
from pathlib import Path
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "orca_bridge.py"
spec = importlib.util.spec_from_file_location("v3_orca_bridge", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BridgeTests(unittest.TestCase):
    def test_packet_is_read_only_and_unverified(self):
        result = module.packet("research-1", "Investigate a possible upper bound")
        self.assertEqual(result["status"], "PLANNING_ONLY_NOT_VERIFIED")
        self.assertEqual(result["roles"], ["planner", "researcher", "critic", "synthesizer"])
        self.assertIn("kit/RULES.md", result["source_refs"])
        self.assertTrue(any("three-skeptic" in x for x in result["constraints"]))

    def test_refuses_empty_inputs(self):
        with self.assertRaises(ValueError):
            module.packet("", "question")
        with self.assertRaises(ValueError):
            module.packet("id", " ")

    def test_refuses_oversized_request(self):
        with self.assertRaises(ValueError):
            module.packet("x" * 201, "question")


if __name__ == "__main__":
    unittest.main()
