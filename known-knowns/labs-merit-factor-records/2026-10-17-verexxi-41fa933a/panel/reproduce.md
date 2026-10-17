# REPRODUCE verdict, claim L = 338

context: subagent (same VM)

Files named relative to the claim folder (panel-claim-L338). I read only files inside it; own work in work-reproduce/ (mychk.py).

## Definition used (quoted from CLAIM.md)
"Definitions: s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E).
Encoding of sequence.txt: character 0 means +1, character 1 means -1 (E is invariant under global negation)."
Claim: sequence.txt (L=338) has E = 7609, strictly below baseline 7865.
My checker (work-reproduce/mychk.py) was written before opening check_energy.py: exact Python integers, direct double loop.

## Checks
1. sequence.txt: length 338, alphabet {0,1} only. PASS.
2. My energy of sequence.txt: "338 7609" (also re-run via numpy autocorrelation: 7609; deterministic across repeated runs). F = 114244/15218. PASS (claimed 7609).
3. Parent source line: source_excerpts.txt line 792 of 2206.12070, L=339, B_339^{26,13,10,2}, hex "7fffffe000ffc231ec37835a670f85a749ccd8db61b9638d8cc9c 2785ad267835a34e9374aad556aaaaaa" (85 hex digits = 340 bits, top bit zero, so 339 bits; the space is a line wrap and removed). Decoded bits equal parent_sequence in parent.txt exactly (not complemented). My E(parent) = 7393; 339^2/(2*7393) = 7.772284593534..., matches printed F 7.77228459353; the only integer E consistent with that printed F is 7393. Not a "repair:" parent; no note:. PASS.
4. Operation: operation_code prefix=- suffix=- trim_start=0 trim_end=1: parent[:338] == sequence.txt (True); parent[1:] == sequence.txt (False, so the direction matters and is as stated). PASS.
5. Baseline row for 338 (the only row in baseline.tsv): source 2206.12070, printed_E empty, printed_F 7.26280991736, hex row line 791 "3fffffe001fe43398de06f21f03c9e4b4d26396733633261b670c 3c69cb52972e568d9b346a9556aaaaaa" (85 digits, top 2 bits zero, 338 bits). My recomputed E of the decoded printed sequence = 7865. Smallest/only integer E consistent with printed F 7.26280991736 at L=338 = 7865. Both equal baseline.tsv columns (7865, 7865). baseline_E = 7865. PASS.
6. 7609 < 7865 strictly. Integer comparison. PASS. (Decoded 338 baseline sequence differs from the claimed sequence; claimed one is not a copy of it.)
7. Agreement among baseline.tsv, source_excerpts.txt, sources_checked.md: the excerpts contain a L=338 line only from 2206.12070 (the 1406.5301 line quoted is L=341); sources_checked.md marks "yes" only for 2206.12070 and "no" for 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222, 2504.00987, 2607.09688, knauer2004; baseline.tsv has exactly one data row (2206.12070). URL, fetch time (17:00:24Z) and HTTP 200 agree between baseline.tsv, parent.txt and sources_checked.md. Consistent. PASS. (Unread sources are listed as such in sources_checked.md; their completeness is for NOVELTY/CRITERION.)
8. check_energy.py (read after my checker): same definition, exact ints; outputs "338 7609" on sequence.txt (3 runs, identical) and "339 7393" on the parent; agrees with my checker. PASS.

## Real outputs
mychk: sequence -> 338 7609; parent -> 339 7393; hex-decoded L=338 row -> 338 7865.
check_energy.py: 338 7609 (x3); 339 7393.

No mismatch, missing object, or non-determinism found.

pass: true
