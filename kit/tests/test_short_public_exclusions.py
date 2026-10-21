# SPDX-License-Identifier: AGPL-3.0-or-later
"""Synthetic raw-line exclusion regressions; package execution is disabled."""
import os
from pathlib import Path
import unittest
from unittest import mock
from test_check_run import Base, w, check_run as c


class ShortPublicExclusions(Base):
    def scan(self, private, public):
        path = Path(self.W, 'private', 'toy-cipher', 'excerpt.txt')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(private if isinstance(private, bytes) else private.encode('utf-8'))
        return c.secret_windows(self.W, public, {'toy-cipher': {'disclosure': 'commit-only'}})

    def assertDetected(self, private, public):
        secrets = self.scan(private, public)
        text = private.decode('utf-8', 'replace') if isinstance(private, bytes) else private
        self.assertIn(c.norm(text), secrets)

    def test_exact_whole_public_lines_all_short_lengths(self):
        for length in range(8, 16):
            token = 'ABCDEFGHJKLMNPQ'[:length]
            with self.subTest(length=length):
                self.assertEqual({}, self.scan(token, ['heading\n' + token + '\nending']))

    def test_exact_single_line_documents_and_optional_final_lf(self):
        for private in ('THEANSWER', 'THEANSWER\n'):
            for public in ('THEANSWER', 'THEANSWER\n'):
                with self.subTest(private=private, public=public):
                    self.assertEqual({}, self.scan(private, [public]))

    def test_exact_line_keeps_spaces_punctuation_and_case(self):
        token = 'The answer: 42!'
        self.assertEqual({}, self.scan(token, ['intro\n' + token + '\nend']))

    def test_longer_public_tokens_do_not_exclude_short_key(self):
        for token in ('THEANSWER', 'THEKEYIS'):
            with self.subTest(token=token):
                self.assertDetected(token, ['X' + token + 'Y'])

    def test_partial_public_sentence_does_not_exclude(self):
        self.assertDetected('THEANSWER', ['Here THEANSWER is only a substring.'])

    def test_space_punctuation_and_case_normalization_do_not_exclude(self):
        for public in ('THE ANSWER', 'THE-ANSWER', 'theanswer', ' THEANSWER', 'THEANSWER ', 'THE\tANSWER'):
            with self.subTest(public=public):
                self.assertDetected('THEANSWER', [public])

    def test_private_edge_whitespace_is_not_stripped(self):
        for private in (' THEANSWER', 'THEANSWER ', '\tTHEANSWER', 'THEANSWER\n\n'):
            with self.subTest(private=private):
                self.assertDetected(private, ['THEANSWER'])

    def test_public_lines_are_not_joined(self):
        self.assertDetected('THEANSWER', ['THE\nANSWER'])

    def test_public_documents_are_not_joined(self):
        self.assertDetected('THEANSWER', ['THE', 'ANSWER'])

    def test_multiline_private_text_is_not_excluded(self):
        for public in (['THEANSWER'], ['THE\nANSWER']):
            with self.subTest(public=public):
                self.assertDetected('THE\nANSWER', public)

    def test_unicode_separators_are_not_line_boundaries(self):
        for separator in ('\u2028', '\u2029', '\x85', '\v', '\f'):
            with self.subTest(separator=repr(separator)):
                self.assertDetected('THEANSWER', ['heading' + separator + 'THEANSWER' + separator + 'ending'])

    def test_unicode_normalization_and_lookalikes_do_not_exclude(self):
        for private, public in [('THEANSWER', 'THE\u200bANSWER'),
                                ('THEANSWER', 'THE\u00a0ANSWER'),
                                ('THEANSWER', 'THEANSW\u00c9R'),
                                ('THEANSWER\u00e9', 'THEANSWERe\u0301'),
                                ('STRASSE12', 'STRA\u00dfE12')]:
            with self.subTest(private=private, public=public):
                self.assertDetected(private, [public])

    def test_exact_unicode_line_is_supported(self):
        self.assertEqual({}, self.scan('THEANSWER\u00e9', ['THEANSWER\u00e9']))

    def test_utf8_replacement_cannot_establish_exact_identity(self):
        self.assertDetected(b'THEANSWER\xff', ['THEANSWER\ufffd'])
        self.assertDetected('THEANSWER\ufffd', ['THEANSWER\ufffd'])

    def test_truncated_private_line_cannot_establish_exact_match(self):
        prefix = 'THEANSWER' + ' ' * (200_000 - len('THEANSWER'))
        self.assertIn('THEANSWER', self.scan(prefix + 'X', [prefix]))

    def test_unavailable_private_size_retains_detection(self):
        with mock.patch.object(c.os.path, 'getsize', side_effect=OSError('synthetic')):
            self.assertDetected('THEANSWER', ['THEANSWER'])

    def test_nonpublic_short_secret_is_detected(self):
        self.assertDetected('THEANSWER', ['unrelated'])

    def test_less_than_eight_normalized_characters_unchanged(self):
        self.assertEqual({}, self.scan('ABCDEF7', []))

    def test_long_secret_logic_unchanged(self):
        for length in (16, 20, 24):
            token = ''.join(chr(ord('A') + i) for i in range(length))
            with self.subTest(length=length):
                self.assertEqual({}, self.scan(token, ['prefix ' + token.lower() + ' suffix']))
                self.assertTrue(self.scan(token, ['unrelated public text']))

    def test_generator_public_documents_preserve_long_logic(self):
        token = ''.join(chr(ord('A') + i) for i in range(24))
        self.assertEqual({}, self.scan(token, iter([token])))

    def workspace(self, public):
        self.attack()
        token = 'THEANSWER'
        w(os.path.join(self.W, 'private', 'toy-cipher', 'excerpt.txt'), token)
        w(os.path.join(self.R, 'data', 'public.txt'), public)
        w(os.path.join(self.W, 'REPORT.md'), '# Report\n' + token + '\n')
        return self.run_check(self.W, '--no-exec')

    def test_workspace_exact_public_line_avoids_false_fail(self):
        self.assertEqual(0, self.workspace('intro\nTHEANSWER\nend'), self.out)

    def test_workspace_normalized_bank_phrase_still_detected(self):
        self.assertEqual(1, self.workspace('intro THE ANSWER ending'), self.out)
        self.assertIn('commit-only secrets stay in private', self.out)

    def test_workspace_short_key_in_long_token_still_detected(self):
        self.assertEqual(1, self.workspace('XTHEANSWERY'), self.out)
        self.assertIn('commit-only secrets stay in private', self.out)


if __name__ == '__main__':
    unittest.main(verbosity=2)
