# SPDX-License-Identifier: AGPL-3.0-or-later
"""Tests for kit/coord_loader.py against the fixture pack in kit/tests/fixtures/coord_loader/. Standard library only.

    python3 kit/tests/test_coord_loader.py

Each fixtures/<name>.txt has a sibling <name>.expected.json (dim, allow_index, and either N/columns/coords or the
anomaly kind, rows, found_columns, expected_columns). A naive "last 3 numeric columns" loader is run as a negative
control: the pack must catch it.
"""
import contextlib, glob, hashlib, io, json, os, sys, tempfile, unittest
from decimal import Decimal as D, InvalidOperation

HERE = os.path.dirname(os.path.abspath(__file__))
FX = os.path.join(HERE, "fixtures", "coord_loader")
sys.path.insert(0, os.path.dirname(HERE))
import coord_loader  # noqa: E402
from coord_loader import CoordAnomaly, load_coords  # noqa: E402

PACK_CASES = 21  # 20 fixtures + the allow_index=False variant of hsp4_indexed_5col
MUST_CATCH = {"hsp4_true4d.txt", "hsp4_indexed_5col.txt", "hsp6_anomaly_4col.txt", "hsp5_index_plus4_5col.txt",
              "ragged_rows.txt", "scu_trailing_index_only.txt", "scu_trailing_index_only_noindex.txt",
              "scu30_real_trailing_index.txt", "scu30_real_packomania.txt", "packomania_radius_layout.txt"}


def cases():
    for ej in sorted(glob.glob(os.path.join(FX, "*.expected.json"))):
        with open(ej) as f:
            e = json.load(f)
        yield e, os.path.join(FX, e["fixture"])
        if "with_allow_index_false" in e:
            e2 = dict(e, allow_index=False, **e["with_allow_index_false"])
            e2["fixture_variant"] = "allow_index=False"
            yield e2, os.path.join(FX, e["fixture"])


class NaiveAnomaly(Exception):
    pass


def naive_last3(path, dim, allow_index=True):
    """Negative control only: the 'last 3 numeric tokens per row' pattern this loader replaces."""
    out = []
    with open(path) as f:
        for line in f:
            nums = []
            for t in line.split():
                try:
                    nums.append(D(t))
                except InvalidOperation:
                    pass
            if len(nums) >= 3:
                out.append(nums[-3:])
    return out


def to_dec(x):
    return D(x) if isinstance(x, str) else D(repr(float(x))) if isinstance(x, float) else D(str(x))


def run_case(load, anomaly_cls, e, path):
    """(ok, message) for one pack case. Values must match exactly; float rounding within 1e-15 is tolerated
    except on the 30-decimal fixture."""
    try:
        got = load(path, e["dim"], allow_index=e["allow_index"])
    except anomaly_cls as ex:
        return (e["status"] == "anomaly"), "raised %s: %s" % (type(ex).__name__, ex)
    except Exception as ex:  # any other exception is a contract failure
        return False, "raised non-contract exception %s: %s" % (type(ex).__name__, ex)
    if e["status"] == "anomaly":
        return False, "returned data instead of raising CoordAnomaly (%s)" % e["anomaly"]
    rows = [list(r) for r in got]
    if len(rows) != e["N"]:
        return False, "N=%d, expected %d" % (len(rows), e["N"])
    if any(len(r) != e["columns"] for r in rows):
        return False, "a row does not have %d columns" % e["columns"]
    lossy = False
    for i, (r, want) in enumerate(zip(rows, e["coords"])):
        for j, (g, w) in enumerate(zip(r, want)):
            g, w = to_dec(g), D(w)
            if g != w:
                if abs(g - w) <= D("1e-15") * max(1, abs(w)):
                    lossy = True
                else:
                    return False, "row %d col %d = %s, expected %s" % (i, j, g, w)
    if lossy and "30dec" in e["fixture"]:
        return False, "30-decimal values lost precision (float?)"
    return True, "ok"


def _widths(v):
    if v is None:
        return None
    return sorted(set(v)) if isinstance(v, (list, tuple)) else [v]


