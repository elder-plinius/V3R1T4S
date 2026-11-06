#!/usr/bin/env python3
"""Standalone pure-stdlib verifier for SRBench 2025 black-box Pareto dominance (win + p1 + p2)."""

import ast
import csv
import gzip
import json
import math
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OBJ_CSV = ROOT / "object" / "srbench2025_verified_splits.csv"
DATA_DIR = ROOT / "verify-it-yourself" / "data"
REF_JSON = DATA_DIR / "srbench_reference_splits.json"


def eval_expr_row(code_obj, var_map):
    env = {
        "sin": math.sin,
        "cos": math.cos,
        "tanh": math.tanh,
    }
    env.update(var_map)
    return float(eval(code_obj, {"__builtins__": {}}, env))


def sympy_equiv_complexity_stdlib(expr_str: str) -> int:
    """Compute exact SymPy preorder traversal AST node count (symbolic_utils.complexity)
    using only the Python standard library `ast` module."""
    tree = ast.parse(expr_str, mode="eval").body

    def to_sym(node):
        if isinstance(node, ast.Constant):
            val = float(node.value)
            if val == 0.0:
                return ("Zero", ())
            return ("Num", ())
        if isinstance(node, ast.Name):
            return ("Sym", (node.id,))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            if isinstance(node.operand, ast.Constant):
                return ("Num", ())
            return ("Mul", (("Num", ()), to_sym(node.operand)))
        if isinstance(node, ast.Call):
            return ("Func", (to_sym(node.args[0]),))
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, (ast.Add, ast.Sub)):
                terms = []

                def collect_add(n, neg=False):
                    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
                        collect_add(n.left, neg)
                        collect_add(n.right, neg)
                    elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Sub):
                        collect_add(n.left, neg)
                        collect_add(n.right, not neg)
                    else:
                        t = to_sym(n)
                        if t[0] == "Zero":
                            return
                        if neg:
                            if t[0] == "Num":
                                terms.append(("Num", ()))
                            elif t[0] == "Mul":
                                ch = list(t[1])
                                if any(c[0] == "Num" for c in ch):
                                    terms.append(("Mul", tuple(ch)))
                                else:
                                    terms.append(("Mul", tuple([("Num", ())] + ch)))
                            else:
                                terms.append(("Mul", (("Num", ()), t)))
                        else:
                            terms.append(t)

                collect_add(node, False)
                return ("Add", tuple(terms))
            if isinstance(node.op, ast.Mult):
                factors = []

                def collect_mul(n):
                    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult):
                        collect_mul(n.left)
                        collect_mul(n.right)
                    else:
                        factors.append(to_sym(n))

                collect_mul(node)
                return ("Mul", tuple(factors))
            if isinstance(node.op, ast.Div):
                num = to_sym(node.left)
                den = to_sym(node.right)
                inv = ("Pow", (den, ("Num", ())))
                if num[0] == "Mul":
                    return ("Mul", tuple(list(num[1]) + [inv]))
                return ("Mul", (num, inv))
            if isinstance(node.op, ast.Pow):
                return ("Pow", (to_sym(node.left), to_sym(node.right)))
        raise ValueError(f"Unsupported AST node: {type(node)}")

    sym_tree = to_sym(tree)

    def count_nodes(t):
        kind, children = t
        if kind in ("Num", "Zero", "Sym"):
            return 1
        return 1 + sum(count_nodes(c) for c in children)

    return count_nodes(sym_tree)


