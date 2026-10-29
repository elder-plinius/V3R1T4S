# SPDX-License-Identifier: AGPL-3.0-or-later
"""Unit tests for kit/derivation_check.py on synthetic point sets.

    python3 kit/tests/test_derivation_check.py        (standard library only)
"""
import io, math, os, random, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import derivation_check as dc  # noqa: E402


def spread(n, d, seed, rmin):
    """n points in [-0.5, 0.5]^d at pairwise distance >= rmin (rejection sampling)."""
    rng = random.Random(seed)
    pts = []
    while len(pts) < n:
        p = tuple(rng.uniform(-0.5, 0.5) for _ in range(d))
        if all(dc.dist(p, q) >= rmin for q in pts):
            pts.append(p)
    return pts


def ball_spread(n, d, seed, rmin):
    rng = random.Random(seed)
    pts = []
    while len(pts) < n:
        p = tuple(rng.uniform(-1, 1) for _ in range(d))
        if sum(v * v for v in p) <= 1 and all(dc.dist(p, q) >= rmin for q in pts):
            pts.append(p)
    return pts


def rotation(d, seed):
    """A random orthogonal d x d matrix (Gram-Schmidt on random vectors)."""
    rng = random.Random(seed)
    basis = []
    while len(basis) < d:
        v = [rng.gauss(0, 1) for _ in range(d)]
        for b in basis:
            c = sum(x * y for x, y in zip(v, b))
            v = [x - c * y for x, y in zip(v, b)]
        n = math.sqrt(sum(x * x for x in v))
        if n > 1e-6:
            basis.append([x / n for x in v])
    return basis


def rotate(pts, m):
    return [tuple(sum(m[i][k] * p[k] for k in range(len(p))) for i in range(len(m))) for p in pts]