class PackTests(unittest.TestCase):
    def test_checksums(self):
        listed = {}
        with open(os.path.join(FX, "SHA256SUMS")) as f:
            for line in f:
                h, name = line.split()
                listed[name] = h
        present = {n for n in os.listdir(FX) if n != "SHA256SUMS"}
        self.assertEqual(set(listed), present)
        for name, h in listed.items():
            with open(os.path.join(FX, name), "rb") as f:
                self.assertEqual(hashlib.sha256(f.read()).hexdigest(), h, name)

    def test_fixtures_self_consistent(self):
        for e, path in cases():
            with self.subTest(e["fixture"]):
                self.assertTrue(os.path.isfile(path))
                if e["status"] == "ok":
                    self.assertEqual(len(e["coords"]), e["N"])
                    self.assertTrue(all(len(r) == e["columns"] for r in e["coords"]))
                    self.assertEqual(e["columns"], e["dim"])
                else:
                    self.assertTrue(e.get("anomaly"))

    def test_pack_cases(self):
        all_cases = list(cases())
        self.assertEqual(len(all_cases), PACK_CASES)
        for e, path in all_cases:
            with self.subTest(e["fixture"], variant=e.get("fixture_variant")):
                ok, msg = run_case(load_coords, CoordAnomaly, e, path)
                self.assertTrue(ok, msg)

    def test_naive_control_is_caught(self):
        failed = {e["fixture"] for e, p in cases() if not run_case(naive_last3, NaiveAnomaly, e, p)[0]}
        self.assertTrue(MUST_CATCH <= failed, sorted(MUST_CATCH - failed))

    def test_anomaly_attributes(self):
        n = 0
        for e, path in cases():
            if e["status"] != "anomaly":
                continue
            n += 1
            with self.subTest(e["fixture"], variant=e.get("fixture_variant")):
                with self.assertRaises(CoordAnomaly) as cm:
                    load_coords(path, e["dim"], allow_index=e["allow_index"])
                ex = cm.exception
                self.assertEqual(ex.kind, e["anomaly"])
                self.assertEqual(ex.lines, e["rows"])
                if "found_columns" in e:
                    self.assertEqual(_widths(ex.found_columns), _widths(e["found_columns"]))
                if "expected_columns" in e:
                    self.assertEqual(ex.expected_columns, e["expected_columns"])
        self.assertGreater(n, 0)


