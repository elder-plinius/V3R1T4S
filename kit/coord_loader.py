#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""coord_loader: coordinate-file parser and validator (dimension-aware, index-aware, flag-don't-fix).

Contract and rationale: kit/COORD-LOADER.md. Tests: kit/tests/test_coord_loader.py.
  - XYZ element-label rows ('Ar 0.1 0.2 0.3') are data: label stripped, row counted in N.
  - XYZ 2-line header (line 1 = a single integer count, line 2 = comment) is detected and both lines
    skipped; the parsed N must equal the declared count, else CoordAnomaly(count_mismatch).
  - NaN/Inf tokens raise CoordAnomaly(non_finite); an index run must span >= 3 rows, else
    CoordAnomaly(ambiguous_small_file); lines whose first non-blank character is '#' are comments.

Public API (standard library only):
    class CoordAnomaly(Exception)   attributes: kind, lines, found_columns, expected_columns
    load_coords(path, dim, allow_index=True) -> list of N rows, each `dim` decimal.Decimal values

Values are decimal.Decimal parsed from the original token strings, so they are lossless
(str(value) reproduces the token's digits). Convert with float() only after loading if needed.

CLI:  python3 kit/coord_loader.py FILE --dim D [--no-index]
      prints N rows (exact decimal strings) or the anomaly; exit 0 = clean, 3 = CoordAnomaly.
"""
import re
import sys
from decimal import Decimal

__all__ = ["CoordAnomaly", "load_coords"]

KINDS = ("dimension_mismatch", "mixed_tokens", "index_in_dim_columns", "empty",
         "count_mismatch", "non_finite", "ambiguous_small_file")

# Column 0 is only treated as an index (rules 2 and 5) when the run spans >= this many rows.
MIN_INDEX_RUN_ROWS = 3

# Plain decimal / scientific literal. Deliberately stricter than Decimal(): no '_' separators,
# no NaN/Infinity, no Fortran 'D' exponents, no thousands commas.
_NUM = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")
_NONFINITE = re.compile(r"^[+-]?(?:nan|snan|inf|infinity)$", re.IGNORECASE)
_INT = re.compile(r"^[+]?\d+$")


class CoordAnomaly(Exception):
    """Data-integrity anomaly raised instead of returning (possibly) wrong coordinates.

    kind              one of
                        'dimension_mismatch'    row width not dim/dim+1, mixed widths, dim+1 without a proven index,
                                                or dim+1 with allow_index=False
                        'mixed_tokens'          non-numeric token after a number (or more than one leading label),
                                                or non-UTF-8 file
                        'index_in_dim_columns'  exactly dim columns but col0 is a sequential integer run (rule 5)
                        'empty'                 missing file or no data rows (rule 8)
                        'count_mismatch'        XYZ count line (line 1) != number of parsed data rows
                        'non_finite'            NaN / Inf token anywhere in the file
                        'ambiguous_small_file'  soft / needs-human: N < 3 rows and col0 looks like an index run
                                                (integer-valued 0.. or 1..); too few rows to decide index vs data
    lines             1-based line numbers of the offending rows (list, possibly empty)
    found_columns     numeric-token count found (int, or sorted list of ints if several widths), or None
    expected_columns  accepted widths [dim, dim+1] (or [dim] if allow_index=False), or None
    """

    def __init__(self, kind, message, lines=None, found_columns=None, expected_columns=None):
        if kind not in KINDS:
            raise ValueError("unknown CoordAnomaly kind %r" % (kind,))
        self.kind = kind
        self.lines = list(lines or [])
        self.found_columns = found_columns
        self.expected_columns = expected_columns
        self.message = message
        super().__init__("%s: %s" % (kind, message))


def _is_index_run(values):
    """Rule 2/6 test, file-wide: integer-valued run starting at 0 or 1, step 1."""
    if not values:
        return False
    for v in values:
        if v != v.to_integral_value():
            return False
    base = values[0]
    if base not in (0, 1):
        return False
    return all(v == base + i for i, v in enumerate(values))


def _fmt_lines(lines, cap=8):
    s = ", ".join(str(l) for l in lines[:cap])
    return s + (", ..." if len(lines) > cap else "")


def load_coords(path, dim, allow_index=True):
    """Return N rows of exactly `dim` coordinates (list of lists of Decimal).

    Raises CoordAnomaly on any mismatch. Never pads, truncates, reorders or guesses.
    """
    if isinstance(dim, bool) or not isinstance(dim, int) or dim < 1:
        raise ValueError("dim must be a positive int declared by the caller, got %r" % (dim,))
    expected = [dim, dim + 1] if allow_index else [dim]

    # Rule 8: no file -> empty.
    try:
        with open(path, "r", encoding="utf-8-sig", newline=None) as fh:
            text = fh.read()
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError) as ex:
        raise CoordAnomaly("empty", "no such coordinate file: %s (%s)" % (path, type(ex).__name__),
                           expected_columns=expected)
    except UnicodeDecodeError as ex:
        raise CoordAnomaly("mixed_tokens", "file is not valid UTF-8 text: %s (%s)" % (path, ex),
                           expected_columns=expected)
    raw_lines = text.splitlines()

    # XYZ 2-line header. Line 1 is exactly one non-negative integer token, and line 2
    # (any content, may be blank or contain numbers) is the comment line. Not applied for dim == 1,
    # where a single integer on line 1 is a legitimate 1-D data row.
    declared_count = None
    start = 0
    if dim > 1 and raw_lines:
        first = raw_lines[0].split()
        if len(first) == 1 and _INT.match(first[0]):
            declared_count = int(first[0])
            start = min(2, len(raw_lines))

    rows = []  # (lineno, [Decimal, ...])
    for idx in range(start, len(raw_lines)):
        lineno = idx + 1
        toks = raw_lines[idx].split()
        if not toks:
            continue  # rule 4: blank line
        if toks[0].startswith("#"):
            continue  # '#' as first non-whitespace char = comment line, skipped
        bad = [t for t in toks if _NONFINITE.match(t)]
        if bad:
            raise CoordAnomaly("non_finite", "line %d: non-finite token %r is not a coordinate" % (lineno, bad[0]),
                               lines=[lineno], expected_columns=expected)
        isnum = [bool(_NUM.match(t)) for t in toks]
        if not any(isnum):
            continue  # rule 4: header line (no numeric tokens), e.g. 'N X Y Z'
        if not isnum[0]:
            # one leading non-numeric token (XYZ element label) is stripped; the row is data
            toks, isnum = toks[1:], isnum[1:]
        if not all(isnum):
            j = isnum.index(False)
            raise CoordAnomaly("mixed_tokens", "line %d: non-numeric token %r after a number" % (lineno, toks[j]),
                               lines=[lineno], expected_columns=expected)
        rows.append((lineno, [Decimal(t) for t in toks]))

    # Rule 8: no data rows -> empty.
    if not rows:
        raise CoordAnomaly("empty", "no data rows in %s" % (path,), expected_columns=expected)

    # Rule 3: every row width must be dim or dim+1 ...
    bad = [(ln, len(v)) for ln, v in rows if len(v) not in (dim, dim + 1)]
    if bad:
        widths = sorted({w for _, w in bad})
        lines = [ln for ln, _ in bad]
        raise CoordAnomaly("dimension_mismatch",
                           "%d row(s) with %s numeric columns where %s expected (dim=%d), lines %s"
                           % (len(bad), "/".join(map(str, widths)), " or ".join(map(str, [dim, dim + 1])), dim,
                              _fmt_lines(lines)),
                           lines=lines, found_columns=widths[0] if len(widths) == 1 else widths,
                           expected_columns=[dim, dim + 1])
    # ... and uniform across the file (rule 6: decisions are file-wide).
    widths = sorted({len(v) for _, v in rows})
    if len(widths) > 1:
        n_dim = sum(1 for _, v in rows if len(v) == dim)
        minority = dim if n_dim <= len(rows) - n_dim else dim + 1
        lines = [ln for ln, v in rows if len(v) == minority]
        raise CoordAnomaly("dimension_mismatch",
                           "mixed row widths %s in one file (dim=%d); minority-width (%d) lines %s"
                           % (widths, dim, minority, _fmt_lines(lines)),
                           lines=lines, found_columns=widths, expected_columns=[dim, dim + 1])
    width = widths[0]
    all_lines = [ln for ln, _ in rows]
    col0_is_index = _is_index_run([v[0] for _, v in rows])

    # Tiny-file guard. With N < 3 a col0 of 0.0/1.0(/...) is too weak to prove an index,
    # so neither strip it (rule 2) nor flag it as index_in_dim_columns (rule 5) nor accept it: needs a human.
    if col0_is_index and len(rows) < MIN_INDEX_RUN_ROWS and not (width == dim + 1 and not allow_index):
        raise CoordAnomaly("ambiguous_small_file",
                           "only %d data row(s) and column 0 (%s) looks like a sequential integer index; "
                           "an index needs a run of >= %d rows to be proven (needs human review)"
                           % (len(rows), ", ".join(str(v[0]) for _, v in rows), MIN_INDEX_RUN_ROWS),
                           lines=all_lines, found_columns=width, expected_columns=expected)

    if width == dim + 1:
        if not allow_index:
            raise CoordAnomaly("dimension_mismatch",
                               "%d columns with dim=%d and allow_index=False" % (width, dim),
                               lines=all_lines, found_columns=width, expected_columns=[dim])
        if not col0_is_index:  # rule 2: never drop a column that is not a proven index
            raise CoordAnomaly("dimension_mismatch",
                               "%d columns with dim=%d but column 0 is not a sequential integer index run"
                               % (width, dim),
                               lines=all_lines, found_columns=width, expected_columns=[dim, dim + 1])
        out = [v[1:] for _, v in rows]
    else:  # width == dim
        if col0_is_index:  # rule 5 (fixture 6b): index + (dim-1) coords; do not strip, do not accept
            raise CoordAnomaly("index_in_dim_columns",
                               "%d columns with dim=%d but column 0 is a sequential integer run (%s, ...): "
                               "index + %d coordinates, i.e. a truncated file"
                               % (width, dim, ", ".join(str(v[0]) for _, v in rows[:3]), dim - 1),
                               lines=all_lines, found_columns=width,
                               expected_columns=[dim, dim + 1] if allow_index else [dim])
        out = [v for _, v in rows]

    # Declared XYZ count must match the parsed N.
    if declared_count is not None and declared_count != len(out):
        raise CoordAnomaly("count_mismatch",
                           "XYZ count line declares N=%d but %d data rows were parsed (line 2 is treated as "
                           "the XYZ comment line)" % (declared_count, len(out)),
                           lines=[1], found_columns=width, expected_columns=expected)
    return out


def _main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="Load and validate a coordinate file (see kit/COORD-LOADER.md).")
    ap.add_argument("path")
    ap.add_argument("--dim", type=int, required=True, help="declared dimension (never inferred)")
    ap.add_argument("--no-index", action="store_true", help="allow_index=False")
    a = ap.parse_args(argv)
    try:
        rows = load_coords(a.path, a.dim, allow_index=not a.no_index)
    except CoordAnomaly as ex:
        print("CoordAnomaly kind=%s lines=%s found_columns=%s expected_columns=%s\n  %s"
              % (ex.kind, ex.lines, ex.found_columns, ex.expected_columns, ex.message))
        return 3
    print("# N=%d dim=%d" % (len(rows), a.dim))
    for r in rows:
        print("  ".join(str(x) for x in r))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
