# SPDX-License-Identifier: AGPL-3.0-or-later
"""Custom bank paths are whole settings values, including spaces."""
import json
import os
import unittest

from test_check_run import Base, check_run, w


CUSTOM_BANK = {"targets": [
    {"id": "custom-record", "category": "record-tables", "disclosure": "open"},
]}


class BankPaths(Base):
    def custom_bank(self, value, text=None):
        path = value if os.path.isabs(value) else os.path.join(self.W, value)
        w(path, json.dumps(CUSTOM_BANK) if text is None else text)
        settings = os.path.join(self.W, "settings.md")
        w(settings, check_run.read(settings) + "bank: `%s`\n" % value)
        return path

    def assert_custom_bank(self, path):
        settings = check_run.kv(check_run.read(os.path.join(self.W, "settings.md")))
        errors = []
        bank, directory = check_run.load_bank(self.W, settings, errors)
        self.assertEqual(bank, {t["id"]: t for t in CUSTOM_BANK["targets"]})
        self.assertEqual(directory, os.path.dirname(os.path.abspath(path)))
        self.assertEqual(errors, [])

    def test_relative_path_with_spaces(self):
        path = self.custom_bank(os.path.join("custom bank", "target list.json"))
        self.assert_custom_bank(path)

    def test_absolute_path_with_spaces(self):
        path = self.custom_bank(os.path.join(self.W, "custom bank", "targets.json"))
        self.assert_custom_bank(path)

    def test_full_path_takes_precedence_over_first_word(self):
        w(os.path.join(self.W, "custom"), json.dumps({"targets": [{"id": "wrong-bank"}]}))
        path = self.custom_bank(os.path.join("custom bank", "targets.json"))
        self.assert_custom_bank(path)

    def test_workspace_uses_configured_bank(self):
        self.custom_bank(os.path.join("custom bank", "targets.json"))
        self.attack()
        w(os.path.join(self.R, "target.md"), "id: custom-record\n")
        self.assertPass(self.W, "--no-exec")

    def test_workspace_reports_malformed_bank_with_spaces(self):
        self.custom_bank(os.path.join("custom bank", "targets.json"), text='{"targets": [')
        self.attack()
        self.assertFail("could not read the bank", self.W, "--no-exec")

    def test_package_reports_malformed_bank_with_spaces(self):
        self.custom_bank(os.path.join(self.W, "custom bank", "targets.json"), text='{"targets": [')
        package = self.package()
        self.assertFail("could not read the bank", "--package", package,
                        "--workdir", self.W, "--no-exec")


if __name__ == "__main__":
    unittest.main(verbosity=2)
