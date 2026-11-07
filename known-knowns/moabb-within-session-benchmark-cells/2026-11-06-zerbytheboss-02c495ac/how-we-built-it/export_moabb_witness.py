#!/usr/bin/env python3
"""Rebuild object/moabb_ssvep_within_session_cells.csv and verify-it-yourself/data/moabb_ssvep_fold_witness.json.gz."""

import csv
import gzip
import hashlib
import json
import os
import time
import mne
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from pyriemann.estimation import Covariances
from pyriemann.classification import MDM
from pyriemann.tangentspace import TangentSpace
from moabb.datasets import Kalunga2016, Nakanishi2015, MAMEM3
from moabb.paradigms import SSVEP, FilterBankSSVEP
from moabb.pipelines.features import ExtendedSSVEPSignal

from fb_htr_ssvep import FBHTRSSVEPClassifier, _batch_corr_1d


def eval_baseline_fold(cov_sub, y_enc, tr, te):
    cov_tr = cov_sub[tr]
    cov_te = cov_sub[te]
    mdm = MDM()
    mdm.fit(cov_tr, y_enc[tr])
    pred_mdm = mdm.predict(cov_te).tolist()

    ts = TangentSpace()
    S_tr = ts.fit_transform(cov_tr, y_enc[tr])
    S_te = ts.transform(cov_te)
    lr = LogisticRegression(solver="lbfgs")
    lr.fit(S_tr, y_enc[tr])
    pred_ts_lr = lr.predict(S_te).tolist()
    return pred_mdm, pred_ts_lr


def qr_factor_clf(clf_lr, Z_te):
    W = clf_lr.coef_
    b = clf_lr.intercept_
    Q_W, R_W = np.linalg.qr(W.T, mode="reduced")
    U_te = Z_te @ Q_W
    logits = U_te @ R_W + b
    logits_shift = logits - np.max(logits, axis=1, keepdims=True)
    exp_l = np.exp(logits_shift)
    probs = exp_l / np.sum(exp_l, axis=1, keepdims=True)
    probs_sk = clf_lr.predict_proba(Z_te)
    max_diff = float(np.max(np.abs(probs - probs_sk)))
    assert max_diff < 1e-11, f"Proba mismatch: {max_diff}"
    return {
        "U_te": [[round(float(x), 10) for x in row] for row in U_te],
        "R_W": [[round(float(x), 10) for x in row] for row in R_W],
        "b": [round(float(x), 10) for x in b],
    }, probs


def extract_projected_test_views(clf, X_te_epochs):
    X_data = X_te_epochs.get_data()
    ts_te, extra_te, R_f_te, _ = clf._extract_unsupervised_batch(
        X_data, clf.sfreq_, clf.slen_, clf.stim_freqs_
    )
    n_te, C, T = X_data.shape
    X_te_c = X_data - X_data.mean(axis=-1, keepdims=True)
    flat_te = X_te_c.reshape(n_te, C * T)
    n_classes = len(clf.classes_)
    tmpl_te = np.zeros((n_te, n_classes * 2))
    for c_idx, (w, proj_mean, flat_mean) in enumerate(clf.template_filters_):
        proj_te = np.tensordot(X_te_c, w, axes=([1], [0]))
        tmpl_te[:, c_idx * 2] = _batch_corr_1d(proj_te, proj_mean[None, :])
        tmpl_te[:, c_idx * 2 + 1] = _batch_corr_1d(flat_te, flat_mean)

    ssd_cols = []
    for f in clf.stim_freqs_:
        R_f = R_f_te[f]
        W = clf.ssd_filters_[f]
        for col in range(W.shape[1]):
            w = W[:, col]
            p_te = np.einsum("c,ncd,d->n", w, R_f, w)
            ssd_cols.append(np.log(np.maximum(p_te, 1e-12))[:, None])
    M_te = np.hstack(ssd_cols)
    ssd_te = np.hstack([M_te, M_te - M_te.mean(axis=1, keepdims=True)])

    F_ts_te = clf.sc_ts_.transform(ts_te)
    F_cca_te = clf.sc_cca_.transform(np.hstack([extra_te, tmpl_te, ssd_te]))
    F_joint_te = np.hstack([F_ts_te, F_cca_te])

    def _project_te(name, F_te):
        base = clf.representer_bases_[name]
        if base is None:
            return F_te
        F_tr, U_scaled = base
        return (F_te @ F_tr.T) @ U_scaled

    return (
        _project_te("joint", F_joint_te),
        _project_te("cca", F_cca_te),
        _project_te("ts", F_ts_te),
    )