class Files(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def write(self, name, pts, header="0.05\n# coordinates\n", index=False):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as f:
            f.write(header)
            for i, p in enumerate(pts, 1):
                f.write(("%4d " % i if index else "") + " ".join("%.15f" % v for v in p) + "\n")
        return path

    def run_check(self, claim, refs, **kw):
        out = io.StringIO()
        flags = dc.check(claim, refs, out=out, **kw)
        return flags, out.getvalue()


class ParseTests(Files):
    def test_reads_packomania_layout(self):
        pts = spread(20, 3, 1, 0.1)
        p = self.write("a.txt", pts, index=True)
        self.assertEqual(dc.guess_dim(p), 3)
        got = dc.read_points(p, 3)
        self.assertEqual(len(got), 20)
        self.assertAlmostEqual(got[5][2], pts[5][2], places=12)

    def test_reads_index_coordinates_radius_layout(self):
        pts = spread(12, 3, 9, 0.1)
        path = os.path.join(self.tmp, "c.txt")
        with open(path, "w") as f:
            f.write("0.065851831431\n#\n#   x-coord   y-coord   z-coord   radius\n")
            for i, q in enumerate(pts, 1):
                f.write("%4d  %.12f  %.12f  %.12f   0.065851831431\n" % ((i,) + q))
        self.assertEqual(dc.guess_dim(path), 3)
        got = dc.read_points(path, 3)
        self.assertEqual(len(got), 12)
        self.assertAlmostEqual(got[3][0], pts[3][0], places=11)

    def test_reads_plain_layout(self):
        p = self.write("b.txt", spread(15, 4, 2, 0.2), header="")
        self.assertEqual(dc.guess_dim(p), 4)
        self.assertEqual(len(dc.read_points(p, 4)), 15)

    def test_min_distance_matches_brute_force(self):
        pts = spread(60, 3, 3, 0.08)
        brute = min(dc.dist(p, q) for i, p in enumerate(pts) for q in pts[i + 1:])
        self.assertAlmostEqual(dc.min_distance(pts), brute, places=12)


class FlagTests(Files):
    def setUp(self):
        super().setUp()
        self.ref_pts = spread(80, 3, 10, 0.12)
        self.ref = self.write("ref.txt", self.ref_pts, index=True)

    def test_deletion_is_flagged(self):
        claim = self.write("del.txt", self.ref_pts[:40] + self.ref_pts[43:])
        flags, text = self.run_check(claim, [self.ref])
        self.assertEqual(len(flags), 1, text)
        self.assertIn("deletion-like", flags[0][1])

    def test_insertion_is_flagged(self):
        extra = (0.4999, 0.4999, 0.4999)
        claim = self.write("ins.txt", self.ref_pts + [extra])
        flags, text = self.run_check(claim, [self.ref])
        self.assertEqual(len(flags), 1, text)
        self.assertIn("insertion-like", flags[0][1])

    def test_polished_copy_is_flagged(self):
        rng = random.Random(4)
        moved = [tuple(v + rng.uniform(-1e-4, 1e-4) for v in p) for p in self.ref_pts]
        flags, text = self.run_check(self.write("pol.txt", moved), [self.ref])
        self.assertEqual(len(flags), 1, text)
        self.assertIn("copy-like", flags[0][1])

    def test_symmetric_copy_is_flagged_and_named(self):
        sym = ((1, 0, 2), (-1, 1, -1))
        flags, text = self.run_check(self.write("sym.txt", [dc.apply(sym, p) for p in self.ref_pts]), [self.ref])
        self.assertEqual(len(flags), 1, text)
        self.assertIn("box symmetry", text)

    def test_rescaled_shifted_copy_is_flagged(self):
        moved = [tuple(0.9 * v + 0.5 for v in p) for p in self.ref_pts]   # e.g. coordinates in [0, 1]
        flags, text = self.run_check(self.write("res.txt", moved), [self.ref])
        self.assertEqual(len(flags), 1, text)
        self.assertIn("bounding box", text)

    def test_unrelated_configuration_is_not_flagged(self):
        flags, text = self.run_check(self.write("new.txt", spread(80, 3, 99, 0.12)), [self.ref])
        self.assertEqual(flags, [], text)
        self.assertTrue(text.rstrip().endswith("DERIVATION_CHECK: NONE"))

    def test_only_the_matching_reference_is_flagged(self):
        other = self.write("other.txt", spread(83, 3, 77, 0.12))
        claim = self.write("del2.txt", self.ref_pts[:-2])
        flags, text = self.run_check(claim, [other, self.ref])
        self.assertEqual([f[0] for f in flags], [self.ref], text)


class BallTests(Files):
    def test_rotated_copy_in_a_ball_is_flagged(self):
        pts = ball_spread(40, 4, 5, 0.3)
        ref = self.write("ball.txt", pts, index=True)
        claim = self.write("rot.txt", rotate(pts, rotation(4, 6)))
        flags, text = self.run_check(claim, [ref], container="ball")
        self.assertEqual(len(flags), 1, text)
        self.assertIn("copy-like", flags[0][1])
        self.assertIn("rotation or reflection about the origin", text)

    def test_isometry_test_still_flags_a_rotated_copy_without_the_search(self):
        pts = ball_spread(40, 4, 5, 0.3)
        ref = self.write("ball.txt", pts, index=True)
        claim = self.write("rot.txt", rotate(pts, rotation(4, 6)))
        flags, text = self.run_check(claim, [ref], container="ball", rotation_budget=0)
        self.assertEqual(len(flags), 1, text)
        self.assertIn("isometric copy", flags[0][1])

    def test_rotated_and_moved_ball_copy_is_flagged_by_the_rotation_search(self):
        pts = ball_spread(40, 4, 12, 0.3)
        rng = random.Random(13)
        moved = rotate([tuple(v + rng.uniform(-1e-3, 1e-3) for v in p) for p in pts], rotation(4, 14))
        claim, ref = self.write("pb.txt", moved), self.write("pa.txt", pts)
        flags, text = self.run_check(claim, [ref], container="ball")
        self.assertEqual(len(flags), 1, text)
        self.assertIn("copy-like", flags[0][1])
        # without the search this is the documented blind spot: moved by more than --iso-tol
        flags, text = self.run_check(claim, [ref], container="ball", rotation_budget=0)
        self.assertEqual(flags, [], text)

    def test_rotated_deletion_and_insertion_in_a_ball_are_flagged(self):
        pts = ball_spread(60, 4, 21, 0.25)
        rng = random.Random(22)
        m = rotation(4, 23)
        ref = self.write("full.txt", pts, index=True)
        part = rotate([tuple(v + rng.uniform(-1e-3, 1e-3) for v in p) for p in pts[:30] + pts[32:]], m)
        flags, text = self.run_check(self.write("del.txt", part), [ref], container="ball")
        self.assertEqual(len(flags), 1, text)
        self.assertIn("deletion-like", flags[0][1])
        flags, text = self.run_check(ref, [self.write("small.txt", part)], container="ball")
        self.assertEqual(len(flags), 1, text)
        self.assertIn("insertion-like", flags[0][1])

    def test_rotated_copy_in_a_disk_is_flagged(self):
        pts = ball_spread(150, 2, 31, 0.1)
        rng = random.Random(32)
        moved = rotate([tuple(v + rng.uniform(-5e-4, 5e-4) for v in p) for p in pts], rotation(2, 33))
        flags, text = self.run_check(self.write("d2.txt", moved), [self.write("d1.txt", pts)], container="ball")
        self.assertEqual(len(flags), 1, text)
        self.assertIn("copy-like", flags[0][1])

    def test_different_ball_configuration_is_not_flagged(self):
        ref = self.write("ball1.txt", ball_spread(40, 4, 7, 0.3))
        claim = self.write("ball2.txt", ball_spread(40, 4, 8, 0.3))
        flags, text = self.run_check(claim, [ref], container="ball")
        self.assertEqual(flags, [], text)

    def test_box_container_does_not_search_rotations(self):
        pts = ball_spread(40, 3, 41, 0.25)
        claim = self.write("r3.txt", rotate(pts, rotation(3, 42)))
        flags, text = self.run_check(claim, [self.write("p3.txt", pts)], container="box")
        self.assertNotIn("rotation or reflection", text)


class CliTests(Files):
    def test_cli_last_line_and_strict_exit(self):
        pts = spread(30, 2, 11, 0.15)
        ref = self.write("r2.txt", pts, index=True)
        claim = self.write("c2.txt", pts[1:])
        script = os.path.join(os.path.dirname(HERE), "derivation_check.py")
        r = subprocess.run([sys.executable, script, claim, ref], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(r.stdout.rstrip().endswith("DERIVATION_CHECK: FLAG (1)"), r.stdout)
        r = subprocess.run([sys.executable, script, claim, ref, "--strict"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
