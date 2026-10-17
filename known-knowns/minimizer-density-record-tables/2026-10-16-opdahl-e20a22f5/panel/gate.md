status: CONFIRMED_SOLUTION
confirmed_scope: The minimizer order [3,4,1,0,5,6,2,7] for (w=12, k=3), evaluated with the published notebook's own rank composition, has mean density 0.136644513466 at n=2,000,000 over seeds 0,1,2, which is strictly lower than the smallest value listed for that cell in k_extension_k16_w12.csv (0.138389448, angle-based) by 1.2609% relative, exceeding the required 0.5% margin.

claim level: solution_claim (three-skeptic panel: 3 pass, 1 refuted dissent on record)

## Panel record

| skeptic | verdict | file |
|---|---|---|
| REPRODUCE (attempt 2) | pass: true | panel/reproduce.md |
| NOVELTY | pass: true | panel/novelty.md |
| CRITERION | pass: true | panel/criterion.md |
| REPRODUCE (attempt 1) | pass: false | panel/reproduce.attempt1.md (preserved, refuted) |

DISCLOSURE - the REPRODUCE verdict required a second attempt. Attempt 1 returned pass: false claiming
the notebook's composition yields density 0.984363938763 for both orders. That finding was verified
unreproducible BEFORE the retry was dispatched, by an independent implementation run by the operator
(n=2,000,000, seeds 0-2): every composition tested returns ~0.1388 for GreedyMini, matching the
published table. Attempt 2 identifies attempt 1's error: it ignored the order[p] << 30 term that
dominates across projection groups. Both attempts are on disk; nothing was deleted or overwritten.

## Corrections applied by this gate

1. Baseline. The claim states the smallest listed value for (w=12, k=3) is 0.138843 (GreedyMini). The
   smallest is angle-based at 0.138389448. Both passing skeptics found this independently. Margin
   corrected from 1.7193% (against GreedyMini) to 1.2609% (against the true smallest).
2. The claim's stated 1.622% figure matches no comparison and is withdrawn.

## Open defect - the shipped checker does not use the repository's code

The success criterion requires the density to be "computed by the skeptic with the repositories' own
density measurement code". The notebook specifies:
    rank = (((order[bin_kmer] << (2*k)) + kmer) << (8*k)) + get_kmer_id_dna(k, km, seed)
with the HIGH-bit projection (bit = (nuc >> 1) & 1, i.e. bits 5,3,1 for k=3).
The package's checker.py uses a LOW-bit projection and drops the "+ kmer" term. Measured side by side
at n=2,000,000 over seeds 0,1,2:

| composition | GreedyMini | claimed order | margin |
|---|---|---|---|
| notebook's own (high-bit, with +kmer) | 0.138882000041 | 0.136644513466 | -1.2609% |
| shipped checker (low-bit, no +kmer) | 0.138843000275 | 0.136447347983 | -1.7254% |

The claim holds under the repository's own composition, which is the one the criterion names, and the
confirmed_scope above states that measurement. But the shipped checker.py must be replaced with one
implementing the notebook's composition before any submission, so that a third party re-running the
package gets the number in the confirmed_scope. NOT PACKAGED until that is done.

## Determinism

Two runs with seed 0 at n=100,000 gave identical density. order.txt is a valid 8-entry permutation of
[0..7]. The incumbent w12_k3.gm order [8,2,8,8,0,1,4,3] is not a permutation of [0..7] (8 appears three
times); ranks may repeat, so this is not an error, but it is worth a skeptic's attention.
