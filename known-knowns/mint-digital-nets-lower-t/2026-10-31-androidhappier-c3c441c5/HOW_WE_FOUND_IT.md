# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target mint-digital-nets-lower-t: find explicit generator matrices of a
digital (t,m,s)-net whose t is strictly below MinT's "Constructive and digital" value for that cell.

- First we built exact checkers and validated them on small fixtures: a positive Hammersley-type net, negatives with
  duplicated rows, and agreement with a point-counting check of the net definition on 180 small cases. This was the
  exact-eval-first step.
- What worked: a depth-major randomized greedy (how-we-built-it/gvgreedy2.c). Rows are placed level by level across
  all 17 matrices. Each new row is drawn from the vectors outside an exact forbidden set, stored as a bitmap over
  F_2^24, so the result is a net by construction. At m = 24 this reached t = 11 for s up to 17 with seed 101. The
  search took seconds. MinT's constructive value there is 13, coming from s-reduction of a shift-net.
- What failed:
  - Pushing the same greedy one step further: (11,24,18), (10,24,16), (11,25,17) and others failed at all three
    preregistered seeds.
  - Deterministic row choices (lexicographically first or last free vector, block-major order) did worse than
    random choices.
  - A plain union-bound argument proves nothing below MinT's existence values. It only predicts where the greedy
    runs out of free vectors.
- The slow generic Python checker named in PREREG.md did not finish at this size, so it was abandoned. The claim
  rests on two other independent checkers, plus the panel's own independent checker (panel/reproduce.md).
- A three-skeptic panel (reproduce, novelty, criterion) and an honesty gate then confirmed the scope quoted in
  README.md.
