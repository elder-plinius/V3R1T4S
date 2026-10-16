import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from check_inference_manifest import validate


class InferenceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = json.loads((Path(__file__).parents[1] / "INFERENCE_EXPERIMENT.json").read_text())
        cls.template["workload"]["request_set_sha256"] = "sha256:" + "a" * 64
        cls.template["measurements"]["raw_results_sha256"] = "sha256:" + "b" * 64

    def test_template_with_realistic_hash_placeholders_passes_bookkeeping(self):
        self.assertEqual([], validate(copy.deepcopy(self.template)))

    def test_bad_hash_and_unmatched_measurement_requirements_fail(self):
        manifest = copy.deepcopy(self.template)
        manifest["workload"]["request_set_sha256"] = "not-a-hash"
        manifest["measurements"]["record_per_request"] = False
        errors = validate(manifest)
        self.assertTrue(any("request_set_sha256" in e for e in errors))
        self.assertTrue(any("record_per_request" in e for e in errors))

    def test_nonpositive_workload_is_rejected(self):
        manifest = copy.deepcopy(self.template)
        manifest["workload"]["concurrency"] = 0
        self.assertIn("workload.concurrency must be a positive integer", validate(manifest))


if __name__ == "__main__":
    unittest.main()
