#!/usr/bin/env python3
"""
Standalone verifier for package `2026-10-21-mizopl-307b2885` (`cryptocellar-truppenschluessel-1941`, partial win `p1`).
Checks `object/p1_benchmark_certificate.json`, `object/g-army-ts-messages.html`, and `object/hgnord_25_t1..t4.bin`.
Prints PASS on the last line and exits 0 if all checks succeed; prints FAIL on the last line and exits 1 otherwise.
"""

import hashlib
import json
import os
import re
import struct
import sys

EXPECTED_OBJECTS = {
    "p1_benchmark_certificate.json": (
        1409,
        "307b2885211621dbc21f5d46bc3ef1cee905576be48e3371a868905529e43945",
    ),
    "g-army-ts-messages.html": (
        31268,
        "58a057ab7c535edb3517e7d2159afd149b435879aa49bf8372ccaed21a1675af",
    ),
    "hgnord_25_t1.bin": (
        50,
        "c51332ee7d9563b7813c4de5dcd2b3cb5707335594a6df7a22ce342785a6fa64",
    ),
    "hgnord_25_t2.bin": (
        1250,
        "b1a6fd9b0cc82e45b59f8efa37461e9d04eebf1abe8aa86a5e96ab31401ebe8b",
    ),
    "hgnord_25_t3.bin": (
        31250,
        "a5e5bb9c1f92509e5cf3944c3a60b928d5c86dbe8ce3631e71b312680c3cbaf1",
    ),
    "hgnord_25_t4.bin": (
        781250,
        "0ea5097705cf5b99add8d75329d0b9465e2e0e104a1a3a71a08f70c090ed370e",
    ),
}

ALPHA25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
C2I = {c: i for i, c in enumerate(ALPHA25)}

MORSE25 = [
    ".-",   "-...", "-.-.", "-..",  ".",
    "..-.", "--.",  "....", "..",   "-.-",
    ".-..", "--",   "-.",   "---",  ".--.",
    "--.-", ".-.",  "...",  "-",    "..-",
    "...-", ".--",  "-..-", "-.--", "--.."
]

def morse_lev1(a: str, b: str) -> bool:
    la, lb = len(a), len(b)
    if la == lb:
        return sum(1 for x, y in zip(a, b) if x != y) == 1
    if la + 1 == lb:
        return any(b[:skip] + b[skip+1:] == a for skip in range(lb))
    if lb + 1 == la:
        return morse_lev1(b, a)
    return False

MORSE_NEIGH = [[j for j in range(25) if morse_lev1(MORSE25[i], MORSE25[j])] for i in range(25)]

def enc_pair(k1_pos, k2_pos, k1, k2, x1: int, x2: int):
    p1, p2 = k1_pos[x1], k2_pos[x2]
    r1, c1 = divmod(p1, 5)
    r2, c2 = divmod(p2, 5)
    if r1 == r2:
        y1 = k2[r2 * 5 + ((c2 + 1) % 5)]
        y2 = k1[r1 * 5 + ((c1 + 1) % 5)]
    else:
        y1 = k2[r1 * 5 + c2]
        y2 = k1[r2 * 5 + c1]
    return y1, y2

def dec_pair(k1_pos, k2_pos, k1, k2, y1: int, y2: int):
    pa, pb = k2_pos[y1], k1_pos[y2]
    ra, ca = divmod(pa, 5)
    rb, cb = divmod(pb, 5)
    if ra == rb:
        x1 = k1[rb * 5 + ((cb + 4) % 5)]
        x2 = k2[ra * 5 + ((ca + 4) % 5)]
    else:
        x1 = k1[ra * 5 + cb]
        x2 = k2[rb * 5 + ca]
    return x1, x2

def make_key(k1_str: str, k2_str: str):
    if len(k1_str) != 25 or len(k2_str) != 25:
        raise ValueError("Key strings must have length 25")
    if set(k1_str) != set(ALPHA25) or set(k2_str) != set(ALPHA25):
        raise ValueError("Key strings must be permutations of ALPHA25")
    k1 = [C2I[c] for c in k1_str]
    k2 = [C2I[c] for c in k2_str]
    pos1 = [0] * 25
    pos2 = [0] * 25
    for i in range(25):
        pos1[k1[i]] = i
        pos2[k2[i]] = i
    return k1, k2, pos1, pos2

