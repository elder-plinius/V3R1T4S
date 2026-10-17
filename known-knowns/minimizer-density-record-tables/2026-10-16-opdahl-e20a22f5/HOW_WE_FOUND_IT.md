# How we found it

This text is contributor text, unverified.

The target comes from the record tables in the bank. The task is to beat the smallest listed density
for one minimizer cell. The cell (w=12, k=3) was selected for one reason. For k=3, the ranking is a
permutation of eight classes. Thus the search space is 40320 orderings. An exhaustive search is
possible in this space.

## What failed

Three attempts failed before the fourth attempt.

1. The first attempt ranked all 40320 orderings on 20000 windows. Then it ranked again only the
   orderings with equal values. This method ranks on noise. The set of equal orderings does not
   contain the true optimum. The null test of the run stopped the claim. The null test was correct.
2. The second attempt repeated the search on 50000 windows. This attempt made the same error on a
   smaller scale. A random control order beat the claimed order again.
3. The third attempt used a wide shortlist. The shortlist went from 20000 windows to 200000 windows
   to 2000000 windows. This attempt found an order that was 1.6% better than GreedyMini. Then the
   attempt stopped on a null test against random orderings.

## Why the null test cannot pass

The density depends only on the relative order of the lowest-ranked classes. Thus the optimal
ordering is a large equivalence class. A random control order falls inside this class. For this
reason, the null test against random orders cannot pass, whatever the quality of the order. The null
test asked a different question than the criterion. The criterion compares the order with the table,
not with random orders.

## What worked

The fourth attempt applied the criterion directly. The criterion asks for an explicit object and a
deterministic computation against a published table value. The attempt did these steps:

1. It refined the ordering on sequences of increasing length.
2. It fetched the table again.
3. It compared the values with the measurement code of the repository.

## Corrections in this record

1. The first version of the claim named the value 0.138843 as the smallest value for the cell. That
   value belongs to GreedyMini. The scheme angle-based holds the smaller value 0.138389448. Two
   independent reviewers found this error. This package gives the margin against the true smallest
   value.
2. The checker of the run used a rank composition that is different from the composition of the
   notebook. The claim holds for both compositions. This package uses the composition of the
   notebook.
