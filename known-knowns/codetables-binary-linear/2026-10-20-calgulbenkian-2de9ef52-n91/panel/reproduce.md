context: Claude Code subagent, fresh context [Sonnet 5.5]

# reproduce: qecc-n91-k73-d5

Hash check: sha256sum -c against the contributor's hash list, run from inside the package folder, all files OK.

## Definition used
A qubit stabilizer code [[n,k,d]] is given by r = n-k independent, pairwise commuting (symplectic product 0) Pauli generators; d is the minimum weight of a Pauli that commutes with all generators but is not in the stabilizer span (pure distance: minimum weight of any nonidentity normalizer element). The claim (p1) asks for d strictly above the table's lower bound 4; I judge only the code properties here, not the table value or novelty.

## My checker (written before reading verify-it-yourself/)
Own script (not shipped in this package). Exact integer bit arithmetic, no sampling:
1. Rows HX, HZ are 0/1 and of length n; the Pauli strings agree with HX/HZ symbol by symbol.
2. All generator pairs have symplectic product 0 (commute).
3. GF(2) rank of the 2n-bit vectors equals r, so k = n - rank.
4. All 1 + 3n + 9*C(n,2) Pauli errors of weight at most 2 have pairwise distinct syndromes (collisions = 0). Hence no nonidentity Pauli of weight 1 to 4 commutes with every generator: normalizer minimum weight is at least 5 (so d >= 5, pure).
5. Weight-5 normalizer elements are found exhaustively by meeting in the middle (weight-3 error vs a disjoint weight-2 error with equal syndrome); the first one found is tested against the stabilizer span by GF(2) reduction and is outside it. So a weight-5 logical operator exists and d = 5 exactly (d = 6 excluded).

## Output (full, from its output)
{'n': 91, 'k': 73, 'r': 18, 'n_minus_rank': 73, 'rank': 18, 'commute': True, 'errors': 37129, 'expect': 37129, 'collisions': 0, 'w5_pairs': 441570, 'logical_w5': ((0, 1), (1, 3), (2, 1), (72, 2), (73, 2))}
PASS

(w5_pairs counts matched weight-3/weight-2 syndrome pairs; each weight-5 normalizer element is counted once per way of splitting it 3+2.)

## Determinism
Ran the whole battery twice; outputs byte-identical.

## Author's checker (run only after mine)
sh verify-it-yourself/run_checks.sh, last lines:
== negative control: a copy with one bit of the first X row flipped must FAIL
negative control rejected as expected: RESULT FAIL [[91,73,None]] live [4,6]
ALL CHECKS PASS
exit 0
It agrees with my result, including the negative control being rejected. No mismatch.

## Verdict
All properties confirmed for [[91,73,5]]: commuting, rank 18 = n-k, pure distance at least 5, a weight-5 logical outside the stabilizer, so d = 5 exactly. This report does not judge table currency or novelty.

pass: true