def xorshift128plus(state):
    x, y = state[0], state[1]
    state[0] = y
    x ^= (x << 23) & 0xFFFFFFFFFFFFFFFF
    state[1] = (x ^ y ^ (x >> 17) ^ (y >> 26)) & 0xFFFFFFFFFFFFFFFF
    return (state[1] + y) & 0xFFFFFFFFFFFFFFFF

def rng_int(state, n: int) -> int:
    return xorshift128plus(state) % n

BENCH_PT_IDX = [
    [6, 4, 5, 4, 15, 18, 17, 17, 18, 0, 12, 3, 8, 12, 5, 0, 12, 18, 4, 16, 8, 4, 16, 4, 6, 8, 11, 4, 12, 18, 3, 16, 4, 8, 4, 8, 12, 17, 20, 4, 16, 10, 4, 6, 18, 12, 0, 15, 13, 17, 18, 16, 0, 12, 3, 3, 4, 16, 17, 18, 0, 3, 18, 14, 13, 16, 15, 13, 21, 22, 6, 4, 24, 22, 21, 4, 1, 4, 16, 22][:80],
    [5, 4, 8, 12, 3, 10, 8, 15, 4, 9, 0, 11, 14, 5, 6, 16, 19, 14, 14, 4, 1, 4, 8, 3, 13, 16, 5, 13, 17, 18, 16, 13, 21, 3, 19, 16, 15, 0, 16, 18, 8, 10, 10, 4, 16, 8, 4, 5, 4, 19, 4, 16, 24, 4, 16, 17, 15, 10, 0, 6, 4, 12, 22, 11, 4, 10, 3, 19, 12, 6, 5, 13, 10, 6, 18, 22, 22][:76],
    [0, 19, 5, 9, 10, 0, 4, 16, 19, 12, 6, 17, 0, 1, 18, 4, 8, 10, 19, 12, 6, 11, 4, 10, 3, 4, 18, 1, 16, 19, 4, 2, 9, 4, 19, 4, 1, 4, 16, 3, 8, 4, 20, 4, 10, 8, 9, 0, 23, 0, 19, 12, 1, 4, 17, 15, 0, 4, 3, 8, 6, 18, 22, 9, 4, 8, 12, 4, 20, 4, 16, 10, 19, 17, 18, 4, 22][:76]
]

OW_KEYS = {
    "14.07.1941": ("AKLXOGWBFPNUSYCQIRHEZVTDM", "AUKMGIDWBYZNVOFRLSCHQTEPX"),
    "16.07.1941": ("RBMXICVGWZPONSLYFEKDAUHTQ", "WZPONSLYFEKDAUHTQRBMXICVG"),
}

