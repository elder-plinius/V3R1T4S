# CRITERION

context: comparison of the saved NONE logs and the two witness enumerations to the A390087 and A390085 definitions, while assembling this package

a(8) = 39 means some irreducible odd zero-sum set of length 16 fits in k = 39, and none of length 16 or more fits in any smaller k. The witness gives the first half. The length-16 NONE log through magnitude 75, plus the length 18 through 38 NONE log through magnitude 77, gives the second half. a(9) = 48 is the same shape one step later: a length-18 witness at magnitude 95, length 18 NONE through magnitude 93, and lengths 20 through 48 NONE through magnitude 95.

A390085 on 31 through 48 is not a second search. It is what those existence and non-existence statements say, using that A390085(30) = 7 is already published and that the function does not decrease when k grows.

The witnesses were checked again by enumerating subsets, which does not use the search pruning. The non-existence statements use that pruning. The research notes justify it: a nontrivial subset-sum collision at a partial assignment remains a proper zero-sum subset after later elements are added. Two further implementations agreed on overlapping ranges, including node counts. That is the evidence. It is not a formal proof that every possible pruning bug is absent.

confirmed_scope: A390087(8) = 39 and A390087(9) = 48, so A390085(31) through A390085(38) = 7, A390085(39) through A390085(47) = 8, and A390085(48) = 9, from explicit irreducible odd zero-sum witnesses of lengths 16 and 18 and from saved exhaustive searches that found no shorter index, past the OEIS b-files ending at A390087(7) = 30 and A390085(30) = 7.

pass: true
