# Honesty gate: run 2026-11-09-1305, claim meunier-stable-kneser-odd-s-small-n, (k,s) = (3,5)

Written by the main session at 2026-11-09T14:44:29Z (date -u), after reading all panel files in full.

History, for honesty: the first panel (panel-v1/, claim/ with n = 17..21) passed REPRODUCE and CRITERION but failed
NOVELTY (Jonsson's 2012 Theorem 1.3 settles n = 18..21; on his text the open n are 17 and 22). PREREG.v3.md added
n = 22 and claim-v3/ went to a fresh panel. Superseded verdicts on claim-v3, kept for the record: a CRITERION that
failed only because it was not allowed to build CaDiCaL and so could not check n = 22 (panel-v3-first-criterion/), and
a passing REPRODUCE and CRITERION whose files quoted file-name patterns in angle brackets, which the kit's mechanical
check rejects (panel-v3-superseded/). Fresh REPRODUCE and CRITERION skeptics then reran everything on the same
claim-v3, including regenerating and checking the n = 22 proof themselves.

- reproduce.md: pass: true (own generator, all six CNF hashes; own drat-trim on the five shipped proofs; own CaDiCaL
  3.0.1 regenerated the n = 22 proof to the recorded sha256 d24a47fc...0c7b and drat-trim verified it; all six
  colourings proper with n - 10 colours).
- novelty.md: pass: true (Jonsson's text read directly: n = 17 and n = 22 open; no source gives either value).
- criterion.md: pass: true, confirmed_scope below.
- The own-exact lens (DSATUR, no SAT solver) agrees for n = 17..21; for n = 22 see attempts/own-exact/out_n22.txt.

status: CONFIRMED_SOLUTION
confirmed_scope: For (k,s) = (3,5) and every n from 17 to 22, the CNF 'KG(n,3)_{5-stab} is (n-11)-colourable' (regenerated independently, sha256 as in object/cnf_sha256.txt, symmetry breaking only by unit colours on the pairwise disjoint 5-stable sets Q_j = {j, j+t, j+2t}, t = floor(n/3)) is unsatisfiable by a DRAT proof that drat-trim verified (shipped for n = 17..21, regenerated bit-identically by CaDiCaL 3.0.1 for n = 22), and object/ holds a checked proper (n-10)-colouring, so chi(KG(n,3)_{5-stab}) = n - 10 for n = 17..22, covering every n left open for (3,5) by arXiv 2607.12912 (n = 17..21) and by Jonsson's Theorem 1.3 (n = 17 and 22).
