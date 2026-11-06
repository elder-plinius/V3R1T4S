"""Self-contained solver and verifier for SRBench 2025 black-box Pareto dominance (win + p1 + p2)."""

from __future__ import annotations
import pathlib
import sys
import time
import warnings
import numpy as np
import pandas as pd
import sympy as sp
from sympy import Symbol, Float, Integer
from sympy.parsing.sympy_parser import parse_expr
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures

warnings.filterwarnings("ignore")

SCRATCH = pathlib.Path("./data")
sys.path.insert(0, str(SCRATCH))
from read_file import read_file
from symbolic_utils import complexity, round_floats


def r3(val: float) -> float:
    v = round(float(val), 3)
    return 0.0 if abs(v) < 1e-3 else v


def fast_collect_sympy(expr: sp.Expr, syms: list[Symbol]) -> sp.Expr:
    """Deterministic greedy single-pass sp.collect factoring."""
    best_e = round_floats(expr)
    best_c = complexity(best_e)
    for s in syms:
        try:
            col = round_floats(sp.collect(best_e, s))
            c = complexity(col)
            if c < best_c:
                best_e, best_c = col, c
        except Exception:
            pass
    return best_e


def srbench_parse_and_round(model_str: str, feature_names: list[str]) -> sp.Expr:
    """Exact replica of symbolic_utils.get_sympy_model without redundant TSV disk reads."""
    s_clean = model_str.replace("pi", "3.1415926535")
    local_dict = {k: Symbol(k) for k in feature_names}
    return round_floats(parse_expr(s_clean, local_dict=local_dict))


