# Meunier's conjecture holds for (k,s) = (3,5) at every open n: chi(KG(n,3)_{5-stab}) = n - 10 for n = 17..22

## What

For (k,s) = (3,5) and every n from 17 to 22, the CNF 'KG(n,3)_{5-stab} is (n-11)-colourable' (regenerated independently, sha256 as in object/cnf_sha256.txt, symmetry breaking only by unit colours on the pairwise disjoint 5-stable sets Q_j = {j, j+t, j+2t}, t = floor(n/3)) is unsatisfiable by a DRAT proof that drat-trim verified (shipped for n = 17..21, regenerated bit-identically by CaDiCaL 3.0.1 for n = 22), and object/ holds a checked proper (n-10)-colouring, so chi(KG(n,3)_{5-stab}) = n - 10 for n = 17..22, covering every n left open for (3,5) by arXiv 2607.12912 (n = 17..21) and by Jonsson's Theorem 1.3 (n = 17 and 22).

(In this package, claim/object/ is object/.)

Status (panel/gate.md): CONFIRMED_SOLUTION (three-skeptic panel, 3/3 pass on the revised claim). In plain words: the
s-stable Kneser graph KG(n,k)_{s-stab} has the k-subsets of [n] whose elements are pairwise at least s apart around
the cycle as vertices, adjacent when disjoint; Meunier conjectured its chromatic number is n - sk + s. For (3,5)
this was open at n = 17 and n = 22. Here both are settled: 7 and 12 colours are needed, certified by DRAT proofs
that drat-trim verifies, and explicit colourings show they suffice. The same holds at n = 18..21, where Jonsson's
2012 theorem already gave it; those certificates confirm it by computer.

## Check it yourself

    DRAT_TRIM=/path/to/drat-trim CADICAL=/path/to/cadical sh verify-it-yourself/run_checks.sh     # last line: PASS

The full check takes about 10-12 minutes on one core: it regenerates all six CNFs and checks their sha256, checks
every colouring, checks the five shipped proofs, and regenerates the n = 22 proof with CaDiCaL (752 MB, the recorded
sha256) and checks it with drat-trim. Without CADICAL it runs in seconds and stops short of the n = 22 proof (its
n = 22 line says so). Python 3 standard library otherwise. Real output of the full check:
verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| arXiv 2607.12912 (status of Meunier's conjecture) | chi(KG(n,3)_{5-stab}), n = 17..22 | not determined for s = 5 | https://arxiv.org/abs/2607.12912 | 2026-11-09T13:04:44Z (sha256 7166ca68...c6cb) |
| Jonsson 2012, Theorem 1.3 (with Schrijver) | lower bounds at n = 17, 22 | 6 and 11 (the conjecture says 7 and 12) | Wayback copy, the-record-we-beat/README.md | 2026-11-09T13:21:17Z (sha256 ee446067...2eaa) |

## Not claimed

- n = 18, 19, 20, 21 are not new: Jonsson's Theorem 1.3 already gives chi = n - 10 there. Their certificates are
  independent computer confirmations.
- Only the pair (3,5). The bank entry's open range "17..21" follows a paraphrase of Jonsson's result; on his text the
  open n are 17 and 22, and both are covered here.
- Not peer reviewed; checked by a three-skeptic panel (panel/) and by the standalone checker shipped here. This is a
  certified computational result (UNSAT proofs checked by drat-trim, explicit colourings), not a proof of anything
  else.

## Credits

- F. Meunier, The chromatic number of almost stable Kneser hypergraphs, J. Combin. Theory Ser. A 118 (2011)
  (arXiv:0912.4748): the conjecture and n = sk + 1.
- W.-C. Chen, A. Parker, S. Zerbib, The chromatic number of 3-stable Kneser graphs, arXiv:2607.12912 (2026).
- J. Jonsson, On the chromatic number of generalized stable Kneser graphs, manuscript (2012).
- A. Schrijver, Vertex-critical subgraphs of Kneser graphs, Nieuw Arch. Wisk. (1978).
- Tools: CaDiCaL (A. Biere and collaborators), drat-trim (M. Heule and collaborators).
- The scan that flagged the target: the 2026-11-09 V3R1T4S bank scan.
