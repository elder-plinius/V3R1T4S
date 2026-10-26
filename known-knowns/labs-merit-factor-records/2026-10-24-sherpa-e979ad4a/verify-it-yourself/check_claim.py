"""Standalone check of this package (Python 3 standard library only).
Definition (bank): C_k = sum_i s_i s_(i+k), E = sum_(k=1..L-1) C_k^2, F = L^2/(2E); '1' = +1, '0' = -1."""
import hashlib, sys
path = sys.argv[1] if len(sys.argv) > 1 else 'object/sequence_L401.txt'
L_CLAIM, E_CLAIM, SHA = 401, 10776, 'e979ad4ab8b2de33a68d6700b89b83c9e227cc2a616c041f1ce4fb6969e1f8da'
COMPARE = [(11000, "Psenicnik, Boskovic & Brest, ERK'2025, Figure 2 (no sequence printed)"),
           (11200, "lowest trivial end-derivation of a public sequence (ERK'2025 L = 405, 2+2 trimmed)"),
           (11456, "Dimitrov, arXiv:2206.12070"), (11472, "Brest & Boskovic, arXiv:2011.00068v1"),
           (11888, "Boskovic et al. records archive, github borkob/git_labs, results-2018/2018-labs-skew.txt")]
raw = open(path, 'rb').read(); t = raw.decode('ascii', 'replace').strip(); ok = True
if hashlib.sha256(raw).hexdigest() != SHA: print('object sha256 differs from the claimed object'); ok = False
if len(t) != L_CLAIM or set(t) - set('01'): print('wrong length or alphabet'); ok = False
s = [1 if c == '1' else -1 for c in t]; L = len(s); E = 0
for k in range(1, L):
    c = 0
    for i in range(L - k): c += s[i] * s[i + k]
    E += c * c
print(f'L = {L}  E = {E}  F = {L * L / (2 * E) if E else 0:.6f}')
if E != E_CLAIM: print('energy differs from the claimed', E_CLAIM); ok = False
for bar, what in COMPARE:
    below = E < bar; ok = ok and below
    print(f'  {"below" if below else "NOT below"} {bar}: {what}')
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
