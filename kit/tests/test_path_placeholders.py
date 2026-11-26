# SPDX-License-Identifier: AGPL-3.0-or-later
"""A path template quoted in an inline code span is documentation, not an unfilled placeholder (#61).

    python3 -m unittest discover -s kit/tests -p 'test_path_placeholders.py' -v
"""
import os
import unittest
from test_check_run import SourcePlaceholders, w
import check_run


class QuotedPathTemplates(SourcePlaceholders):
    def doc(self, text):
        P = self._confirmed()
        w(os.path.join(P, "HOW_WE_FOUND_IT.md"), "Contributor text, unverified.\n" + text + "\n")
        self.sums(P)
        return P

    def test_quoted_path_template_passes(self):
        """The case from the field: a panel file saying where its own working notes were saved."""
        self.doc("Each skeptic's notes are under `panel_work/novelty/<name>/body` in the run folder.")
        self.assertPass(self.W)

    def test_quoted_path_template_with_several_tokens_passes(self):
        self.doc("Runs are saved as `runs/<date>-<time>/attempts/<lens>/report.md`.")
        self.assertPass(self.W)

    def test_placeholder_outside_a_code_span_still_fails(self):
        self.doc("Built by <credit_name>.")
        self.assertFail("unfilled placeholder <credit_name>", self.W)

    def test_placeholder_in_a_code_span_without_a_slash_still_fails(self):
        """A bare field in backticks is still a field; only a path template is exempt."""
        self.doc("Fill in `<credit_name>` before submitting.")
        self.assertFail("unfilled placeholder <credit_name>", self.W)

    def test_workdir_in_a_quoted_path_still_fails(self):
        """An unfilled workspace path is the thing this check exists to catch, code span or not."""
        self.doc("Run it from `<WORKDIR>/runs/2026-10-12-0300`.")
        self.assertFail("unfilled placeholder <WORKDIR>", self.W)


class Unit(unittest.TestCase):
    """unfilled_placeholder() alone, so a regression is localised without building a workspace."""

    def hit(self, t):
        m = check_run.unfilled_placeholder(t)
        return m.group(0) if m else None

    def test_exempt(self):
        for t in ("see `panel_work/novelty/<name>/body`",
                  "`runs/<date>-<time>/panel`",
                  "`a/<n>/b` and `c/<path>/d`",
                  "prose before `x/<lens>/y` and prose after"):
            self.assertIsNone(self.hit(t), t)

    def test_still_reported(self):
        for t, want in (("Built by <credit_name>.", "<credit_name>"),
                        ("`<credit_name>`", "<credit_name>"),
                        ("`<WORKDIR>/runs`", "<WORKDIR>"),
                        ("a `code/span` and then <credit_name>", "<credit_name>"),
                        ("`unclosed/span <name>", "<name>"),
                        ("`one/span` then `two/span` then <date>", "<date>")):
            self.assertEqual(self.hit(t), want, t)

    def test_a_span_does_not_reach_across_lines(self):
        """Backticks are per-line, so a stray backtick cannot exempt a placeholder further down the file."""
        self.assertEqual(self.hit("a `stray/backtick\nBuilt by <credit_name>.\n"), "<credit_name>")


if __name__ == "__main__":
    unittest.main(verbosity=2)