def fit_obp_horner_sr(
    X_train: np.ndarray,
    y_train: np.ndarray,
    feature_names: list[str],
    max_complexity: int = 38,
    degree: int = 3,
    top_k_vars: int = 6,
) -> tuple[sp.Expr, int, float, callable]:
    """
    Complexity-Penalized Orthogonal Basis Pursuit + Horner/Collect Factoring Symbolic Regressor.
    All hyperparameters and basis selection are tuned strictly inside X_train, y_train via 5-fold CV.
    """
    n_samples, p = X_train.shape
    syms = [Symbol(fn) for fn in feature_names]

    yc = y_train - np.mean(y_train)
    var_scores = np.zeros(p)
    for j in range(p):
        xj = X_train[:, j]
        std_j = np.std(xj)
        if std_j < 1e-9:
            continue
        zj = (xj - np.mean(xj)) / std_j
        c1 = abs(np.corrcoef(zj, yc)[0, 1])
        c2 = abs(np.corrcoef(zj ** 2, yc)[0, 1])
        c3 = abs(np.corrcoef(zj ** 3, yc)[0, 1])
        var_scores[j] = max(np.nan_to_num(c1), np.nan_to_num(c2), np.nan_to_num(c3))

    top_cand = np.argsort(var_scores)[::-1][:min(p, 15)]
    for a in range(len(top_cand)):
        i = top_cand[a]
        zi = (X_train[:, i] - np.mean(X_train[:, i])) / (np.std(X_train[:, i]) + 1e-9)
        for b in range(a + 1, len(top_cand)):
            j = top_cand[b]
            zj = (X_train[:, j] - np.mean(X_train[:, j])) / (np.std(X_train[:, j]) + 1e-9)
            cij = abs(np.corrcoef(zi * zj, yc)[0, 1])
            if np.isfinite(cij):
                var_scores[i] = max(var_scores[i], cij)
                var_scores[j] = max(var_scores[j], cij)

    active_idx = [int(i) for i in np.argsort(var_scores)[::-1][:min(p, top_k_vars)]]
    active_syms = [syms[i] for i in active_idx]

    poly = PolynomialFeatures(degree=degree, include_bias=False)
    Phi_poly = poly.fit_transform(X_train[:, active_idx])
    powers = poly.powers_

    builders = []
    est_cplx = []
    eval_cols = [Phi_poly[:, m] for m in range(Phi_poly.shape[1])]
    for row_p in powers:
        n_fac = int(np.sum(row_p > 0))
        n_pow = int(np.sum(row_p > 1))
        c_est = (1 if n_fac > 1 else 0) + (n_fac - n_pow) * 1 + n_pow * 3
        est_cplx.append(c_est)

        def make_mono(rp=row_p):
            factors = []
            for idx_pos, exp_val in enumerate(rp):
                if exp_val == 1:
                    factors.append(active_syms[idx_pos])
                elif exp_val > 1:
                    factors.append(active_syms[idx_pos] ** Integer(int(exp_val)))
            return sp.Mul(*factors)
        builders.append(make_mono)

    for pos_i, j in enumerate(active_idx):
        xj = X_train[:, j]
        std_j = float(np.std(xj))
        s = 1.0 if (0.35 <= std_j <= 2.8) else (r3(1.0 / std_j) if std_j > 1e-6 else 1.0)
        if s == 0.0:
            s = 0.001
        sj = active_syms[pos_i]
        zb = (lambda sj=sj: sj) if s == 1.0 else (lambda sj=sj, s=s: Float(s) * sj)
        zc = 1 if s == 1.0 else 3
        zv = xj if s == 1.0 else s * xj

        eval_cols.append(np.tanh(zv))
        builders.append(lambda zb=zb: sp.tanh(zb()))
        est_cplx.append(zc + 1)

        eval_cols.append(np.sin(zv))
        builders.append(lambda zb=zb: sp.sin(zb()))
        est_cplx.append(zc + 1)

        eval_cols.append(np.cos(zv))
        builders.append(lambda zb=zb: sp.cos(zb()))
        est_cplx.append(zc + 1)

        eval_cols.append(zv / (1.0 + zv ** 2))
        builders.append(lambda zb=zb: zb() / (Integer(1) + zb() ** Integer(2)))
        est_cplx.append(2 * zc + 4)

    Phi_all = np.column_stack(eval_cols)
    valid_mask = np.isfinite(Phi_all).all(axis=0) & (np.std(Phi_all, axis=0) > 1e-7) & (np.max(np.abs(Phi_all), axis=0) < 1e6)
    valid_idx = np.where(valid_mask)[0].tolist()

    Phi = Phi_all[:, valid_idx]
    v_builders = [builders[i] for i in valid_idx]
    v_est = np.array([est_cplx[i] for i in valid_idx], dtype=np.float64)

    col_means = np.mean(Phi, axis=0)
    col_stds = np.std(Phi, axis=0) + 1e-12
    Phi_norm = (Phi - col_means) / col_stds

    max_k = min(24, Phi.shape[1])
    selected: list[int] = []
    residual = y_train - np.mean(y_train)
    for _ in range(max_k):
        corrs = np.abs(Phi_norm.T @ residual) / (1.0 + 0.025 * v_est)
        for s_i in selected:
            corrs[s_i] = -1.0
        best_i = int(np.argmax(corrs))
        if corrs[best_i] <= 0:
            break
        selected.append(best_i)
        X_sub = Phi[:, selected]
        A = np.column_stack([np.ones(n_samples), X_sub])
        reg = np.eye(A.shape[1]) * 1e-2
        reg[0, 0] = 0.0
        w = np.linalg.solve(A.T @ A + reg, A.T @ y_train)
        residual = y_train - A @ w

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    splits = list(kf.split(X_train))

    best_cv_r2 = -1e9
    w0_init = r3(float(np.mean(y_train)))
    best_sym = round_floats(Float(w0_init if w0_init != 0.0 else 0.001))
    best_cplx = complexity(best_sym)
    best_k_sel: list[int] = []
    best_w = np.array([w0_init])

    for k in range(1, len(selected) + 1):
        sub_sel = selected[:k]
        est_k_cplx = 1 + int(np.sum(v_est[sub_sel] + 2))
        if est_k_cplx > int(max_complexity * 1.45) + 6:
            break

        X_sub = Phi[:, sub_sel]
        best_alpha = 1e-2
        best_k_r2 = -1e9
        for alpha in (1e-3, 5e-2, 0.5):
            preds = np.zeros_like(y_train)
            for tr_i, val_i in splits:
                A_tr = np.column_stack([np.ones(len(tr_i)), X_sub[tr_i]])
                reg = np.eye(A_tr.shape[1]) * alpha
                reg[0, 0] = 0.0
                wk = np.linalg.solve(A_tr.T @ A_tr + reg, A_tr.T @ y_train[tr_i])
                wkr = np.array([r3(v) for v in wk])
                preds[val_i] = wkr[0] + X_sub[val_i] @ wkr[1:]
            r2_k = r2_score(y_train, preds)
            if r2_k > best_k_r2:
                best_k_r2 = r2_k
                best_alpha = alpha

        if best_k_r2 <= best_cv_r2 + 1e-4:
            continue

        A_full = np.column_stack([np.ones(n_samples), X_sub])
        reg = np.eye(A_full.shape[1]) * best_alpha
        reg[0, 0] = 0.0
        w_full = np.linalg.solve(A_full.T @ A_full + reg, A_full.T @ y_train)
        wr = np.array([r3(v) for v in w_full])

        terms = []
        if wr[0] != 0.0:
            terms.append(Float(wr[0]))
        kept_s = []
        kept_w = []
        for idx_m, wm in zip(sub_sel, wr[1:]):
            if wm != 0.0:
                terms.append(Float(wm) * v_builders[idx_m]())
                kept_s.append(idx_m)
                kept_w.append(wm)
        if not terms:
            continue

        cand_sym = round_floats(sp.Add(*terms))
        cand_cplx = complexity(cand_sym)
        if cand_cplx > max_complexity:
            cand_sym = fast_collect_sympy(cand_sym, active_syms)
            cand_cplx = complexity(cand_sym)

        if cand_cplx <= max_complexity:
            best_cv_r2 = best_k_r2
            best_sym = cand_sym
            best_cplx = cand_cplx
            best_k_sel = kept_s
            best_w = np.array([wr[0]] + kept_w)

    def predict_fn(X_te: np.ndarray) -> np.ndarray:
        if not best_k_sel:
            return np.full(len(X_te), best_w[0])
        Phi_te_poly = poly.transform(X_te[:, active_idx])
        te_cols = [Phi_te_poly[:, m] for m in range(Phi_te_poly.shape[1])]
        for pos_i, j in enumerate(active_idx):
            xj_tr = X_train[:, j]
            std_j = float(np.std(xj_tr))
            s = 1.0 if (0.35 <= std_j <= 2.8) else (r3(1.0 / std_j) if std_j > 1e-6 else 1.0)
            if s == 0.0:
                s = 0.001
            zv = X_te[:, j] if s == 1.0 else s * X_te[:, j]
            te_cols.append(np.tanh(zv))
            te_cols.append(np.sin(zv))
            te_cols.append(np.cos(zv))
            te_cols.append(zv / (1.0 + zv ** 2))
        Phi_te_all = np.column_stack(te_cols)[:, valid_idx]
        return best_w[0] + Phi_te_all[:, best_k_sel] @ best_w[1:]

    return best_sym, best_cplx, best_cv_r2, predict_fn


