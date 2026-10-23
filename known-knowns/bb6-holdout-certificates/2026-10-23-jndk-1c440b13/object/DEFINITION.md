# Definition of the restricted counter recurrence

## Exact integer-counter state

A state has phase `front` or `sweep`, a nearest-first finite left stack `(g,b)` with gap `g` and positive ones length `b`, and a right leading-zero count `z` followed by a finite stack `(b,g)` of positive ones lengths and following gaps. Final right gap `None` denotes infinite blank padding. Empty right support has `z=None`. First left gap may be zero; subsequent left gaps are positive. All counters are integers with no upper bound.

Head is at coordinate zero and reads zero. Left pair `(g,b)` denotes `g` zeros then `b` ones moving left from the preceding edge. Right z includes the current zero; right tokens proceed rightward. Exact reconstruction is a finite union of integer ones intervals. The implementation splices those integer intervals without allocating one item per tape cell. `counter_data.py` supplies wellformedness, encode/decode and the restricted language. `counter_core.py` contains the recurrence and no TM transition table, binary-stack integer encoding or fallback simulator.

The blank start is `front,left=[],right={z:None,tokens:[]}`.

## Restricted right language

All finite internal right gaps are one or two. In `sweep`, right support is nonempty, z=1 and every token with following gap one has length at least two. In `front`, empty right support is allowed. If z=2 or3, every right token is typed by the same gap-one condition. If z=1, an ordinary front block of size at least two is allowed, as is front size one followed by a gap of at least two (a terminal prestate). The remaining front scaffold is `(1,1),(c,g),pending`, with active c>=1; the marker and active counter are exempt, and all pending tokens are typed. The c=1,g=1 front exception is explicit. No bound is placed on left gaps or left block lengths.

## Semantic macro identities

Here `[A]` and `[C]` identify the original semantics corresponding to counter phases front/sweep, solely to state the semantic proof obligations. All unmentioned left and right contexts are arbitrary and retained. All times count defined transitions. A final F0 is terminal; no undefined attempt is counted.

| Counter rule | Protected symbolic word identity | Time | Head displacement |
|---|---|---:|---:|
| ZERO | `0 1^M [A]00 -> [S]0 1^(M+2)`, M>=0; S=A for even M, C for odd M | M+3 | -M-1 |
| TRANSFER | `0 1^M [A]0 1^n00 -> [S]0 1^(M+n-2)00111`, M>=0,n>=2; S=A iff M+n even | 6n-3+M | -M-1 |
| SCAN | `[A]0 1^n0 -> 1^(n-1)01 [A]0`, n>=2 | 5n-7 | n+1 |
| C_adj | `0 1^b [C]0 -> [S]0 1^(b-1)00`, b>=1; S=A for odd b, C for even b | b+1 | -b-1 |
| C_iso | `0 1^b0 [C]0 -> [S]0 1^(b+1)0`, b>=1; S=A for even b, C for odd b | b+2 | -b-2 |
| C_END | `00 [C]0 -> [A]010` | 2 | -2 |
| D1_FOLD | `[A]0101 0^g1^b -> 1^g [A]0101^(b+1)`, g,b>=1 | 7g | g |
| D1_TRAVEL | right `0101` then all blank -> prepend left one, same right `0101` | 7 | 1 |
| D3_FOLD | `[A]01011100 -> 10 [A]010111` | 12 | 2 |
| D3_GAP1 | `[A]0101110 -> 100001 [A]0` | 6 | 6 |
| D_SEED | `[A]0101111 -> 1000 [A]011` | 8 | 4 |
| HALT_FRONT1 | `[A]0100 -> 100 [F]0` | 3 | 3 |
| HALT_D2 | `[A]0101100 -> 100000 [F]0` | 6 | 6 |

D3_FOLD also supplies the positive twelve-step travelling step when its right support ends after the three ones. D1/D3 travelling steps remain `NEXT` with their actual updated left stack; no approximate terminal output is used.

## Counter carry

At D active size2 with following gap1, clear the initial `101` right prefix and enter a run cursor. The cursor has a singleton remaining block. If it is followed by a gap1, clear that singleton, its zero gap, and the first one of the next block, then advance by three. This decreases the remaining run stack: a next size2/gap1 continues with a singleton; all other sizes exit. The final block has an infinite gap, so the loop cannot continue forever on a finite counter state.

A next size1 exits through the fixed B0 path and produces a D1 scaffold; because pending gap1 singletons are forbidden by the restricted grammar, its following gap is2 or infinite. A next size3 exits on its following zero, producing leading z1, z2, or empty right support. A next size at least4 exits with ordinary active size b-2>=2. A next size2 followed by gap2 or infinite is the carry halting terminal. Context-audit's independent fixed-window affine proofs check these exits and the continuing three-step path.

No branch reads an unknown left exterior during carry: the cleared prefix supplies every left bit needed by the B0 exit or the final two-step A/C normalization.

## Explicit arithmetic terminal condition

For a restricted counter state the halting macro occurs exactly when either:

1. Its phase is front, z=1, and its first block has size1 followed by gap2 or infinite padding; or
2. Its phase is front, z=1, and it is the D scaffold; starting at the active counter, a finite prefix has the form `(2,1)^r (2,2-or-infinite)`, r>=0.

The first case takes three defined transitions. The second takes `3r+6`, with the same rightward displacement. Thus halting from blank is the existence of an iterate satisfying one of these two explicit run-counter patterns, provided the universal semantic and grammar-preservation proof is fully bound to the implementation. Neither pattern contains the original F0 predicate or a generic bit-stack residue.

The recurrence does not decide whether such an iterate exists. Positive time on every macro prevents Zeno skipping. The inner carry and finite gap folds terminate by finite run count/positive gap; other updates use integer formulas and finite list operations.