def load_tsv_gz(path: pathlib.Path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        raw_header = next(reader)
        header = [c.strip().replace(".", "_") for c in raw_header]
        feat_names = [c for c in header if c != "target"]
        t_idx = header.index("target")
        f_idxs = [header.index(c) for c in feat_names]
        X_rows = []
        y_vals = []
        for row in reader:
            X_rows.append([float(row[i]) for i in f_idxs])
            y_vals.append(float(row[t_idx]))
    return feat_names, X_rows, y_vals


def r2_score_stdlib(y_true, y_pred):
    n = len(y_true)
    mean_y = sum(y_true) / n
    ss_tot = sum((y - mean_y) ** 2 for y in y_true)
    ss_res = sum((y - yp) ** 2 for y, yp in zip(y_true, y_pred))
    return 1.0 - (ss_res / ss_tot)


def main() -> int:
    if not OBJ_CSV.is_file() or not REF_JSON.is_file():
        print("FAIL")
        return 1

    ref = json.loads(REF_JSON.read_text(encoding="utf-8"))
    expected_rows = ref["expected_rows"]

    try:
        with OBJ_CSV.open("r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception:
        print("FAIL")
        return 1

    if len(rows) != len(expected_rows):
        print("FAIL")
        return 1

    tsv_cache = {}
    grouped = {}

    for row, exp in zip(rows, expected_rows):
        try:
            ds = row["dataset"]
            mode = row["mode"]
            seed = int(row["random_state"])
            r2_dir = float(row["r2_test_direct"])
            r2_sym = float(row["r2_test_sympy"])
            msz = int(row["model_size"])
            expr_str = row["symbolic_model"]
        except Exception:
            print("FAIL")
            return 1

        if (
            ds != exp["dataset"]
            or mode != exp["mode"]
            or seed != exp["random_state"]
            or msz != exp["model_size"]
            or abs(r2_dir - exp["r2_test_direct"]) > 1e-9
            or abs(r2_sym - exp["r2_test_sympy"]) > 1e-9
        ):
            print("FAIL")
            return 1

        if ds not in tsv_cache:
            tsv_cache[ds] = load_tsv_gz(DATA_DIR / f"{ds}.tsv.gz")
        feat_names, X_rows, y_vals = tsv_cache[ds]
        te_indices = ref["datasets"][ds]["test_indices"][str(seed)]

        try:
            recomp_cplx = sympy_equiv_complexity_stdlib(expr_str)
            tree = ast.parse(expr_str, mode="eval")
            code_obj = compile(tree, "<expr>", "eval")
            y_true = [y_vals[i] for i in te_indices]
            y_pred = []
            for i in te_indices:
                vmap = {fn: X_rows[i][j] for j, fn in enumerate(feat_names)}
                y_pred.append(eval_expr_row(code_obj, vmap))
            recomp_r2 = r2_score_stdlib(y_true, y_pred)
        except Exception:
            print("FAIL")
            return 1

        if recomp_cplx != msz or abs(recomp_r2 - r2_sym) > 1e-7:
            print("FAIL")
            return 1

        grouped.setdefault((ds, mode), []).append((r2_sym, recomp_cplx))

    # Verify target win and p1/p2 criteria
    # 1. 579_fri_c0_250_5 win_and_p1: median R2 > leader_r2_median AND median size <= leader_model_size_median
    g_win = grouped.get(("579_fri_c0_250_5", "win_and_p1"), [])
    ds_579 = ref["datasets"]["579_fri_c0_250_5"]
    med_r2_win = statistics.median([x[0] for x in g_win])
    med_sz_win = statistics.median([x[1] for x in g_win])
    if not (len(g_win) == 30 and med_r2_win > ds_579["leader_r2_median"] and med_sz_win <= ds_579["leader_model_size_median"]):
        print("FAIL")
        return 1

    # 2. p2_size20 across all 3 datasets: median size <= 20 AND median R2 > small20_best_r2_median
    for ds_name in ("579_fri_c0_250_5", "1028_SWD", "650_fri_c0_500_50"):
        g_p2 = grouped.get((ds_name, "p2_size20"), [])
        ds_info = ref["datasets"][ds_name]
        med_r2_p2 = statistics.median([x[0] for x in g_p2])
        med_sz_p2 = statistics.median([x[1] for x in g_p2])
        if not (len(g_p2) == 30 and med_sz_p2 <= 20.0 and med_r2_p2 > ds_info["small20_best_r2_median"]):
            print("FAIL")
            return 1

    print(f"Verified 120 SRBench splits: 579_fri_c0_250_5 median R2={med_r2_win:.6f} > {ds_579['leader_r2_median']:.6f} at size {med_sz_win:.1f} <= {ds_579['leader_model_size_median']:.1f}")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
