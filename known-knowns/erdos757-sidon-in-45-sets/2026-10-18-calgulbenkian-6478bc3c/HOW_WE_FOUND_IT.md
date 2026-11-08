contributor text, unverified

An AI search agent (Gemini, called Argon) working for the contributor calgulbenkian looked at the 14-element set of Ma and Tang, whose largest Sidon subset has 8 elements (ratio 4/7). It found that the structure of the 3-term progressions in that set splits into two similar 8-element shells. Gluing one extra 8-element shell onto it at a single shared point, and adding two progressions that cross between the blocks, gives 21 elements (14 + 8 - 1) whose largest Sidon subset has 12 elements. 12/21 is 4/7 again, but 21 is not a multiple of 14, which is what the "p1" partial win asks for.

It also reasoned (in `how-we-built-it/contributor_how_we_found_it.md`) that no (4,5)-set with fewer than 16 elements can beat 4/7. That argument has not been checked by the panel and is not claimed here. A search for a set strictly below 4/7 found nothing.

This is the same set as the contributor's earlier pull request 29, closed on 2026-10-14. The two-method check (including the ILP) was added on 2026-10-18 before the panel ran.