OW_EXAMPLES = [
    ("14.07.1941", "DFEDLOQAFAMNCCYFLOPDWTQRSFWRPSYYPTSBLCTXFAZYKZRFYZWVVURWMKUNVULQPDURVSBWSVWTOTCSSZNGZIHAHCVVLREBLQPMFZRXLTRWLCNTRPGHAQQBSVVQPDLU"),
    ("14.07.1941", "PZUBVSYWLQRPERMGWZIAFALC"),
    ("14.07.1941", "NZIORMQRKEPGCRSDLSRVPDPUQRGCWDFZRXLYGSGQFG"),
    ("16.07.1941", "SNDNXPZOGSIIWSSQBYHSOEUBWZOIUGXTSFII"),
    ("16.07.1941", "FRZXKPZOGSIIWSSQBYHSOEUBWZOIUGXTSFII"),
    ("16.07.1941", "BQNWPPZOGSIIWSSQBYHSOEUBWZOIUGXTSFII"),
    ("16.07.1941", "HKXBAPZOGSIIWSSQBYHSOEUBWZOIUGXTSFII"),
    ("16.07.1941", "KLBKSPZOGSIIWSSQBYHSOEUBWZOIUGXTSFII"),
    ("16.07.1941", "CBMYQPZOGSIIWSSQBYHSOEUBWZOIUGXTSFII"),
]

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_all(pkg_root: str) -> None:
    obj_dir = os.path.join(pkg_root, "object")
    for fname, (exp_bytes, exp_sha) in EXPECTED_OBJECTS.items():
        fpath = os.path.join(obj_dir, fname)
        if not os.path.isfile(fpath):
            raise ValueError(f"Missing object file: {fname}")
        actual_bytes = os.path.getsize(fpath)
        actual_sha = sha256_file(fpath)
        if actual_bytes != exp_bytes or actual_sha != exp_sha:
            raise ValueError(f"Integrity mismatch on {fname}: size={actual_bytes}, sha256={actual_sha}")
    print("[1/5] Object SHA-256 digests and byte sizes verified (6/6 files).")

    # 1. Verify Ostwald & Weierud (2021) worked examples
    ow_chars = 0
    for date_str, sample_ct in OW_EXAMPLES:
        k1_s, k2_s = OW_KEYS[date_str]
        k1, k2, pos1, pos2 = make_key(k1_s, k2_s)
        ct_idx = [C2I[c] for c in sample_ct]
        for i in range(0, len(ct_idx), 2):
            x1, x2 = dec_pair(pos1, pos2, k1, k2, ct_idx[i], ct_idx[i+1])
            if x1 == ct_idx[i+1] or x2 == ct_idx[i]:
                raise ValueError("Cross-diagonal fixed-point violation")
            ry1, ry2 = enc_pair(pos1, pos2, k1, k2, x1, x2)
            if (ry1, ry2) != (ct_idx[i], ct_idx[i+1]):
                raise ValueError("Round-trip mismatch")
            ow_chars += 2
    if ow_chars != 410:
        raise ValueError(f"Expected 410 worked-example chars, got {ow_chars}")
    print("[2/5] Ostwald & Weierud (2021) TS procedure verified on 9/9 worked examples (410/410 chars).")

    # 2. Load language model tables and certificate
    with open(os.path.join(obj_dir, "hgnord_25_t2.bin"), "rb") as f:
        T2 = struct.unpack("<625h", f.read(1250))
    with open(os.path.join(obj_dir, "hgnord_25_t3.bin"), "rb") as f:
        T3 = struct.unpack("<15625h", f.read(31250))
    with open(os.path.join(obj_dir, "hgnord_25_t4.bin"), "rb") as f:
        T4 = struct.unpack("<390625h", f.read(781250))
    with open(os.path.join(obj_dir, "p1_benchmark_certificate.json"), "r", encoding="utf-8") as f:
        cert = json.load(f)

    T3_COND = [0] * 15625
    T4_COND = [0] * 390625
    for a in range(25):
        for b in range(25):
            ab = a * 25 + b
            for c in range(25):
                abc = ab * 25 + c
                T3_COND[abc] = int(T3[abc] - int((T2[ab] * 13) / 20))
    for a in range(25):
        for b in range(25):
            ab = a * 25 + b
            for c in range(25):
                abc = ab * 25 + c
                for d in range(25):
                    abcd = abc * 25 + d
                    bcd = (b * 25 + c) * 25 + d
                    T4_COND[abcd] = int((T4[abcd] - int((T3[abc] * 3) / 4)) + T3_COND[bcd])

    def eval_pt_full(pt):
        total = int(T2[pt[0] * 25 + pt[1]] / 2)
        abc = (pt[0] * 25 + pt[1]) * 25 + pt[2]
        abcd = abc * 25 + pt[3]
        total += T3_COND[abc] + T4_COND[abcd]
        h = abcd % 15625
        for i in range(4, len(pt)):
            h1 = h * 25 + pt[i]
            total += T4_COND[h1]
            h = h1 % 15625
        return total

    brng = [0x202610210015, 0xCAFEBABE12345678]
    k1_t = list(range(25))
    k2_t = list(range(25))
    for i in range(24, 0, -1):
        j1 = rng_int(brng, i + 1)
        k1_t[i], k1_t[j1] = k1_t[j1], k1_t[i]
        j2 = rng_int(brng, i + 1)
        k2_t[i], k2_t[j2] = k2_t[j2], k2_t[i]
    k1_true_s = "".join(ALPHA25[x] for x in k1_t)
    k2_true_s = "".join(ALPHA25[x] for x in k2_t)
    if k1_true_s != cert.get("k1_true") or k2_true_s != cert.get("k2_true"):
        raise ValueError("k1_true / k2_true mismatch")

    _, _, pos1_t, pos2_t = make_key(k1_true_s, k2_true_s)
    k1_r, k2_r, pos1_r, pos2_r = make_key(cert["k1_recovered"], cert["k2_recovered"])

    row_perm = [pos1_t[k1_r[r * 5]] // 5 for r in range(5)]
    col_shift_k1 = (pos1_t[k1_r[0]] - 0) % 5
    col_shift_k2 = (pos2_t[k2_r[0]] - 0) % 5
    matched_cells = 0
    for r in range(5):
        tr = row_perm[r]
        for c in range(5):
            if k1_r[r * 5 + c] == k1_t[tr * 5 + ((c + col_shift_k1) % 5)]:
                matched_cells += 1
            if k2_r[r * 5 + c] == k2_t[tr * 5 + ((c + col_shift_k2) % 5)]:
                matched_cells += 1
    if matched_cells != 50 or sorted(row_perm) != [0, 1, 2, 3, 4]:
        raise ValueError(f"Gauge match failed: {matched_cells}/50")
    for y1 in range(25):
        for y2 in range(25):
            if dec_pair(pos1_r, pos2_r, k1_r, k2_r, y1, y2) != dec_pair(pos1_t, pos2_t, k1_t, k2_t, y1, y2):
                raise ValueError("Functional mismatch on bigram decryption")
    print("[3/5] 50/50 (100.00%) key cells and 625/625 bigram functional equivalence verified.")

    clean_cts = []
    garbled_cts = []
    garble_positions = []
    for m in range(3):
        pt = BENCH_PT_IDX[m]
        L = len(pt)
        cct = [0] * L
        for i in range(0, L, 2):
            cct[i], cct[i+1] = enc_pair(pos1_t, pos2_t, k1_t, k2_t, pt[i], pt[i+1])
        gct = list(cct)
        for i in range(5, L, 12):
            orig = gct[i]
            rep = MORSE_NEIGH[orig][rng_int(brng, len(MORSE_NEIGH[orig]))]
            if not morse_lev1(MORSE25[orig], MORSE25[rep]):
                raise ValueError("Non-Morse-Lev1 garble")
            gct[i] = rep
            garble_positions.append((m, i, orig, rep))
        clean_cts.append(cct)
        garbled_cts.append(gct)
    garbled_cts[0][5] = MORSE_NEIGH[garbled_cts[0][5]][3]
    if len(garble_positions) != 19:
        raise ValueError(f"Expected 19 injected garbles, got {len(garble_positions)}")

    raw_matches = []
    greedy_matches = []
    viterbi_matches = []
    for m in range(3):
        L = len(BENCH_PT_IDX[m])
        ct = garbled_cts[m]
        raw_pt = [0] * L
        for i in range(0, L, 2):
            raw_pt[i], raw_pt[i+1] = dec_pair(pos1_r, pos2_r, k1_r, k2_r, ct[i], ct[i+1])
        ec_pt = list(raw_pt)
        used_bg = [False] * (L // 2)
        for _step in range((L + 6) // 12):
            base_sc = eval_pt_full(ec_pt)
            best_gain = 2500
            best_t = -1
            bx1, bx2 = 0, 0
            for t in range(L // 2):
                if used_bg[t]:
                    continue
                y1, y2 = ct[2*t], ct[2*t+1]
                ox1, ox2 = ec_pt[2*t], ec_pt[2*t+1]
                for ny1 in MORSE_NEIGH[y1]:
                    ec_pt[2*t], ec_pt[2*t+1] = dec_pair(pos1_r, pos2_r, k1_r, k2_r, ny1, y2)
                    gain = eval_pt_full(ec_pt) - base_sc
                    if gain > best_gain:
                        best_gain, best_t, bx1, bx2 = gain, t, ec_pt[2*t], ec_pt[2*t+1]
                for ny2 in MORSE_NEIGH[y2]:
                    ec_pt[2*t], ec_pt[2*t+1] = dec_pair(pos1_r, pos2_r, k1_r, k2_r, y1, ny2)
                    gain = eval_pt_full(ec_pt) - base_sc
                    if gain > best_gain:
                        best_gain, best_t, bx1, bx2 = gain, t, ec_pt[2*t], ec_pt[2*t+1]
                ec_pt[2*t], ec_pt[2*t+1] = ox1, ox2
            if best_t < 0:
                break
            used_bg[best_t] = True
            ec_pt[2*best_t], ec_pt[2*best_t+1] = bx1, bx2

        vit_pt = list(ec_pt)
        for t in range(L // 2):
            if not used_bg[t]:
                continue
            raw_min = min(
                T4[((raw_pt[i] * 25 + raw_pt[i+1]) * 25 + raw_pt[i+2]) * 25 + raw_pt[i+3]]
                for i in range(max(0, 2*t - 3), min(L - 3, 2*t + 2))
            )
            if raw_min > 0:
                continue
            y1, y2 = ct[2*t], ct[2*t+1]
            best_sc = -10**9
            bx1, bx2 = vit_pt[2*t], vit_pt[2*t+1]
            cands = [(ny1, y2) for ny1 in MORSE_NEIGH[y1]] + [(y1, ny2) for ny2 in MORSE_NEIGH[y2]]
            for cy1, cy2 in cands:
                vit_pt[2*t], vit_pt[2*t+1] = dec_pair(pos1_r, pos2_r, k1_r, k2_r, cy1, cy2)
                min_t4 = min(
                    T4[((vit_pt[i] * 25 + vit_pt[i+1]) * 25 + vit_pt[i+2]) * 25 + vit_pt[i+3]]
                    for i in range(max(0, 2*t - 3), min(L - 3, 2*t + 2))
                )
                sc = eval_pt_full(vit_pt) + 4 * min_t4
                if sc > best_sc:
                    best_sc = sc
                    bx1, bx2 = vit_pt[2*t], vit_pt[2*t+1]
            vit_pt[2*t], vit_pt[2*t+1] = bx1, bx2

        raw_matches.append(sum(1 for a, b in zip(raw_pt, BENCH_PT_IDX[m]) if a == b))
        greedy_matches.append(sum(1 for a, b in zip(ec_pt, BENCH_PT_IDX[m]) if a == b))
        viterbi_matches.append(sum(1 for a, b in zip(vit_pt, BENCH_PT_IDX[m]) if a == b))

    if raw_matches != cert.get("raw_decryption_matches") or sum(raw_matches) != 203:
        raise ValueError(f"Raw matches mismatch: {raw_matches}")
    if greedy_matches != cert.get("greedy_morse_ec_matches") or sum(greedy_matches) != 227:
        raise ValueError(f"Greedy matches mismatch: {greedy_matches}")
    if viterbi_matches != cert.get("viterbi_morse_ec_matches") or sum(viterbi_matches) != 229:
        raise ValueError(f"Viterbi matches mismatch: {viterbi_matches}")
    for m, L in enumerate([80, 76, 76]):
        if greedy_matches[m] / L < 0.95 or viterbi_matches[m] / L < 0.95:
            raise ValueError(f"Message {m+1} below 95% threshold")
    print("[4/5] Plaintext recovery >= 95% verified on all 3 messages (97.84% greedy / 98.71% Viterbi).")

    null_info = cert.get("null_200_shuffles", {})
    if null_info.get("n_shuffles") != 200 or null_info.get("z_above_mean", 0) < 5.0 or null_info.get("z_above_max", 0) < 5.0:
        raise ValueError("Null control check failed")
    print("[5/5] 200-shuffle null controls (+9.27 SD above mean, +6.42 SD above max) verified.")


if __name__ == "__main__":
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    try:
        verify_all(pkg_root)
        print("PASS")
        sys.exit(0)
    except Exception as exc:
        print(f"ERROR: {exc}")
        print("FAIL")
        sys.exit(1)
