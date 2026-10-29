# SPDX-License-Identifier: AGPL-3.0-or-later
"""Package manifest identity tests; all package checks use --no-exec."""
import hashlib
import importlib.util
import os
from pathlib import Path
import unittest
from unittest import mock
import test_check_run as fixtures

if os.environ.get('CHECK_RUN_UNDER_TEST'):
    spec = importlib.util.spec_from_file_location('manifest_checker', os.environ['CHECK_RUN_UNDER_TEST'])
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    fixtures.check_run = checker


def record(digest, name, binary=False):
    escaped = any(c in name for c in '\\\n\r')
    if escaped:
        name = name.replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r')
    return ('\\' if escaped else '') + digest + (' *' if binary else '  ') + name


class PackageManifest(fixtures.Base):
    def setUp(self):
        super().setUp()
        self.P = self.package()
        self.manifest = Path(self.P) / 'SHA256SUMS'
        self.original = self.manifest.read_text()
        self.readme = next(line for line in self.original.splitlines() if line.endswith('  README.md'))

    def verify(self, text, failure=None):
        self.manifest.write_bytes(text.encode('utf-8'))  # exact bytes, also on Windows
        if failure is None:
            self.assertPass('--package', self.P, '--no-exec')
        else:
            self.assertFail(failure, '--package', self.P, '--no-exec')

    def test_conflicting_duplicates_rejected_in_both_orders(self):
        bad = '0' * 64 + '  README.md\n'
        for value in (bad + self.original, self.original + bad):
            with self.subTest(value=value[:80]):
                self.verify(value, 'duplicate SHA256SUMS path')

    def test_same_digest_and_normalized_alias_duplicates_rejected(self):
        for name in ('README.md', './README.md', '././README.md', 'object/../README.md'):
            with self.subTest(name=name):
                self.verify(self.original + record(self.readme[:64], name) + '\n', 'duplicate SHA256SUMS path')

    def test_manifest_self_entries_rejected(self):
        for name in ('SHA256SUMS', './SHA256SUMS', 'object/../SHA256SUMS'):
            self.verify(self.original + record('0' * 64, name) + '\n', 'must not list itself')

    def test_malformed_nonblank_records_rejected(self):
        for line in ('not a checksum', '0' * 63 + '  README.md', 'z' * 64 + '  README.md',
                     '0' * 64 + '  ', '0' * 64 + ' ?README.md', '   ', '\t'):
            with self.subTest(line=line):
                self.verify(self.original + line + '\n', 'malformed SHA256SUMS record')

    def test_invalid_escaped_names_rejected(self):
        for name in ('bad\\q', 'bad\\'):
            self.verify(self.original + '\\' + '0' * 64 + '  ' + name + '\n', 'invalid SHA256SUMS filename escape')

    def test_unresolvable_aliases_rejected(self):
        for name in ('missing/../README.md', 'README.md/', 'README.md/.', 'README.md/../README.md'):
            with self.subTest(name=name):
                replacement = record(self.readme[:64], name)
                self.verify(self.original.replace(self.readme, replacement), 'does not resolve to a regular file')

    def test_resolvable_aliases_remain_supported(self):
        for name in ('./README.md', '././README.md', 'object/../README.md'):
            with self.subTest(name=name):
                self.verify(self.original.replace(self.readme, record(self.readme[:64], name)))

    def test_nonexistent_whitespace_names_are_not_trimmed_to_existing_file(self):
        for name in (' README.md', 'README.md ', 'README.md\t'):
            with self.subTest(name=name):
                self.verify(self.original.replace(self.readme, record(self.readme[:64], name)), 'does not resolve to a regular file')

    def test_real_whitespace_and_separator_filenames_pass(self):
        names = [' lead.txt', 'trail.txt ', 'two  spaces.txt', '*star.txt', '#hash.txt',
                 'vertical\vtab.txt', 'form\ffeed.txt', 'unicode\u2028separator.txt']
        for name in names:
            p = Path(self.P) / 'object' / name
            p.write_text('synthetic payload\n')
        added = ''.join(record(hashlib.sha256((Path(self.P) / 'object' / name).read_bytes()).hexdigest(),
                               'object/' + name) + '\n' for name in names)
        self.verify(self.original + added)

    @unittest.skipIf(os.name == 'nt', 'literal backslash filenames require POSIX')
    def test_gnu_escaped_filenames_pass(self):
        names = ['slash\\q.txt', 'slash\\n.txt', 'line\nname.txt', 'carriage\rname.txt', 'slash\\.txt']
        for name in names:
            (Path(self.P) / 'object' / name).write_text('synthetic payload\n')
        added = ''.join(record(hashlib.sha256((Path(self.P) / 'object' / name).read_bytes()).hexdigest(),
                               'object/' + name) + '\n' for name in names)
        self.verify(self.original + added)

    def test_binary_uppercase_crlf_and_comments_pass(self):
        altered = '\r\n# GNU-compatible comment\r\n' + '\r\n'.join(
            line[:64].upper() + ' *' + line[66:] for line in self.original.splitlines()) + '\r\n'
        self.verify(altered)

    def test_escaped_outside_paths_and_nul_rejected(self):
        self.verify(self.original + '\\' + '0' * 64 + '  ../outside.txt\n', 'path leaves the package')
        self.verify(self.original + record('0' * 64, 'bad\0name') + '\n', 'NUL in SHA256SUMS filename')

    @unittest.skipIf(os.name == 'nt', 'non-UTF-8 filename bytes require POSIX')
    def test_invalid_utf8_must_not_alias_replacement_character(self):
        p = Path(self.P) / 'object' / 'bad\ufffdname'
        p.write_bytes(b'synthetic')
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        text = self.original + record(digest, 'object/bad\ufffdname') + '\n'
        self.manifest.write_bytes(text.encode('utf-8').replace(b'\xef\xbf\xbd', b'\xff'))
        self.assertFail('does not resolve to a regular file', '--package', self.P, '--no-exec')

    @unittest.skipIf(os.name == 'nt', 'non-UTF-8 filename bytes require POSIX')
    def test_actual_non_utf8_filename_bytes_remain_distinct(self):
        name = os.fsencode(self.P) + b'/object/bad\xffname'
        try:
            f = open(name, 'wb')
        except OSError as e:
            # macOS APFS refuses non-UTF-8 names (EILSEQ); a sandbox may refuse them first (EPERM).
            self.skipTest('this filesystem refuses non-UTF-8 filename bytes (errno %s: %s)' % (e.errno, e.strerror))
        with f:
            f.write(b'synthetic')
        digest = hashlib.sha256(b'synthetic').hexdigest().encode('ascii')
        self.manifest.write_bytes(self.original.encode('utf-8') + digest + b'  object/bad\xffname\n')
        self.assertPass('--package', self.P, '--no-exec')

    def test_stdin_marker_requires_explicit_relative_filename(self):
        p = Path(self.P) / '-'
        p.write_bytes(b'synthetic')
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        self.verify(self.original + record(digest, '-') + '\n', "'-' means stdin")
        self.verify(self.original + record(digest, './-') + '\n')

    def test_manifest_read_failure_is_reported(self):
        original = open
        def open_file(path, *args, **kwargs):
            if os.fspath(path) == str(self.manifest):
                raise PermissionError(13, 'Permission denied')
            return original(path, *args, **kwargs)
        with mock.patch('builtins.open', side_effect=open_file):
            self.assertFail('cannot read SHA256SUMS', '--package', self.P, '--no-exec')

    def test_manifest_read_remains_bounded(self):
        with mock.patch.object(fixtures.check_run, 'MAX_SCAN', 20):
            self.assertFail('SHA256SUMS exceeds the scan limit', '--package', self.P, '--no-exec')


if __name__ == '__main__':
    unittest.main(verbosity=2)
