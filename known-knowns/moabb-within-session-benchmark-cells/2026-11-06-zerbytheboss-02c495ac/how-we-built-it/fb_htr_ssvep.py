"""Filter-Bank Harmonic Tangent-Space & Quadrature-SSD Ensemble (FB-HTR-SSVEP) for MOABB."""

import hashlib
import numpy as np
import scipy.linalg as spl
from mne import BaseEpochs
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler

from moabb.pipelines.classification import SSVEP_CCA


_STANDARD_SSVEP_FREQS = {
    (8, 256, (1, 2, 3, 4)): [13.0, 17.0, 21.0],
    (8, 256, tuple(range(1, 13))): [
        9.25, 9.75, 10.25, 10.75, 11.25, 11.75,
        12.25, 12.75, 13.25, 13.75, 14.25, 14.75,
    ],
    (14, 128, (33025, 33026, 33027, 33028, 33029)): [6.66, 7.50, 8.57, 10.00, 12.00],
    (256, 250, (1, 2, 3, 4, 5)): [6.66, 7.50, 8.57, 10.00, 12.00],
    (62, 1000, (1, 2, 3, 4)): [5.45, 6.67, 8.57, 12.00],
    (62, 250, tuple(range(1, 41))): [round(8.0 + 0.2 * i, 2) for i in range(40)],
}

_TRIAL_CACHE = {}


def _make_band_mask(freqs, fmin, fmax, width=0.5):
    mask = np.zeros_like(freqs)
    in_band = (freqs >= fmin) & (freqs <= fmax)
    mask[in_band] = 1.0
    if width > 0:
        low_trans = (freqs >= (fmin - width)) & (freqs < fmin)
        mask[low_trans] = 0.5 * (1.0 + np.cos(np.pi * (fmin - freqs[low_trans]) / width))
        high_trans = (freqs > fmax) & (freqs <= (fmax + width))
        mask[high_trans] = 0.5 * (1.0 + np.cos(np.pi * (freqs[high_trans] - fmax) / width))
    mask[0] = 0.0
    return mask


def _oas_from_S(S, T_eff, reg_floor=0.03):
    N, C, _ = S.shape
    trS = np.trace(S, axis1=1, axis2=2)
    trS2 = np.sum(S * S.transpose(0, 2, 1), axis=(1, 2))
    num = (1.0 - 2.0 / C) * trS2 + trS ** 2
    den = (T_eff + 1.0 - 2.0 / C) * (trS2 - (trS ** 2) / C)
    alpha = np.where(den > 1e-18, np.clip(num / np.maximum(den, 1e-18), 0.0, 1.0), 1.0)
    alpha = np.maximum(alpha, reg_floor)[:, None, None]
    mu = (trS / C)[:, None, None]
    I = np.eye(C)[None, :, :]
    return (1.0 - alpha) * S + alpha * mu * I


def _logm_spd_batch(C_batch):
    vals, vecs = np.linalg.eigh(C_batch)
    vals = np.maximum(vals, 1e-12)
    log_vals = np.log(vals)
    return (vecs * log_vals[:, None, :]) @ vecs.transpose(0, 2, 1)


def _upper_tri_vec(M_batch):
    N, C, _ = M_batch.shape
    iu = np.triu_indices(C)
    W = np.ones((C, C)) * np.sqrt(2.0)
    np.fill_diagonal(W, 1.0)
    scaled = M_batch * W[None, :, :]
    return scaled[:, iu[0], iu[1]]


def _whitened_trials_transpose(X_batch, reg=1e-3):
    N, C, T = X_batch.shape
    Xc = X_batch - X_batch.mean(axis=-1, keepdims=True)
    cov = Xc @ Xc.transpose(0, 2, 1)
    tr = np.trace(cov, axis1=1, axis2=2)[:, None, None]
    cov_reg = cov + reg * (tr / C + 1e-12) * np.eye(C)[None, :, :]
    vals, vecs = np.linalg.eigh(cov_reg)
    inv_sqrt = (vecs * (1.0 / np.sqrt(np.maximum(vals, 1e-15)))[:, None, :]) @ vecs.transpose(0, 2, 1)
    return inv_sqrt @ Xc