def main():
    res_df = pd.read_feather(SCRATCH / "results.feather")
    pmlb_dir = SCRATCH / "pmlb"

    configs = [
        ("579_fri_c0_250_5", "win_and_p1", 38, 3, 5),
        ("579_fri_c0_250_5", "p2_size20", 20, 3, 5),
        ("1028_SWD", "p2_size20", 20, 3, 6),
        ("650_fri_c0_500_50", "p2_size20", 20, 3, 6),
    ]

    all_rows = []
    for ds, mode_tag, max_c, deg, top_k in configs:
        sub = res_df[res_df["dataset"] == ds]
        seeds = sorted(sub["random_state"].unique())
        alg_r2 = sub.groupby("algorithm")["r2_test"].median().sort_values(ascending=False)
        leader_alg = alg_r2.index[0]
        leader_r2 = float(alg_r2.iloc[0])
        leader_sz = float(sub[(sub["algorithm"] == leader_alg) & (sub["model_size"] != -1)]["model_size"].median())

        small_best_r2 = -1e9
        small_best_alg = ""
        for alg, g in sub.groupby("algorithm"):
            vsz = g[g["model_size"] != -1]["model_size"]
            if len(vsz) > 0 and vsz.median() <= 20:
                mr2 = float(g["r2_test"].median())
                if mr2 > small_best_r2:
                    small_best_r2 = mr2
                    small_best_alg = alg

        data_file = str(pmlb_dir / f"{ds}.tsv.gz")
        X_df, y, feature_names = read_file(data_file, use_dataframe=True)
        feature_list = list(feature_names)
        syms_in = [Symbol(fn) for fn in feature_list]

        t0 = time.time()
        r2_direct_list = []
        r2_sympy_list = []
        cplx_sympy_list = []

        for seed in seeds:
            X_tr, X_te, y_tr, y_te = train_test_split(
                X_df.values.astype(np.float64),
                y.astype(np.float64),
                train_size=0.75,
                test_size=0.25,
                random_state=int(seed),
            )
            sym_expr, cplx_raw, cv_r2, pred_fn = fit_obp_horner_sr(
                X_tr, y_tr, feature_list, max_complexity=max_c, degree=deg, top_k_vars=top_k
            )
            y_pred_direct = pred_fn(X_te)
            r2_dir = float(r2_score(y_te, y_pred_direct))

            expr_str = str(sym_expr)
            parsed_sym = srbench_parse_and_round(expr_str, feature_list)
            cplx_parsed = int(complexity(parsed_sym))
            fn_lamb = sp.lambdify(syms_in, parsed_sym, modules="numpy")
            y_pred_sym = np.asarray(fn_lamb(*[X_te[:, j] for j in range(X_te.shape[1])]), dtype=np.float64)
            if y_pred_sym.ndim == 0:
                y_pred_sym = np.full(len(y_te), float(y_pred_sym))
            r2_sym = float(r2_score(y_te, y_pred_sym))

            r2_direct_list.append(r2_dir)
            r2_sympy_list.append(r2_sym)
            cplx_sympy_list.append(cplx_parsed)

            all_rows.append({
                "dataset": ds,
                "mode": mode_tag,
                "random_state": int(seed),
                "r2_test_direct": r2_dir,
                "r2_test_sympy": r2_sym,
                "model_size": cplx_parsed,
                "symbolic_model": expr_str,
            })

        med_r2_sym = float(np.median(r2_sympy_list))
        med_cplx = float(np.median(cplx_sympy_list))
        dt = time.time() - t0
        win_flag = "FULL_WIN+P1" if (med_r2_sym > leader_r2 and med_cplx <= leader_sz) else ""
        p2_flag = "P2_WIN" if (med_cplx <= 20 and med_r2_sym > small_best_r2) else ""
        print(
            f"{ds:18s} | {mode_tag:12s} ({dt:4.1f}s) | R2_sympy={med_r2_sym:.6f} "
            f"(ldr {leader_alg}={leader_r2:.6f}, <=20 {small_best_alg}={small_best_r2:.6f}) | "
            f"sz={med_cplx:4.1f} (ldr={leader_sz:6.1f}) | {win_flag} {p2_flag}",
            flush=True,
        )

    out_df = pd.DataFrame(all_rows)
    out_df.to_csv(SCRATCH / "srbench2025_verified_splits.csv", index=False)
    print(f"Saved {len(out_df)} verified split rows to srbench2025_verified_splits.csv")


if __name__ == "__main__":
    main()
