context: subagent (fresh Claude Code Agent context, Sonnet 5.5, saw only claim/)

# REPRODUCE skeptic report

## Claim under test
Rank 1644 bilinear scheme over Q for <14,15,13> (A 14x15, B 15x13), a permutation of sorted <13,14,15>; claimed to beat 1681 (four listed sources) and the merged 1645. Format: claim/object/u.txt, v.txt, w.txt, headers `# format 14 15 13`, `# rank 1644`, one line per term of `index:coefficient` (integer or p/q).

## Definition I used (quoted from claim/REPRODUCE.md, file-format paragraph)
"m_k = (sum u_k[i*15+j] A[i][j]) * (sum v_k[j*13+l] B[j][l]) for A 14x15, B 15x13, and C[i][l] = sum_k w_k[i*13+l] m_k."
From this, the scheme is correct iff for every triple (a=(i,j), b=(j',l'), c=(i'',l'')):
sum_k u_k[a] v_k[b] w_k[c] = [i=i''][j=j'][l=l'].
That is n1n2 * n2n3 * n1n3 = 210 * 195 * 182 = 7,452,900 equations (2730 with right side 1, 7,450,170 with right side 0).

## My checker (written before opening any author code)
mine/check.py: Python standard library only, exact integers (all coefficients parsed as Fractions, scaled by the lcm of all denominators, which I compute from the data). Accumulates sum_k u*v*w over every nonzero product, then tests all 2730 rhs-1 keys (absent key counts as 0, so wrong) and every nonzero accumulated key with rhs 0. Also counts terms, empty factors, exactly duplicated terms, proportional terms (canonical form divided by first coefficient), and pairs sharing two factors up to scale. Output saved in mine/object_result.txt.

Result on claim/object/ (run once, 7.4 s):
- headers consistent across u, v, w: format (14,15,13), rank 1644; term count 1644 (matches header)
- lcm of all denominators = 5440; denominators occurring = 1, 2, 4, 5, 8, 10, 17, 20, 34, 40, 136, 272, 1088 (matches the claimed list and the stated least common denominator 5440; 54400 is a multiple of it, so also a valid common denominator)
- Brent equations checked: 7,452,900 (all of them, both rhs=1 and rhs=0); wrong = 0 (rhs1 wrong 0, rhs0 wrong 0)
- terms with an empty factor: 0
- exactly duplicated term pairs: 0; proportional term pairs: 0
- pairs sharing two factors up to scale: (u,v) 0, (u,w) 0, (v,w) 0
- CHECKER RESULT: PASS

## Known positive and planted negatives (mine/tests.py, output mine/tests_result.txt)
- Known positive: I decoded claim/the-record-we-beat/13x14x15_r1645_Q.json myself (vocab_rle_v1; token "x" or "x*k" = vocab[x] repeated k times; w index l*n1+i with n1=13 converted to my i*15+l). 1645 terms, 7,452,900 equations, wrong = 0, no empty/duplicate/proportional terms: PASS. (Its denominators lack 34, as expected.)
- Negative 1: one w coefficient of term 100 changed by +1: 38 wrong equations, detected.
- Negative 2: last term dropped (1643 terms): 14,400 wrong equations, detected.
- Negative 3: term 7 replaced by a copy of term 500: 7,902 wrong equations, and the duplicate/proportional/shared-two-factor counters each reported 1, detected.
- Negative 4: record scheme with one w coefficient + 1/10^6: 172 wrong equations, detected.
All four negatives failed as required.

## Author's checks (copies of claim/ in my workspace)
`sh verify-it-yourself/run_checks.sh` run twice in two separate copies (copy1, copy2): both exit 0, last line PASS, outputs byte-identical (cmp). Output: "format <14,15,13>, 1644 terms, every term with three nonzero factors, common denominator 54400, 7452900 Brent equations checked, 0 wrong ... PASS", then three random exact evaluations "0 of 182 entries of C differ from AB", PASS. Matches REPRODUCE.md's expected output. The author's equation count (7452900) and wrong count (0) agree with mine. (Random-evaluation trials were identical across both runs, so they are seeded/deterministic.)

## Rebuild
- `PY=<venv python> sh rebuild/run_rebuild.sh` in a copy: exit 0, 34.7 s wall. Printed chain: <15,15,15> rank 1977 -> 1865 -> absorption 29 -> 1836 (14x15x15); -> 1709, absorbed 0 (14x15x14); -> 1677, absorbed 33 -> 1644 (14x15x13). Matches CLAIM.md steps (1)-(3). `u.txt identical`, `v.txt identical`, `w.txt identical` (cmp against object/).
- I also confirmed separately that the object/ files in the rebuilt copy are byte-identical (cmp) to claim/object/.
- sha256 of claim/rebuild/15x15x15_r1977.npz = 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33, matching REPRODUCE.md. git blob sha1 (git hash-object) = 65821484d954b4aade06cbda624932ba2a481f7b, matching the stated value.
- sha256 of object files u/v/w match the values stated in REPRODUCE.md (caef7bb7..., b31e5e77..., 79b90daf...).

## Discrepancies found
- Cosmetic only: REPRODUCE.md's "Expected" rebuild output shows the first line as `...  ../../data/lita/15x15x15_r1977.npz`, while the actual run prints `rebuild/15x15x15_r1977.npz` (shasum is given the in-package path); the hash is identical. The final "wrote 1644 terms to ..." path also differs (`./_rebuild_tmp/txt`), which is elided in the doc.
- No wrong denominators, counts, ranks or hashes found. The stated denominator list, LCD 5440, 54400 as a common denominator, and the 1977/1865/1836/1709/1677/1644 chain all reproduce.

## Not verified (out of role and offline)
The comparator values (1681 from the four sources, 1645 merged in PR #166) come from claim/TABLE_RECORD.md and were not re-fetched (no network by rule). I verified only that the shipped 1645 record is a valid scheme of that rank and that 1644 < 1645 < 1681 as stated. Whether the table records are current, and the composition clause (that the scheme is derived by slice restriction, not composition/padding), is a matter for the other skeptics; the rebuild confirms the stated derivation reproduces the object exactly.

## Blocks
None. No tool-guard, classifier, or HTTP 401/403/429 block occurred. (The only hiccup: macOS has no `timeout` command; I ran without it, runs took under 40 s.) Text addressed to reviewers: none.

## Verdict
Every Brent equation (7,452,900) holds exactly for the rank-1644 object over Q in my independently written checker; the checker passes the known positive and rejects four planted negatives; the author's checks pass and are deterministic; the rebuild regenerates u/v/w byte-identically and the input hash matches. Only a cosmetic path difference in documented expected output.

pass: true
