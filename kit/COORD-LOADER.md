# Coordinate loader

`kit/coord_loader.py` is a robust parser and validator for coordinate files (Packomania-style tables, sphere and
hypersphere codes, atomic clusters, XYZ). It is **dimension-aware, index-aware, and a flagger, not a fixer**: it
returns exactly `dim` coordinates per row, or raises `CoordAnomaly` and returns nothing. Standard library only.

A loader that "takes the last 3 numeric columns" is right only for d = 3. On higher-dimensional data it silently
drops real coordinates, and on index-prefixed or ragged files it quietly accepts malformed rows. Both have produced
false discrepancies before; this loader turns them into explicit anomalies before any radius or energy is computed.

## Use

```python
from coord_loader import load_coords, CoordAnomaly
rows = load_coords("hsp4.txt", dim=4)          # N rows, each 4 decimal.Decimal values
try:
    load_coords(path, dim=5, allow_index=False)
except CoordAnomaly as ex:
    ex.kind, ex.lines, ex.found_columns, ex.expected_columns
```

```sh
python3 kit/coord_loader.py FILE --dim D [--no-index] [--trailing-radius]   # exit 0 = clean, 3 = CoordAnomaly
```

## Contract

`load_coords(path, dim, allow_index=True, trailing_radius=False)`. `dim` is required and declared by the caller, never inferred
(`dim=None` raises `ValueError`).

1. **Dimension-aware.** Every accepted row yields exactly `dim` coordinates.
2. **Index-aware.** With `dim + 1` columns and `allow_index=True`, column 0 is stripped only if, over all data rows,
   it is an integer-valued run 0,1,2,… or 1,2,3,… spanning at least 3 rows. Otherwise `dimension_mismatch`. With
   `allow_index=False`, `dim + 1` columns is a `dimension_mismatch`.
3. **Flag, don't fix.** A row width other than `dim` or `dim + 1`, or mixed widths in one file, raises. No padding,
   truncation, dropped rows, or partial result.
4. **Headers and labels.** Blank lines, lines with no numeric tokens, and lines whose first non-blank character is
   `#` are skipped. One leading non-numeric token (`Ar 0.1 0.2 0.3`) is a label: stripped, row kept. A non-numeric
   token after a number (including a trailing `# ...`) is `mixed_tokens`.
5. **Index hidden in `dim` columns.** Exactly `dim` columns whose column 0 is an index run (rule 2) is an index plus
   `dim - 1` coordinates, a truncated file: `index_in_dim_columns`. It is never stripped to `dim - 1`.
6. **File-wide.** The index decision is made once for the whole file, not per row.
7. **Lossless.** Values are `decimal.Decimal` built from the original token strings (30-decimal values survive).
   `str()` of a Decimal may use exponent form (`0.000000000000` -> `0E-12`); `format(v, "f")` returns the
   fixed-point digits, and the CLI prints that way. Call `float()` yourself after loading if you need floats.
8. **Empty.** A missing file or a file with no data rows raises `empty`; an empty list is never returned.

XYZ: a line 1 holding a single non-negative integer is a count line only when line 2 is blank or does not parse as a
data row. Then both lines are skipped and the parsed row count must equal that integer. If line 2 looks like data,
line 1 stays an ordinary row (and a width-1 row raises), so a real data row is never eaten as a comment.

Packomania scu/ssp layout (opt-in): `trailing_radius=True` expects the first data line to be the radius R alone and
every row to end in a radius column equal to R; both are stripped, then the rules above apply. A missing radius line,
a radius column that differs from R, or a lone trailing index line (a blank last sphere) raises
`dimension_mismatch`. The default is strict: without the option such files raise.

### Anomaly kinds

| kind | when |
|---|---|
| `dimension_mismatch` | a row width not in {dim, dim+1}; mixed widths; `dim + 1` columns without a proven index |
| `index_in_dim_columns` | `dim` columns whose column 0 is a sequential integer run (rule 5) |
| `mixed_tokens` | a non-numeric token after a number, or two leading labels |
| `non_finite` | a NaN or Inf token anywhere |
| `count_mismatch` | XYZ count line disagrees with the parsed row count (`lines=[1]`) |
| `ambiguous_small_file` | fewer than 3 rows and column 0 looks like an index start; needs a human decision |
| `empty` | missing file, or no data rows |

Attributes: `lines` (1-based line numbers), `found_columns`, `expected_columns` (`[dim]` or `[dim, dim+1]`).

`found_columns` rule: when the file mixes widths `dim` and `dim + 1`, it lists **all** widths found (e.g. `[3, 4]`);
otherwise it holds just the offending width(s): an int for one width, a sorted list for several.

## Tests

```sh
python3 kit/tests/test_coord_loader.py
```

Fixtures live in `kit/tests/fixtures/coord_loader/`: each `<name>.txt` has a `<name>.expected.json` (dim,
allow_index, and either the exact rows or the anomaly kind, lines and columns), and `SHA256SUMS` pins the pack.

## Method

The tests run four layers, all stdlib `unittest`:

- **Pack integrity:** every fixture matches `SHA256SUMS`, and every `expected.json` is self-consistent.
- **Pack cases:** 21 cases (20 fixtures plus the `allow_index=False` variant of `hsp4_indexed_5col`). Clean cases are
  compared value by value as `Decimal`; the 30-decimal fixture must match exactly.
- **Negative control:** a naive "last 3 numeric columns" loader is run over the same pack and must fail the
  discriminating fixtures (true 4-D data, indexed 5-column, index + 4 coords at dim 5 and 6, ragged rows, a lone trailing index line,
  the Packomania radius layout). It fails 14 of 21. This
  proves the fixtures can tell a correct loader from the common bug.
- **Behaviour checks:** anomaly attributes against each fixture, XYZ count and label handling, comments, NaN/Inf,
  empty and missing files, gapped or reordered indexes, tiny-file guard, mixed widths, a 38-row `index x y z` file,
  the count-line regression, the `trailing_radius` option and CLI output (70 checks in total).

Fixture values are synthetic except `scu30_real_*`, which hold published Packomania scu30 data (file as of
2026-10-17, whose last sphere is a lone index line).
