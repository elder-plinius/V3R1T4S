import os
import sys
import unittest
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import propagated_bar as pb  # noqa: E402


class PropagatedBarTests(unittest.TestCase):
    def test_monotone_table_has_no_free_cells(self):
        rows = pb.parse_table("1 0.5\n2 0.25\n3 0.2\n4 0.1\n")
        self.assertEqual(pb.free_cells(rows, "down", "1e-10"), [])

    def test_single_planted_inversion_is_found(self):
        rows = pb.parse_table("1 0.5\n2 0.25\n3 0.2\n4 0.21\n5 0.1\n")
        self.assertEqual([(n, s) for n, s, _ in pb.free_cells(rows, "down", "1e-10")], [(3, 4)])

    def test_ties_and_margin_boundary(self):
        rows = pb.parse_table("1 0.3\n2 0.3\n3 0.3000000001\n")
        self.assertEqual([(n, s) for n, s, _ in pb.free_cells(rows, "down", "1e-10")], [(1, 3), (2, 3)])
        self.assertEqual(pb.free_cells(rows, "down", "2e-10"), [])

    def test_exact_comparison_beyond_float_precision(self):
        rows = pb.parse_table("10 0.058531064606729197904556991356\n11 0.058531064606729197904556991357\n")
        fc = pb.free_cells(rows, "down", "1e-31")
        self.assertEqual([(n, s) for n, s, _ in fc], [(10, 11)])
        self.assertEqual(fc[0][2], Fraction(1, 10**30))

    def test_up_direction_for_sum_of_radii(self):
        rows = pb.parse_table("1 0.5\n2 0.8\n3 0.7\n4 0.9\n")
        self.assertEqual([(n, s) for n, s, _ in pb.free_cells(rows, "up", "1e-11")], [(3, 2)])
        self.assertEqual(pb.free_cells(pb.parse_table("1 0.5\n2 0.6\n3 0.7\n"), "up", "1e-11"), [])

    def test_parser_ignores_headers_blank_lines_and_crlf(self):
        rows = pb.parse_table("N radius\r\n\r\n1\t0.5\r\n2\t0.25 extra\r\n# 3 0.9\r\n")
        self.assertEqual(sorted(rows), [1, 2])

    def test_bar_names_its_source(self):
        rows = pb.parse_table("7 0.1\n8 0.12\n9 0.11\n")
        bars = pb.propagated(rows, "down")
        self.assertEqual(bars[7][1], 8)
        self.assertEqual(bars[9][1], 9)

    def test_cli_reports_a_free_cell(self):
        import io
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("1 0.5\n2 0.2\n3 0.21\n")
            path = f.name
        try:
            out = io.StringIO()
            old, sys.stdout = sys.stdout, out
            try:
                rc = pb.main([path, "--n", "2", "--margin", "1e-10"])
            finally:
                sys.stdout = old
            self.assertEqual(rc, 0)
            self.assertIn("FREE", out.getvalue())
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