def main():
    t0 = time.time()
    mne.set_log_level("ERROR")
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(here)

    ds_objs = {
        "Kalunga2016": Kalunga2016(),
        "Nakanishi2015": Nakanishi2015(),
        "MAMEM3": MAMEM3(),
    }

    witness = {
        "target_id": "moabb-within-session-benchmark-cells",
        "paradigm": "SSVEP (All classes)",
        "evaluation": "WithinSessionEvaluation(n_splits=5, shuffle=True, random_state=42)",
        "ensemble_weights": {"joint": 0.45, "cca": 0.40, "ts": 0.15},
        "regularization_C": {"joint": 0.1, "cca": 0.2, "ts": 0.1},
        "sessions": [],
    }
    csv_rows = []

    for ds_name in ["Kalunga2016", "Nakanishi2015", "MAMEM3"]:
        ds = ds_objs[ds_name]
        ssvep_paradigm = SSVEP()
        ep_all, y_str, meta = ssvep_paradigm.get_data(ds, return_epochs=True)
        meta = meta.reset_index(drop=True)
        y_str = np.asarray(y_str)
        X_all = ep_all.get_data()
        sfreq = float(ep_all.info["sfreq"])
        times = ep_all.times

        # Fresh FilterBankSSVEP instance per dataset so self.filters is initialized per dataset
        fb_paradigm = FilterBankSSVEP(n_classes=None)
        X_fb_all, _, _ = fb_paradigm.get_data(ds)
        cov_all = Covariances(estimator="oas").fit_transform(
            ExtendedSSVEPSignal().fit_transform(X_fb_all, y_str)
        )

        clf_warm = FBHTRSSVEPClassifier()
        stim_freqs = clf_warm._infer_stim_freqs(ep_all, y_str)
        clf_warm._extract_unsupervised_batch(
            X_all, sfreq, float(times[-1] - times[0]), stim_freqs
        )

        for (subj, sess), grp in meta.groupby(["subject", "session"], sort=False):
            idx = grp.index.to_numpy()
            ep_sub = ep_all[idx]
            cov_sub = cov_all[idx]
            y_sub_str = y_str[idx]

            le = LabelEncoder()
            y_enc = le.fit_transform(y_sub_str)
            classes = [str(c) for c in le.classes_]
            n_classes = len(classes)

            cv = StratifiedKFold(5, shuffle=True, random_state=42)
            folds_data = []
            fb_htr_scores = []
            mdm_scores = []
            ts_lr_scores = []

            for fold_idx, (tr, te) in enumerate(cv.split(cov_sub, y_enc)):
                y_tr = y_enc[tr]
                y_te = y_enc[te]

                clf = FBHTRSSVEPClassifier()
                clf.fit(ep_sub[tr], y_sub_str[tr])
                Z_j_te, Z_c_te, Z_t_te = extract_projected_test_views(clf, ep_sub[te])

                v_joint, pj = qr_factor_clf(clf.clf_joint_, Z_j_te)
                v_cca, pc = qr_factor_clf(clf.clf_cca_, Z_c_te)
                v_ts, pt = qr_factor_clf(clf.clf_ts_, Z_t_te)

                p_ens = 0.45 * pj + 0.40 * pc + 0.15 * pt
                pred_fb = np.argmax(p_ens, axis=1)
                acc_fb = float(np.mean(pred_fb == y_te))

                pred_mdm, pred_ts_lr = eval_baseline_fold(cov_sub, y_enc, tr, te)
                acc_mdm = float(np.mean(np.array(pred_mdm) == y_te))
                acc_ts_lr = float(np.mean(np.array(pred_ts_lr) == y_te))

                fb_htr_scores.append(acc_fb)
                mdm_scores.append(acc_mdm)
                ts_lr_scores.append(acc_ts_lr)

                folds_data.append({
                    "fold": fold_idx,
                    "train_idx": [int(i) for i in tr],
                    "test_idx": [int(i) for i in te],
                    "y_train": [int(y) for y in y_tr],
                    "y_test": [int(y) for y in y_te],
                    "views": {
                        "joint": v_joint,
                        "cca": v_cca,
                        "ts": v_ts,
                    },
                    "pred_fb_htr": [int(y) for y in pred_fb],
                    "pred_mdm": [int(y) for y in pred_mdm],
                    "pred_ts_lr": [int(y) for y in pred_ts_lr],
                    "acc_fb_htr": round(acc_fb, 10),
                    "acc_mdm": round(acc_mdm, 10),
                    "acc_ts_lr": round(acc_ts_lr, 10),
                })

            sess_fb = float(np.mean(fb_htr_scores))
            sess_mdm = float(np.mean(mdm_scores))
            sess_ts_lr = float(np.mean(ts_lr_scores))

            witness["sessions"].append({
                "dataset": ds_name,
                "subject": int(subj),
                "session": str(sess),
                "n_trials": int(len(idx)),
                "n_classes": int(n_classes),
                "classes": classes,
                "fb_htr_ssvep": round(sess_fb, 10),
                "ssvep_mdm": round(sess_mdm, 10),
                "ssvep_ts_lr": round(sess_ts_lr, 10),
                "folds": folds_data,
            })

            csv_rows.append({
                "dataset": ds_name,
                "subject": int(subj),
                "session": str(sess),
                "n_trials": int(len(idx)),
                "n_classes": int(n_classes),
                "fb_htr_ssvep": f"{sess_fb:.10f}",
                "ssvep_mdm": f"{sess_mdm:.10f}",
                "ssvep_ts_lr": f"{sess_ts_lr:.10f}",
                "fold0_fb_htr": f"{fb_htr_scores[0]:.10f}",
                "fold1_fb_htr": f"{fb_htr_scores[1]:.10f}",
                "fold2_fb_htr": f"{fb_htr_scores[2]:.10f}",
                "fold3_fb_htr": f"{fb_htr_scores[3]:.10f}",
                "fold4_fb_htr": f"{fb_htr_scores[4]:.10f}",
                "fold0_mdm": f"{mdm_scores[0]:.10f}",
                "fold1_mdm": f"{mdm_scores[1]:.10f}",
                "fold2_mdm": f"{mdm_scores[2]:.10f}",
                "fold3_mdm": f"{mdm_scores[3]:.10f}",
                "fold4_mdm": f"{mdm_scores[4]:.10f}",
                "fold0_ts_lr": f"{ts_lr_scores[0]:.10f}",
                "fold1_ts_lr": f"{ts_lr_scores[1]:.10f}",
                "fold2_ts_lr": f"{ts_lr_scores[2]:.10f}",
                "fold3_ts_lr": f"{ts_lr_scores[3]:.10f}",
                "fold4_ts_lr": f"{ts_lr_scores[4]:.10f}",
            })

    csv_path = os.path.join(pkg_root, "object", "moabb_ssvep_within_session_cells.csv")
    fieldnames = list(csv_rows[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(csv_rows)

    gz_path = os.path.join(
        pkg_root, "verify-it-yourself", "data", "moabb_ssvep_fold_witness.json.gz"
    )
    raw_json = json.dumps(witness, separators=(",", ":"), sort_keys=True).encode("utf-8")
    with gzip.open(gz_path, "wb", compresslevel=9) as f:
        f.write(raw_json)

    csv_sha = hashlib.sha256(open(csv_path, "rb").read()).hexdigest()
    gz_sha = hashlib.sha256(open(gz_path, "rb").read()).hexdigest()
    print(f"CSV size: {os.path.getsize(csv_path)} bytes, sha256: {csv_sha}")
    print(f"GZ  size: {os.path.getsize(gz_path)} bytes, sha256: {gz_sha}")
    print(f"Export completed in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