class BehaviourTests(unittest.TestCase):
    """XYZ headers and labels, comments, non-finite values, empty input, index edge cases, small files."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.n = 0

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_behaviour(self):
        results = []

        def check(name, cond, info=""):
            results.append(bool(cond))
            with self.subTest(name):
                self.assertTrue(cond, info)

        def tmp(text):
            self.n += 1
            p = os.path.join(self.tmpdir.name, "c%d.txt" % self.n)
            with open(p, "w") as f:
                f.write(text)
            return p

        def anomaly(path, dim, **kw):
            try:
                load_coords(path, dim, **kw)
            except CoordAnomaly as ex:
                return ex
            return None

        # XYZ label rows XYZ label rows are data
        p = tmp("Ar 0.1 0.2 0.3\nAr 0.4 0.5 0.6\nKr -1 -2 -3\n")
        r = load_coords(p, 3)
        check("xyz label rows kept, label stripped, N=3", len(r) == 3 and r[2] == [D(-1), D(-2), D(-3)], r)

        # XYZ 2-line header, count matches; comment line may contain numbers
        p = tmp("3\nEnergy: -5.0 step 12\nAr 0.1 0.2 0.3\nAr 0.4 0.5 0.6\nAr 0.7 0.8 0.900000000000000000000000000001\n")
        r = load_coords(p, 3)
        check("xyz count+comment skipped, N=3, lossless", len(r) == 3 and str(r[2][2]) == "0.900000000000000000000000000001", r)
        p = tmp("2\n\n0.1 0.2 0.3\n0.4 0.5 0.6\n")
        check("xyz count + blank comment line", len(load_coords(p, 3)) == 2)
        # count mismatch -> anomaly
        p = tmp("4\ncomment\nAr 0.1 0.2 0.3\nAr 0.4 0.5 0.6\nAr 0.7 0.8 0.9\n")
        ex = anomaly(p, 3)
        check("xyz count mismatch -> count_mismatch", ex is not None and ex.kind == "count_mismatch" and ex.lines == [1], ex)
        p = tmp("2\ncomment\nAr 0.1 0.2 0.3\nAr 0.4 0.5 0.6\nAr 0.7 0.8 0.9\n")
        ex = anomaly(p, 3)
        check("xyz count too small -> count_mismatch", ex is not None and ex.kind == "count_mismatch", ex)
        # count line with no comment line: line 2 looks like data, so line 1 is not a count line; the lone integer
        # is a width-1 row and is flagged. No data row is consumed as a comment.
        p = tmp("3\n0.1 0.2 0.3\n0.4 0.5 0.6\n0.7 0.8 0.9\n")
        ex = anomaly(p, 3)
        check("count line without comment line -> dimension_mismatch on line 1, not silent",
              ex is not None and ex.kind == "dimension_mismatch" and ex.lines == [1], ex)
        # regression: integer on line 1 equal to the remaining row count must not eat data row 2
        p = tmp("2\n0.1 0.2 0.3\n0.4 0.5 0.6\n0.7 0.8 0.9\n")
        ex = anomaly(p, 3)
        check("line-1 integer == remaining rows: line 2 is not eaten (raises, no N=2)",
              ex is not None and ex.kind == "dimension_mismatch" and ex.lines == [1], ex)
        p = tmp("1\n0.1 0.2 0.3\n0.4 0.5 0.6\n")
        ex = anomaly(p, 3)
        check("line-1 '1' + 2 data rows: no silent N=1", ex is not None and ex.kind == "dimension_mismatch", ex)
        p = tmp("2\nAr 0.1 0.2 0.3\nAr 0.4 0.5 0.6\n")
        ex = anomaly(p, 3)
        check("label row on line 2 is data, not an XYZ comment", ex is not None and ex.lines == [1], ex)
        # multi-frame XYZ: second count line is a width-1 row -> flagged
        p = tmp("1\nf1\nAr 0 0 0\n1\nf2\nAr 1 1 1\n")
        ex = anomaly(p, 3)
        check("multi-frame xyz flagged", ex is not None and ex.kind == "dimension_mismatch" and ex.lines == [4], ex)  # "f2" has no numeric tokens -> header (rule 4)
        # xyz header with indexed rows (CCD-ish) still goes through rule 2
        p = tmp("3\nLJ3\n1 0.0 0.0 0.0\n2 1.1 0.0 0.0\n3 0.5 0.9 0.0\n")
        check("xyz header + index x y z", load_coords(p, 3)[1] == [D("1.1"), D("0.0"), D("0.0")])

        # edge cases
        p = tmp("0.1 0.2 abc\n")
        ex = anomaly(p, 3)
        check("non-numeric after number -> mixed_tokens", ex is not None and ex.kind == "mixed_tokens" and ex.lines == [1], ex)
        p = tmp("Ar He 0.1 0.2 0.3\n")
        ex = anomaly(p, 3)
        check("two leading labels -> mixed_tokens", ex is not None and ex.kind == "mixed_tokens", ex)
        for bad in ("nan", "inf", "-Infinity", "NaN"):
            p = tmp("0.1 0.2 %s\n0.1 0.2 0.3\n" % bad)
            ex = anomaly(p, 3)
            check("non-finite %s -> non_finite" % bad, ex is not None and ex.kind == "non_finite" and ex.lines == [1], ex)
        p = tmp("nan 0.1 0.2 0.3\n")
        ex = anomaly(p, 3)
        check("leading nan not taken as a label -> non_finite", ex is not None and ex.kind == "non_finite", ex)
        ex = anomaly(tmp("0.1 0.2 0.3\n0.4 0.5 0.6\n0.7 0.8 1e999999\n"), 3)
        check("huge finite exponent is not non_finite", ex is None, ex)
        p = tmp("\n\nN X Y Z\n\n")
        ex = anomaly(p, 3)
        check("header-only file -> empty", ex is not None and ex.kind == "empty", ex)
        p = tmp("")
        ex = anomaly(p, 3)
        check("zero-byte file -> empty", ex is not None and ex.kind == "empty", ex)
        ex = anomaly("/nonexistent/coords.txt", 3)
        check("missing file -> empty", ex is not None and ex.kind == "empty", ex)
        p = tmp("0\ncomment\n")
        ex = anomaly(p, 3)
        check("xyz count 0, no rows -> empty", ex is not None and ex.kind == "empty", ex)
        # gapped / non-sequential index
        for name, txt in [("gapped 1,2,4", "1 0 0 0\n2 1 0 0\n4 0 1 0\n"),
                          ("starts at 2", "2 0 0 0\n3 1 0 0\n4 0 1 0\n"),
                          ("reordered", "1 0 0 0\n3 1 0 0\n2 0 1 0\n"),
                          ("non-integer col0", "1.5 0 0 0\n2.5 1 0 0\n3.5 0 1 0\n")]:
            ex = anomaly(tmp(txt), 3)
            check("index %s -> dimension_mismatch" % name, ex is not None and ex.kind == "dimension_mismatch", ex)
        # integer-valued decimal index accepted (rule 2 says integer-valued)
        check("index written as 1.0,2.0,3.0 accepted",
              load_coords(tmp("1.0 9 9 9\n2.0 8 8 8\n3.0 7 7 7\n"), 3) == [[9, 9, 9], [8, 8, 8], [7, 7, 7]])

        # tiny-file min-N guard (index run must span >= 3 rows)
        for name, txt, dim, ai in [("N=1 dim cols col0=1.0", "1.0 0.0 0.0 0.0\n", 4, True),
                                   ("N=1 dim cols col0=0.0", "0.0 0.6 0.0 0.8\n", 4, True),
                                   ("N=2 dim cols col0=0.0,1.0", "0.0 0.6 0.8\n1.0 0.0 0.0\n", 3, True),
                                   ("N=2 dim+1 cols col0=1,2", "1 0.1 0.2 0.3\n2 0.4 0.5 0.6\n", 3, True),
                                   ("N=1 dim+1 cols col0=0", "0 0.1 0.2 0.3\n", 3, True),
                                   ("N=2 dim cols, allow_index=False", "0.0 0.6 0.8\n1.0 0.0 0.0\n", 3, False)]:
            ex = anomaly(tmp(txt), dim, allow_index=ai)
            check("small file %s -> ambiguous_small_file" % name, ex is not None and ex.kind == "ambiguous_small_file", ex)
        ex = anomaly(tmp("1 0.1 0.2 0.3\n2 0.4 0.5 0.6\n"), 3, allow_index=False)
        check("N=2 dim+1 cols allow_index=False stays dimension_mismatch", ex is not None and ex.kind == "dimension_mismatch", ex)
        check("small file with non-index col0 accepted (N=2)",
              load_coords(tmp("0.5 0.5 0.5\n-0.5 0.5 0.5\n"), 3) == [[D("0.5")] * 3, [D("-0.5"), D("0.5"), D("0.5")]])
        check("small file col0=2.0 (not a run start) accepted (N=1)", len(load_coords(tmp("2.0 0 0\n"), 3)) == 1)
        ex = anomaly(tmp("1 0 0 0 0\n2 1 0 0 0\n3 0 1 0 0\n"), 5)
        check("N=3 index run in dim columns still index_in_dim_columns", ex is not None and ex.kind == "index_in_dim_columns", ex)

        # '#' comment lines are skipped
        r = load_coords(tmp("# 0.1 0.2 0.3\n0.4 0.5 0.6\n   # 9 9 9\n0.7 0.8 0.9\n#\n#N=2\n"), 3)
        check("# comment lines skipped (not data, not label rows)", r == [[D("0.4"), D("0.5"), D("0.6")], [D("0.7"), D("0.8"), D("0.9")]], r)
        ex = anomaly(tmp("# 0.1 0.2 0.3\n# 1 2 3\n"), 3)
        check("comments-only file -> empty", ex is not None and ex.kind == "empty", ex)
        r = load_coords(tmp("# source: synthetic\n1 0 0 0\n# mid-file comment 7 8 9\n2 1 0 0\n3 0 1 0\n"), 3)
        check("comments do not break the file-wide index run", r == [[0, 0, 0], [1, 0, 0], [0, 1, 0]], r)
        r = load_coords(tmp("2\n# xyz comment line\nAr 0.5 0 0\nAr -0.5 1 1\n"), 3)
        check("xyz count line + '#' comment line", len(r) == 2, r)
        ex = anomaly(tmp("0.1 0.2 0.3 # trailing\n"), 3)
        check("trailing '#' after numbers is still mixed_tokens (only leading # is a comment)",
              ex is not None and ex.kind == "mixed_tokens", ex)

        # kind list
        check("CoordAnomaly kinds wired", set(coord_loader.KINDS) == {"dimension_mismatch", "mixed_tokens", "index_in_dim_columns", "empty",
                                                       "count_mismatch", "non_finite", "ambiguous_small_file"}, coord_loader.KINDS)
        # CCD *new.TXT-style index x y z, larger N, blank lines and header
        lines = ["  %d  %s  %s  %s" % (i + 1, "%.10f" % (i * 0.1), "-%.10f" % (i * 0.2), "%.10f" % (i * 0.3)) for i in range(38)]
        r = load_coords(tmp("index x y z\n\n" + "\n".join(lines) + "\n\n"), 3)
        check("CCD-style 38-atom index x y z", len(r) == 38 and str(r[37][0]) == "3.7000000000" and all(len(x) == 3 for x in r))
        # mixed widths dim/dim+1 -> dimension_mismatch
        ex = anomaly(tmp("1 0 0 0\n2 1 0 0\n0 1 0\n"), 3)
        check("mixed dim/dim+1 widths -> dimension_mismatch", ex is not None and ex.kind == "dimension_mismatch" and ex.lines == [3], ex)
        # rule 6 file-wide: index run holds overall, not per row
        ex = anomaly(tmp("0 1 1\n0.5 2 2\n2 3 3\n"), 3)
        check("partial run in dim columns is data (not index)", ex is None)
        # dim must be declared
        try:
            load_coords(tmp("0 0 0\n"), None)
            check("dim=None rejected", False)
        except ValueError:
            check("dim=None rejected", True)

        # opt-in trailing_radius (Packomania scu/ssp layout)
        pk = os.path.join(FX, "packomania_radius_layout.txt")
        r = load_coords(pk, 3, trailing_radius=True)
        check("trailing_radius=True: synthetic Packomania layout -> N=4, radius and index stripped, lossless",
              len(r) == 4 and all(len(x) == 3 for x in r) and format(r[0][0], "f") == "0.250000000000", r)
        ex = anomaly(pk, 3)
        check("trailing_radius default off: Packomania layout raises", ex is not None and ex.kind == "dimension_mismatch", ex)
        ex = anomaly(os.path.join(FX, "scu30_real_packomania.txt"), 3, trailing_radius=True)
        check("trailing_radius=True: real scu30 lone '30' line still raises",
              ex is not None and ex.kind == "dimension_mismatch" and ex.lines == [36], ex)
        ex = anomaly(tmp("0.25\n1 0.1 0.2 0.3 0.25\n2 0.4 0.5 0.6 0.25\n3 0.7 0.8 0.9 0.25\n4\n"), 3, trailing_radius=True)
        check("trailing_radius=True: synthetic lone trailing index raises", ex is not None and ex.kind == "dimension_mismatch" and ex.lines == [5], ex)
        ex = anomaly(tmp("0.25\n0.1 0.2 0.3 0.25\n0.4 0.5 0.6 0.25\n0.7 0.8 0.9 0.25\n4\n"), 3, trailing_radius=True)
        check("trailing_radius=True: lone integer after unindexed rows raises", ex is not None and ex.lines == [5], ex)
        ex = anomaly(tmp("0.25\n1 0.1 0.2 0.3 0.25\n2 0.4 0.5 0.6 0.26\n3 0.7 0.8 0.9 0.25\n"), 3, trailing_radius=True)
        check("trailing_radius=True: radius column != radius line raises", ex is not None and ex.lines == [3], ex)
        ex = anomaly(tmp("1 0.1 0.2 0.3 0.25\n2 0.4 0.5 0.6 0.25\n3 0.7 0.8 0.9 0.25\n"), 3, trailing_radius=True)
        check("trailing_radius=True: missing radius line raises", ex is not None and ex.lines == [1], ex)
        ex = anomaly(tmp("0.25\n1 0.1 0.2 0.3\n2 0.4 0.5 0.6\n3 0.7 0.8 0.9\n"), 3, trailing_radius=True)
        check("trailing_radius=True: rows without a radius column raise (never drop a coordinate)",
              ex is not None and ex.kind == "dimension_mismatch", ex)

        # CLI prints fixed-point digits, not '0E-12'
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = coord_loader._main([os.path.join(FX, "hsp4_true4d.txt"), "--dim", "4"])
        out = buf.getvalue()
        check("CLI keeps fixed-point digits (0.000000000000, no 0E-12)",
              rc == 0 and "0.000000000000" in out and "E-" not in out, out)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = coord_loader._main([pk, "--dim", "3", "--trailing-radius"])
        check("CLI --trailing-radius", rc == 0 and buf.getvalue().startswith("# N=4 dim=3"), buf.getvalue())

        self.assertEqual(len(results), 58)  # + 12 anomaly-attribute cases in PackTests = 70


if __name__ == "__main__":
    unittest.main()
