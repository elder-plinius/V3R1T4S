context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: lpub-q7-n55-k10-d39   role: reproduce

The contributor's hash list: 12 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted)
Claim text: "the object gives an exact rational Delsarte linear-programming dual certificate that no [55,10,40]_7 code exists ... lowering the live codetables.de upper bound 40 ... by 1, to 39." Criterion p2 (verbatim): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification ...) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."
Delsarte LP, as I use it (Hamming scheme H(n,q)): if f(x) = sum_{j=0}^m f_j K_j(x) with f_0 > 0, f_j >= 0 for j >= 1, and f(i) <= 0 for every integer i in [d, n], then every code with minimum distance at least d has at most f(0)/f_0 words; K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s). A linear [n,k] code has q^k words, so f(0)/f_0 < q^k excludes it. Here f_0 = 1 and the object's rational y_j are the f_j.

## My checker (written before opening verify-it-yourself/)
My checker (written from scratch, not shipped in this package): exact Fractions and integer Krawtchouk. It self-tests K_j (orthogonality sums and K_j(0)), takes the excluded distance from the command line (not from the object), requires every y_j >= 0, evaluates f(0) and f(w) for all integer w in [40, 55] exactly, and compares with the object's stated P_at_0 and max values. Weights are integers, so only integer w are tested (as in the Delsarte theorem).

## Command and real output
    (own checker, run on object/*.json with the excluded distance 40 on the command line)
krawtchouk self-test OK
n,q,k = 55 7 10 excluded d = 40 degree m = 7
f(0) = 7145717180865253961732487977/30501068176025076000
f(0) < q^k : True  ratio 0.8293739190573837
max f(w), w in [d,n] = -13207755302871499166543/26415511095982869119952000 at w = 53 ; all <=0 : True ; count 16
matches object P_at_0: True ; matches object max: True ; q^k matches: True
CERT VALID (no code with min distance >=40, hence d<=39)

Negative control (same object, excluded distance lowered by one to 39; must be rejected, and is):
matches object P_at_0: True ; matches object max: False ; q^k matches: True
CERT INVALID

## Propagation closure (own script, not shipped in this package, on the four neighbour rows in the-record-we-beat/neighbours.csv; each row is the live neighbour cell plus the rule's offset)
shorten 54 9 live ub 40 offset 0 -> implied 40
puncture 54 10 live ub 39 offset 1 -> implied 40
subcode 55 9 live ub 41 offset 0 -> implied 41
pad with a zero column 56 10 live ub 41 offset 0 -> implied 41
live ub 40 neighbour closure 40 claimed 39 strictly below closure: True
Open PR values were not consulted by this role (they belong to the novelty skeptic); the closure above is the four live neighbours only.

## Author's checker, run only after mine
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 40) and neighbour propagation
{"q": 7, "n": 55, "k": 10, "D": 40, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 40; new upper bound 39; best upper bound implied by the four live neighbours = 40 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement: the same f(0), the same maximum, same verdict. No mismatch.

## Notes

Scope: this role confirms that the certificate is a valid exact Delsarte dual certificate excluding d >= 40 for q^k = 282475249, and that the new bound is below the four-neighbour closure. Currency of the live table is not judged here.

pass: true
