context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: lpub-q8-n67-k5-d55   role: reproduce

The contributor's hash list: 12 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted)
Claim text: "the object gives an exact rational Delsarte linear-programming dual certificate that no [67,5,56]_8 code exists ... lowering the live codetables.de upper bound 56 ... by 1, to 55." Criterion p2 (verbatim): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification ...) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."
Delsarte LP, as I use it (Hamming scheme H(n,q)): if f(x) = sum_{j=0}^m f_j K_j(x) with f_0 > 0, f_j >= 0 for j >= 1, and f(i) <= 0 for every integer i in [d, n], then every code with minimum distance at least d has at most f(0)/f_0 words; K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s). A linear [n,k] code has q^k words, so f(0)/f_0 < q^k excludes it. Here f_0 = 1 and the object's rational y_j are the f_j.

## My checker (written before opening verify-it-yourself/)
My checker (written from scratch, not shipped in this package): exact Fractions and integer Krawtchouk. It self-tests K_j (orthogonality sums and K_j(0)), takes the excluded distance from the command line (not from the object), requires every y_j >= 0, evaluates f(0) and f(w) for all integer w in [56, 67] exactly, and compares with the object's stated P_at_0 and max values. Weights are integers, so only integer w are tested (as in the Delsarte theorem).

## Command and real output
    (own checker, run on object/*.json with the excluded distance 56 on the command line)
krawtchouk self-test OK
n,q,k = 67 8 5 excluded d = 56 degree m = 3
f(0) = 2599266943397044/90226601905
f(0) < q^k : True  ratio 0.8791568155960161
max f(w), w in [d,n] = -444764489315164/889530443964507345 at w = 62 ; all <=0 : True ; count 12
matches object P_at_0: True ; matches object max: True ; q^k matches: True
CERT VALID (no code with min distance >=56, hence d<=55)

Negative control (same object, excluded distance lowered by one to 55; must be rejected, and is):
matches object P_at_0: True ; matches object max: False ; q^k matches: True
CERT INVALID

## Propagation closure (own script, not shipped in this package, on the four neighbour rows in the-record-we-beat/neighbours.csv; each row is the live neighbour cell plus the rule's offset)
shorten 66 4 live ub 56 offset 0 -> implied 56
puncture 66 5 live ub 55 offset 1 -> implied 56
subcode 67 4 live ub 56 offset 0 -> implied 56
pad with a zero column 68 5 live ub 56 offset 0 -> implied 56
live ub 56 neighbour closure 56 claimed 55 strictly below closure: True
Open PR values were not consulted by this role (they belong to the novelty skeptic); the closure above is the four live neighbours only.

## Author's checker, run only after mine
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 56) and neighbour propagation
{"q": 8, "n": 67, "k": 5, "D": 56, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 56; new upper bound 55; best upper bound implied by the four live neighbours = 56 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement: the same f(0), the same maximum, same verdict. No mismatch.

## Notes

Scope: this role confirms that the certificate is a valid exact Delsarte dual certificate excluding d >= 56 for q^k = 32768, and that the new bound is below the four-neighbour closure. Currency of the live table is not judged here.

pass: true
