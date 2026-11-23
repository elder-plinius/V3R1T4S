# How it was built

The construction code is not included. Argon's construction code from the contributor's laptop is not in our snapshot of that laptop (the snapshot holds a different quantum-code folder, which is about upper bounds and does not build these codes), so we cannot ship it, and no PREREG.md, command log or exact commands for this object are available to us. We say so plainly rather than reconstruct them.

Method, only as the claim folder documents it (these are the object file's own fields, unverified):

- The object's method field reads: Wedge-Kernel Zero-Conflict Extension of a [[64,53,4]] quantum code with 11 parity checks (r = 11).
- Each of the six codes keeps a subset of the base code's 64 columns (field c64_column_indices_0based) and adds two extension columns (extension_column_int_pair); the object also lists a zero-conflict subspace of eight 11-bit values (zero_conflict_f8_subspace_U3) and a four-element extension subspace (extension_2_subspace_W0).
- The object file credits the base code to "Dastbasteh et al., Quantum Twisted Codes". That attribution is unconfirmed: the novelty skeptic believes the base code is the quantum twisted code of the older literature (suspecting Bierbrauer and Edel) and could not confirm either name from a fetched source. We credit no author for the base code.
- The live codetables.de table itself lists a [[64,53,4]] quantum twisted code and, at the even lengths 38, 40, 44, 46, 48 and 50 with n - k = 11, codes derived from it by Markus Grassl (per the novelty report in panel/). The six odd lengths here are the gaps.

Nothing here is needed to check the claim: the object is explicit, and verify-it-yourself/ checks it from the definition.
