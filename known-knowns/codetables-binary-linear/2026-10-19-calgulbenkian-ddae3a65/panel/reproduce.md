context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: lpub-q2-n163-k18-d71   role: reproduce

The contributor's hash list: 12 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted)
Claim text: "the object gives an exact rational Delsarte linear-programming dual certificate that no [163,18,72]_2 code exists ... lowering the live codetables.de upper bound 72 ... by 1, to 71." Criterion p2 (verbatim): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification ...) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."
Delsarte LP, as I use it (Hamming scheme H(n,q)): if f(x) = sum_{j=0}^m f_j K_j(x) with f_0 > 0, f_j >= 0 for j >= 1, and f(i) <= 0 for every integer i in [d, n], then every code with minimum distance at least d has at most f(0)/f_0 words; K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s). A linear [n,k] code has q^k words, so f(0)/f_0 < q^k excludes it. Here f_0 = 1 and the object's rational y_j are the f_j.

## My checker (written before opening verify-it-yourself/)
Own program, not shipped in this package: exact Fractions and integer Krawtchouk. It self-tests K_j (orthogonality sums and K_j(0)), takes the excluded distance from the command line (not from the object), requires every y_j >= 0, evaluates f(0) and f(w) for all integer w in [72, 163] exactly, and compares with the object's stated P_at_0 and max values. Weights are integers, so only integer w are tested (as in the Delsarte theorem).

## Command and real output
    (own checker, run on object/lp_cert_q2_n163_k18_dub72.json, excluded distance 72)
krawtchouk self-test OK
n,q,k = 163 2 18 excluded d = 72 degree m = 5
f(0) = 138327920185042536516573/621000958767257068
f(0) < q^k : True  ratio 0.8497235494401905
max f(w), w in [d,n] = -731566217158668677/1463134713488272857396 at w = 72 ; all <=0 : True ; count 92
matches object P_at_0: True ; matches object max: True ; q^k matches: True
CERT VALID (no code with min distance >=72, hence d<=71)

Negative control (same object, excluded distance lowered by one to 71; must be rejected, and is):
matches object P_at_0: True ; matches object max: False ; q^k matches: True
CERT INVALID

## Propagation closure (own script, not shipped in this package, on the four neighbour rows in the-record-we-beat/neighbours.csv; each row is the live neighbour cell plus the rule's offset)
shorten 162 17 live ub 72 offset 0 -> implied 72
puncture 162 18 live ub 72 offset 1 -> implied 73
subcode 163 17 live ub 72 offset 0 -> implied 72
pad with a zero column 164 18 live ub 72 offset 0 -> implied 72
live ub 72 neighbour closure 72 claimed 71 strictly below closure: True
Open PR values were not consulted by this role (they belong to the novelty skeptic); the closure above is the four live neighbours only.

## Author's checker, run only after mine
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 72) and neighbour propagation
{"q": 2, "n": 163, "k": 18, "D": 72, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 72; new upper bound 71; best upper bound implied by the four live neighbours = 72 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement: the same f(0), the same maximum, same verdict. No mismatch.

## Notes

Scope: this role confirms that the certificate is a valid exact Delsarte dual certificate excluding d >= 72 for q^k = 262144, and that the new bound is below the four-neighbour closure. Currency of the live table is not judged here.

pass: true