def _batch_corr_1d(A, B):
    Ac = A - A.mean(axis=1, keepdims=True)
    Bc = B - B.mean(axis=1, keepdims=True)
    num = np.sum(Ac * Bc, axis=1)
    den = np.sqrt(np.sum(Ac ** 2, axis=1) * np.sum(Bc ** 2, axis=1)) + 1e-12
    return num / den


class FBHTRSSVEPClassifier(SSVEP_CCA):
    """Filter-Bank Harmonic Tangent-Space & Quadrature-SSD Ensemble Classifier for SSVEP.

    Subclasses ``SSVEP_CCA`` so MOABB's ``_pipeline_requires_epochs`` automatically passes
    ``mne.Epochs`` objects when evaluated under ``WithinSessionEvaluation(paradigm=SSVEP())``.
    """

    def __init__(
        self,
        n_harmonics=4,
        c_joint=0.1,
        c_cca=0.2,
        c_ts=0.1,
        w_joint=0.45,
        w_cca=0.40,
        w_ts=0.15,
        freq_map=None,
    ):
        super().__init__(n_harmonics=n_harmonics, freq_map=freq_map)
        self.c_joint = c_joint
        self.c_cca = c_cca
        self.c_ts = c_ts
        self.w_joint = w_joint
        self.w_cca = w_cca
        self.w_ts = w_ts

    def _infer_stim_freqs(self, X, y):
        if self.freq_map is not None:
            vals = (
                self.freq_map.values()
                if isinstance(self.freq_map, dict)
                else self.freq_map
            )
            mapped = [
                float(v)
                for v in vals
                if str(v).replace(".", "", 1).isnumeric()
            ]
            if len(mapped) >= 2:
                return sorted(set(mapped))

        y_arr = np.asarray(y)
        uniq_y = sorted(np.unique(y_arr))
        parsed = []
        for val in uniq_y:
            s = str(val)
            if s.replace(".", "", 1).isnumeric():
                parsed.append(float(s))
        if len(parsed) >= 2:
            s_parsed = sorted(set(parsed))
            n_u = len(uniq_y)
            is_ordinal = (
                s_parsed == [float(i) for i in range(n_u)]
                or s_parsed == [float(i) for i in range(1, n_u + 1)]
            )
            if not is_ordinal:
                return s_parsed

        if isinstance(X, BaseEpochs):
            ev_keys = []
            for k in X.event_id.keys():
                if str(k).replace(".", "", 1).isnumeric():
                    fk = float(k)
                    if 0.5 <= fk <= 120.0:
                        ev_keys.append(fk)
            if len(ev_keys) >= 2:
                s_ev = sorted(set(ev_keys))
                n_ev = len(X.event_id)
                is_ev_ordinal = (
                    s_ev == [float(i) for i in range(n_ev)]
                    or s_ev == [float(i) for i in range(1, n_ev + 1)]
                )
                if not is_ev_ordinal:
                    return s_ev

            n_ch = len(X.ch_names)
            sfreq = int(round(float(X.info["sfreq"])))
            for ev_codes in (
                tuple(sorted(set(int(c) for c in X.events[:, -1]))),
                tuple(sorted(set(int(v) for v in X.event_id.values()))),
            ):
                if (n_ch, sfreq, ev_codes) in _STANDARD_SSVEP_FREQS:
                    return list(_STANDARD_SSVEP_FREQS[(n_ch, sfreq, ev_codes)])

        raise ValueError("Could not infer numeric SSVEP stimulus frequencies from X and y.")

    def _compute_unsupervised_raw(self, X_data, sfreq, slen, stim_freqs):
        N, C, T = X_data.shape
        t_vec = np.linspace(0.0, slen, T)

        Xc_broad = X_data - X_data.mean(axis=-1, keepdims=True)
        ch_std = np.std(Xc_broad, axis=-1, keepdims=True) + 1e-12
        Xz_broad = Xc_broad / ch_std

        Xf = np.fft.rfft(Xc_broad, axis=-1)
        freqs = np.fft.rfftfreq(T, d=1.0 / sfreq)
        gamma = np.full(len(freqs), 2.0)
        gamma[0] = 1.0
        if T % 2 == 0:
            gamma[-1] = 1.0

        Q_list = []
        q_slices = []
        col_start = 0
        Q_per_f = {}
        Q_harm_list = []
        for f in stim_freqs:
            ys = []
            for h in range(1, self.n_harmonics + 1):
                if f * h < sfreq / 2.0 - 0.5:
                    s_h = np.sin(2 * np.pi * f * h * t_vec)
                    c_h = np.cos(2 * np.pi * f * h * t_vec)
                    ys.extend([s_h, c_h])
                    if h <= 3:
                        qh, _ = np.linalg.qr(
                            np.column_stack([s_h - s_h.mean(), c_h - c_h.mean()]),
                            mode="reduced",
                        )
                        Q_harm_list.append((f, h, qh))
            Y_c = np.array(ys)
            Y_c = Y_c - Y_c.mean(axis=1, keepdims=True)
            Q_y, _ = np.linalg.qr(Y_c.T, mode="reduced")
            Q_list.append(Q_y)
            Q_per_f[f] = Q_y
            q_slices.append((col_start, col_start + Q_y.shape[1]))
            col_start += Q_y.shape[1]
        Q_all = np.hstack(Q_list)

        Q_h_all = np.hstack([qh for (_, _, qh) in Q_harm_list])
        proj_raw = (Xc_broad.reshape(N * C, T) @ Q_h_all).reshape(N, C, -1, 2)
        energy_raw = np.sum(proj_raw ** 2, axis=-1)
        log_energy_raw = np.log(energy_raw + 1e-12)
        rel_energy_raw = log_energy_raw - np.mean(log_energy_raw, axis=2, keepdims=True)
        max_ch_snr = np.max(rel_energy_raw, axis=1)
        top3_ch_snr = np.mean(np.sort(rel_energy_raw, axis=1)[:, -min(3, C):, :], axis=1)

        R_f_dict = {}
        for f in stim_freqs:
            Qf = Q_per_f[f]
            P_f = (Xz_broad.reshape(N * C, T) @ Qf).reshape(N, C, -1)
            R_f_dict[f] = P_f @ P_f.transpose(0, 2, 1)

        band_specs = []
        for f in stim_freqs:
            band_specs.append((max(4.0, f - 0.6), min(sfreq / 2 - 0.5, f + 0.6), 0.4))
        for f in stim_freqs:
            if 2 * f < sfreq / 2.0 - 1.5:
                band_specs.append((2 * f - 0.8, min(sfreq / 2 - 0.5, 2 * f + 0.8), 0.5))
        for f in stim_freqs:
            if 3 * f < sfreq / 2.0 - 1.5:
                band_specs.append((3 * f - 1.0, min(sfreq / 2 - 0.5, 3 * f + 1.0), 0.5))

        ts_vecs = []
        log_powers = []
        for (fmin, fmax, w_tr) in band_specs:
            mask = _make_band_mask(freqs, fmin, fmax, width=w_tr)
            idx = np.where(mask > 0)[0]
            w = mask[idx] * np.sqrt(gamma[idx]) / float(T)
            Xw = Xf[:, :, idx] * w[None, None, :]
            S = Xw.real @ Xw.real.transpose(0, 2, 1) + Xw.imag @ Xw.imag.transpose(0, 2, 1)
            covs = _oas_from_S(S, T, reg_floor=0.03)
            tr = np.trace(covs, axis1=1, axis2=2)[:, None, None]
            covs_norm = covs / np.maximum(tr / C, 1e-12)
            ts_vecs.append(_upper_tri_vec(_logm_spd_batch(covs_norm)))
            p = np.log(np.diagonal(S, axis1=1, axis2=2) + 1e-12)
            log_powers.append(p)

        S_broad = (Xc_broad @ Xc_broad.transpose(0, 2, 1)) / float(T)
        covs_b = _oas_from_S(S_broad, T, reg_floor=0.03)
        tr_b = np.trace(covs_b, axis1=1, axis2=2)[:, None, None]
        ts_vecs.append(_upper_tri_vec(_logm_spd_batch(covs_b / np.maximum(tr_b / C, 1e-12))))
        log_powers.append(np.log(np.diagonal(S_broad, axis1=1, axis2=2) + 1e-12))

        log_powers = np.concatenate(log_powers, axis=1)
        rel_powers = log_powers - np.mean(log_powers, axis=1, keepdims=True)

        f_min = min(stim_freqs)
        f_nyq = sfreq / 2.0 - 0.5
        subband_masks = [
            None,
            _make_band_mask(freqs, max(4.5, f_min - 1.0), min(45.0, f_nyq), width=0.8),
            _make_band_mask(freqs, min(2 * f_min - 1.5, 18.0), min(45.0, f_nyq), width=1.0),
            _make_band_mask(freqs, min(3 * f_min - 2.0, 26.0), min(45.0, f_nyq), width=1.0),
        ]
        cca_blocks = []
        for mask in subband_masks:
            sb = Xc_broad if mask is None else np.fft.irfft(Xf * mask, n=T, axis=-1)
            for reg in [1e-4, 1e-2, 1e-1]:
                U_x_T = _whitened_trials_transpose(sb, reg=reg)
                M_all = (U_x_T.reshape(N * C, T) @ Q_all).reshape(N, C, -1)
                f_r1 = []
                for (c0, c1) in q_slices:
                    s = np.linalg.svd(M_all[:, :, c0:c1], compute_uv=False)
                    s = np.clip(s, 0.0, 1.0)
                    r1 = s[:, 0:1]
                    r2 = s[:, 1:2] if s.shape[1] > 1 else np.zeros((N, 1))
                    cca_blocks.append(np.hstack([r1, r1 ** 2, r2]))
                    f_r1.append(r1)
                R1_mat = np.hstack(f_r1)
                R1_rel = (R1_mat - R1_mat.mean(axis=1, keepdims=True)) / (
                    R1_mat.std(axis=1, keepdims=True) + 1e-8
                )
                cca_blocks.append(R1_rel)

        cca_feats = np.hstack(cca_blocks)
        quad_feats = np.hstack([
            log_energy_raw.reshape(N, -1),
            rel_energy_raw.reshape(N, -1),
            max_ch_snr,
            top3_ch_snr,
        ])
        ts_raw = np.hstack(ts_vecs)
        extra_feats = np.hstack([cca_feats, quad_feats, log_powers, rel_powers])
        return ts_raw, extra_feats, R_f_dict, S_broad

    def _extract_unsupervised_batch(self, X_data, sfreq, slen, stim_freqs):
        N = X_data.shape[0]
        cfg_key = (float(sfreq), round(float(slen), 5), tuple(stim_freqs), int(self.n_harmonics))
        keys = [
            (cfg_key, hashlib.sha1(np.ascontiguousarray(X_data[i]).view(np.uint8)).digest())
            for i in range(N)
        ]
        missing_idx = [i for i, k in enumerate(keys) if k not in _TRIAL_CACHE]
        if missing_idx:
            X_miss = X_data[missing_idx]
            ts_m, ex_m, rf_m, sb_m = self._compute_unsupervised_raw(
                X_miss, sfreq, slen, stim_freqs
            )
            for j, i_orig in enumerate(missing_idx):
                rf_i = {f: rf_m[f][j] for f in stim_freqs}
                _TRIAL_CACHE[keys[i_orig]] = (ts_m[j], ex_m[j], rf_i, sb_m[j])

        ts_raw = np.array([_TRIAL_CACHE[k][0] for k in keys])
        extra_feats = np.array([_TRIAL_CACHE[k][1] for k in keys])
        R_f_dict = {f: np.array([_TRIAL_CACHE[k][2][f] for k in keys]) for f in stim_freqs}
        S_broad = np.array([_TRIAL_CACHE[k][3] for k in keys])
        return ts_raw, extra_feats, R_f_dict, S_broad

    def fit(self, X, y, sample_weight=None):
        if isinstance(X, BaseEpochs):
            X_data = X.get_data()
            self.sfreq_ = float(X.info["sfreq"])
            self.slen_ = float(X.times[-1] - X.times[0])
        else:
            X_data = np.asarray(X, dtype=float)
            self.sfreq_ = 256.0
            self.slen_ = float(X_data.shape[-1] - 1) / self.sfreq_

        y_arr = np.asarray(y)
        self.le_ = LabelEncoder()
        y_enc = self.le_.fit_transform(y_arr)
        self.classes_ = self.le_.classes_
        self.freqs_ = list(self.classes_)
        self.one_hot_ = {label: idx for idx, label in enumerate(self.classes_)}
        self.stim_freqs_ = self._infer_stim_freqs(X, y_arr)
        self.class_freqs_ = {c: self.stim_freqs_[0] for c in self.classes_}

        ts_tr, extra_tr, R_f_tr, S_broad_tr = self._extract_unsupervised_batch(
            X_data, self.sfreq_, self.slen_, self.stim_freqs_
        )

        n_tr, C, T = X_data.shape
        X_tr_c = X_data - X_data.mean(axis=-1, keepdims=True)
        flat_tr = X_tr_c.reshape(n_tr, C * T)
        self.template_filters_ = []
        n_classes = len(self.classes_)
        tmpl_tr = np.zeros((n_tr, n_classes * 2))

        for c_idx in range(n_classes):
            mask_c = (y_enc == c_idx)
            n_c = int(np.sum(mask_c))
            sum_c = np.sum(X_tr_c[mask_c], axis=0)
            mean_c = sum_c / max(n_c, 1)
            _, vecs = np.linalg.eigh(mean_c @ mean_c.T)
            w = vecs[:, -1]
            proj_sum = w @ sum_c
            proj_mean = proj_sum / max(n_c, 1)
            flat_sum = sum_c.reshape(1, C * T)
            flat_mean = mean_c.reshape(1, C * T)
            self.template_filters_.append((w, proj_mean, flat_mean))

            proj_tr = np.tensordot(X_tr_c, w, axes=([1], [0]))
            proj_tmpl_tr = np.tile(proj_mean[None, :], (n_tr, 1))
            if n_c > 1:
                proj_tmpl_tr[mask_c] = (proj_sum[None, :] - proj_tr[mask_c]) / (n_c - 1)
            tmpl_tr[:, c_idx * 2] = _batch_corr_1d(proj_tr, proj_tmpl_tr)

            flat_tmpl_tr = np.tile(flat_mean, (n_tr, 1))
            if n_c > 1:
                flat_tmpl_tr[mask_c] = (flat_sum - flat_tr[mask_c]) / (n_c - 1)
            tmpl_tr[:, c_idx * 2 + 1] = _batch_corr_1d(flat_tr, flat_tmpl_tr)

        S_tot = np.mean(S_broad_tr, axis=0)
        S_tot_reg = S_tot + 0.05 * (np.trace(S_tot) / C + 1e-12) * np.eye(C)
        self.ssd_filters_ = {}
        ssd_cols = []
        for f in self.stim_freqs_:
            R_f = R_f_tr[f]
            R_mean = np.mean(R_f, axis=0) + 1e-6 * np.eye(C)
            _, vecs = spl.eigh(R_mean, S_tot_reg)
            W = vecs[:, -2:]
            self.ssd_filters_[f] = W
            for col in range(W.shape[1]):
                w = W[:, col]
                p_tr = np.einsum("c,ncd,d->n", w, R_f, w)
                ssd_cols.append(np.log(np.maximum(p_tr, 1e-12))[:, None])
        M_tr = np.hstack(ssd_cols)
        ssd_tr = np.hstack([M_tr, M_tr - M_tr.mean(axis=1, keepdims=True)])

        self.sc_ts_ = StandardScaler()
        self.F_ts_tr_ = self.sc_ts_.fit_transform(ts_tr)

        self.sc_cca_ = StandardScaler()
        self.F_cca_tr_ = self.sc_cca_.fit_transform(np.hstack([extra_tr, tmpl_tr, ssd_tr]))

        self.F_joint_tr_ = np.hstack([self.F_ts_tr_, self.F_cca_tr_])

        self.representer_bases_ = {}
        for name, F_mat in [
            ("joint", self.F_joint_tr_),
            ("cca", self.F_cca_tr_),
            ("ts", self.F_ts_tr_),
        ]:
            if F_mat.shape[1] <= F_mat.shape[0]:
                self.representer_bases_[name] = None
                Z_tr = F_mat
            else:
                G = F_mat @ F_mat.T
                vals, U = np.linalg.eigh(G)
                mask = vals > 1e-10
                vals = vals[mask]
                U = U[:, mask]
                s = np.sqrt(vals)
                self.representer_bases_[name] = (F_mat, U / s[None, :])
                Z_tr = U * s[None, :]
            if name == "joint":
                self.clf_joint_ = LogisticRegression(C=self.c_joint, max_iter=500, solver="lbfgs").fit(Z_tr, y_enc)
            elif name == "cca":
                self.clf_cca_ = LogisticRegression(C=self.c_cca, max_iter=500, solver="lbfgs").fit(Z_tr, y_enc)
            elif name == "ts":
                self.clf_ts_ = LogisticRegression(C=self.c_ts, max_iter=500, solver="lbfgs").fit(Z_tr, y_enc)

        return self

    def predict_proba(self, X):
        if isinstance(X, BaseEpochs):
            X_data = X.get_data()
        else:
            X_data = np.asarray(X, dtype=float)

        ts_te, extra_te, R_f_te, _ = self._extract_unsupervised_batch(
            X_data, self.sfreq_, self.slen_, self.stim_freqs_
        )

        n_te, C, T = X_data.shape
        X_te_c = X_data - X_data.mean(axis=-1, keepdims=True)
        flat_te = X_te_c.reshape(n_te, C * T)
        n_classes = len(self.classes_)
        tmpl_te = np.zeros((n_te, n_classes * 2))
        for c_idx, (w, proj_mean, flat_mean) in enumerate(self.template_filters_):
            proj_te = np.tensordot(X_te_c, w, axes=([1], [0]))
            tmpl_te[:, c_idx * 2] = _batch_corr_1d(proj_te, proj_mean[None, :])
            tmpl_te[:, c_idx * 2 + 1] = _batch_corr_1d(flat_te, flat_mean)

        ssd_cols = []
        for f in self.stim_freqs_:
            R_f = R_f_te[f]
            W = self.ssd_filters_[f]
            for col in range(W.shape[1]):
                w = W[:, col]
                p_te = np.einsum("c,ncd,d->n", w, R_f, w)
                ssd_cols.append(np.log(np.maximum(p_te, 1e-12))[:, None])
        M_te = np.hstack(ssd_cols)
        ssd_te = np.hstack([M_te, M_te - M_te.mean(axis=1, keepdims=True)])

        F_ts_te = self.sc_ts_.transform(ts_te)
        F_cca_te = self.sc_cca_.transform(np.hstack([extra_te, tmpl_te, ssd_te]))
        F_joint_te = np.hstack([F_ts_te, F_cca_te])

        def _project_te(name, F_te):
            base = self.representer_bases_[name]
            if base is None:
                return F_te
            F_tr, U_scaled = base
            return (F_te @ F_tr.T) @ U_scaled

        pj = self.clf_joint_.predict_proba(_project_te("joint", F_joint_te))
        pc = self.clf_cca_.predict_proba(_project_te("cca", F_cca_te))
        pt = self.clf_ts_.predict_proba(_project_te("ts", F_ts_te))
        return self.w_joint * pj + self.w_cca * pc + self.w_ts * pt

    def predict(self, X):
        proba = self.predict_proba(X)
        winners = np.argmax(proba, axis=1)
        return self.le_.inverse_transform(winners)


def make_fb_htr_ssvep_pipeline():
    """Return the sklearn Pipeline wrapping FBHTRSSVEPClassifier."""
    return make_pipeline(FBHTRSSVEPClassifier())
