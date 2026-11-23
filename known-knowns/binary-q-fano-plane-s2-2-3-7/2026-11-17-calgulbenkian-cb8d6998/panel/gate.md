# Honesty gate (binary-q-fano-plane-s2-2-3-7)

status: CONFIRMED_PARTIAL
confirmed_scope: The file object/p2_240_planes_order5.txt gives an explicit order-5 matrix pi in GL(7,2) (acting on row vectors) and 240 distinct rank-3 planes of PG(6,2) that are pi-invariant as a set, disjoint from the 3-dimensional pi-fixed space F, pairwise meeting in at most a point, and covering each of the 120 points outside F exactly 14 times, which answers in the affirmative the Section 6 research problem of arXiv 2112.11766v3 with its evidently intended count of 14 (not the paper's misprinted 15), and says nothing about a 381-plane q-Fano plane or any code of 334 or more planes.

## Gate notes
- Object: object/p2_240_planes_order5.txt, sha256 cb8d6998429ada84305df6e4680f83ce60e90223c34b9513e632da182c708815.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Partial win p2 only; the 381-plane q-Fano plane (full criterion) and p1 are not claimed. The survey's research problem (arXiv:2112.11766v3, Section 6) says each outside point is covered '15 times', which is arithmetically impossible (240 x 7 = 1680 = 120 x 14); the target's p2 fixes the count at 14, and this object meets that. pi acts on row vectors (v -> v pi); equivalently its transpose acts on column vectors.
- The reproduce skeptic and a separate checker both confirmed every p2 property exhaustively over GF(2): pi of order 5 with a 3-dimensional fixed space F, 240 distinct rank-3 planes forming a pi-invariant set, all disjoint from F, 1680 distinct lines each in one plane, and every one of the 120 points outside F covered exactly 14 times.
