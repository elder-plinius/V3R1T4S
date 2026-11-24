#!/usr/bin/env python3
"""Fast regression tests for verification admission; no network or large search."""
from pathlib import Path
from contextlib import redirect_stdout
import io
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import check

GOOD = ('END nodes=43196762 hits=0 capped=0 elapsed=31 '
        'targets=25 matches=5519232 completed=25')


class VerificationAdmission(unittest.TestCase):
    def test_complete_summary(self):
        self.assertEqual(check.parse_summary(GOOD)['completed'], 25)

    def test_nonzero_hits_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD.replace('hits=0', 'hits=1'))

    def test_timeout_cap_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD.replace('capped=0', 'capped=1'))

    def test_partial_run_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD.replace('completed=25', 'completed=1'))

    def test_missing_completion_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD.replace(' completed=25', ''))

    def test_substring_spoof_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD.replace('hits=0', 'fakehits=0 hits=10'))

    def test_duplicate_field_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD + ' hits=0')

    def test_wrong_search_counts_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD.replace('nodes=43196762', 'nodes=0'))

    def test_trailing_text_rejected(self):
        with self.assertRaises(ValueError):
            check.parse_summary(GOOD + '\ncrashed')

    def test_exit_failure_even_with_good_summary(self):
        with patch('check.subprocess.run', return_value=subprocess.CompletedProcess([], 1, GOOD)):
            with self.assertRaises(ValueError):
                check.execute(['unused'], 1)

    def test_timeout_propagates(self):
        with patch('check.subprocess.run', side_effect=subprocess.TimeoutExpired('unused', 1)):
            with self.assertRaises(subprocess.TimeoutExpired):
                check.execute(['unused'], 1)

    def test_real_object_matches_enumeration(self):
        text = (check.ROOT / 'object/contractions.txt').read_text()
        self.assertEqual(check.parse_rows(text), check.contractions())

    def test_corrupt_object_rejected(self):
        text = (check.ROOT / 'object/contractions.txt').read_text()
        lines = text.splitlines()
        lines[0] = '0 ' + ' '.join(lines[0].split()[1:])
        with self.assertRaises(ValueError):
            check.parse_rows('\n'.join(lines))

    def test_duplicate_contraction_rejected(self):
        lines = (check.ROOT / 'object/contractions.txt').read_text().splitlines()
        lines[-1] = lines[0]
        with self.assertRaises(ValueError):
            check.parse_rows('\n'.join(lines))


    def orchestration(self, changes=None):
        # Mocked outputs exercise admission, not mathematical evidence.
        stages = ['', (check.ROOT / 'object/contractions.txt').read_text(),
                  'SELFTEST PASS\n', GOOD + '\n',
                  'INDEPENDENT PASS: positive control, negative control, target\n']
        for index, value in (changes or {}).items():
            stages[index] = value
        out = io.StringIO()
        with patch('check.execute', side_effect=stages), redirect_stdout(out):
            status = check.cli()
        return status, out.getvalue().strip().splitlines()[-1]

    def test_orchestration_success_marker(self):
        self.assertEqual(self.orchestration(), (0, 'PASS'))

    def test_each_orchestration_stage_failure(self):
        for stage in range(5):
            with self.subTest(stage=stage):
                self.assertEqual(self.orchestration({stage: ValueError('injected failure')}),
                                 (1, 'FAIL'))

    def test_orchestration_timeout_and_bad_completion(self):
        mutations = [(3, subprocess.TimeoutExpired('search', 1)),
                     (3, GOOD.replace('capped=0', 'capped=1')),
                     (3, GOOD.replace('completed=25', 'completed=1')),
                     (4, 'incomplete independent output\n'),
                     (1, '0 0 0\n')]
        for stage, result in mutations:
            with self.subTest(stage=stage, result=str(result)):
                self.assertEqual(self.orchestration({stage: result}), (1, 'FAIL'))

    def test_shell_failure_and_success_propagation(self):
        # Exercise the shipped shell in fixtures, never rewrite this package.
        with tempfile.TemporaryDirectory(prefix='cw208-shell-test-') as tmp:
            root = Path(tmp)
            vd = root / 'verify-it-yourself'
            vd.mkdir()
            shutil.copy2(check.ROOT / 'verify-it-yourself/run_checks.sh', vd / 'run_checks.sh')
            for test_rc, check_rc, expected in ((1, 0, 1), (0, 1, 1), (0, 0, 0)):
                with self.subTest(test_rc=test_rc, check_rc=check_rc):
                    (vd / 'test_verifier.py').write_text(f'raise SystemExit({test_rc})\n')
                    marker = 'PASS' if check_rc == 0 else 'FAIL'
                    (vd / 'check.py').write_text(f'print({marker!r})\nraise SystemExit({check_rc})\n')
                    result = subprocess.run(['sh', str(vd / 'run_checks.sh')], cwd=root,
                                            text=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT, timeout=10)
                    self.assertEqual(result.returncode, expected)
                    self.assertEqual(result.stdout.strip().splitlines()[-1],
                                     'PASS' if expected == 0 else 'FAIL')


if __name__ == '__main__':
    unittest.main(verbosity=2)
