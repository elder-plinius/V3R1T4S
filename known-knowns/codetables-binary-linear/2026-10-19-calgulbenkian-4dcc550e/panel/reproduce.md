context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: lpub-q4-n148-k7-d106   role: reproduce

The contributor's hash list: 12 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted)
Claim text: "the object gives an exact rational Delsarte linear-programming dual certificate that no [148,7,107]_4 code exists ... lowering the live codetables.de upper bound 107 ... by 1, to 106." Criterion p2 (verbatim): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification ...) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."
Delsarte LP, as I use it (Hamming scheme H(n,q)): if f(x) = sum_{j=0}^m f_j K_j(x) with f_0 > 0, f_j >= 0 for j >= 1, and f(i) <= 0 for every integer i in [d, n], then every code with minimum distance at least d has at most f(0)/f_0 words; K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s). A linear [n,k] code has q^k words, so f(0)/f_0 < q^k excludes it. Here f_0 = 1 and the object's rational y_j are the f_j.

## My checker (written before opening verify-it-yourself/)
My checker (written from scratch, not shipped in this package): exact Fractions and integer Krawtchouk. It self-tests K_j (orthogonality sums and K_j(0)), takes the excluded distance from the command line (not from the object), requires every y_j >= 0, evaluates f(0) and f(w) for all integer w in [107, 148] exactly, and compares with the object's stated P_at_0 and max values. Weights are integers, so only integer w are tested (as in the Delsarte theorem).

## Command and real output
    (own checker, run on object/*.json with the excluded distance 107 on the command line)
krawtchouk self-test OK
n,q,k = 148 4 7 excluded d = 107 degree m = 3
f(0) = 258051632794969/16695880740
f(0) < q^k : True  ratio 0.9433597408535728
max f(w), w in [d,n] = -3314519539249/6629049360174780 at w = 118 ; all <=0 : True ; count 42
matches object P_at_0: True ; matches object max: True ; q^k matches: True
CERT VALID (no code with min distance >=107, hence d<=106)

Negative control (same object, excluded distance lowered by one to 106; must be rejected, and is):
matches object P_at_0: True ; matches object max: False ; q^k matches: True
CERT INVALID

## Propagation closure (own script, not shipped in this package, on the four neighbour rows in the-record-we-beat/neighbours.csv; each row is the live neighbour cell plus the rule's offset)
shorten 147 6 live ub 108 offset 0 -> implied 108
puncture 147 7 live ub 106 offset 1 -> implied 107
subcode 148 6 live ub 108 offset 0 -> implied 108
pad with a zero column 149 7 live ub 107 offset 0 -> implied 107
live ub 107 neighbour closure 107 claimed 106 strictly below closure: True
Open PR values were not consulted by this role (they belong to the novelty skeptic); the closure above is the four live neighbours only.

## Author's checker, run only after mine
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 107) and neighbour propagation
{"q": 4, "n": 148, "k": 7, "D": 107, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 107; new upper bound 106; best upper bound implied by the four live neighbours = 107 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement: the same f(0), the same maximum, same verdict. No mismatch.

## Notes

Scope: this role confirms that the certificate is a valid exact Delsarte dual certificate excluding d >= 107 for q^k = 16384, and that the new bound is below the four-neighbour closure. Currency of the live table is not judged here.

pass: true
