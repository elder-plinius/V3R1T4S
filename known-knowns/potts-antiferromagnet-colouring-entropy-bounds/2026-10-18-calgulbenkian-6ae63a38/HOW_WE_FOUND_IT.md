contributor text, unverified

# How we found it

The brief was one target from the bank: the zero-temperature entropy of the q-state Potts antiferromagnet, that is the growth rate W_sq(q) of proper
q-colourings of the square grid, where Lundow and Markstrom (2008) give rigorous bounds from transfer matrices of cycles up to C_16 (q = 4) and C_12 (q = 5).
The bank text said larger transfer matrices with symmetry compression were laptop-reachable. The contributor's search agent, Argon, took the target on 2026-10-18 with a
pre-registration (how-we-built-it/PREREG.md).

What worked: a matrix-free product with the orbit-quotient transfer matrix, built site by site, so that the quotient matrix (more than 85 percent dense) is never stored.
That reached the cycle C_%(m)d for %(q)d colours (%(states)s states, %(orbits)s orbits). A power iteration with a precision ladder produced a positive vector v;
then y = C v was computed exactly in 256-bit integers and the bound read off from the largest ratio y_i / v_i.

What failed or was wrong: the snapshot records one wrong table entry (the q = 4 open strip of width 3), which does not matter here, and it does not record a
failure log. The claim folder cited the key inequality as "Theorem 2.2" of the paper; the panel found the correct label is equation (6). The first criterion run of the panel could not
read the paper (abstract only) and failed; the second run read it and passed. The snapshot gives no run times and no command log for this width.

The orchestrator that passed the claim to the panel did not run a checker of its own on the large file; the panel's reproduce skeptic did, with its own program,
on the full transfer matrix.
