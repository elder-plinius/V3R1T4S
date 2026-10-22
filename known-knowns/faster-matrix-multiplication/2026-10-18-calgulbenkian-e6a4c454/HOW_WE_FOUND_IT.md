contributor text, unverified

# How we found it

Start: Perminov's published rational (Q) scheme `14x16x16_m2128_Q.json`, rank 2128. Inside it the agent looked for runs of 48 consecutive terms that together form a known small scheme for the format <4,4,4> over the rationals (rank 48), found 31 such runs, and replaced each run by an integer-coefficient scheme of the same small format with rank 49, which costs one or two extra multiplications per run (here 31 x 1 = 31). The result is valid over the integers and its rank is above the Q rank but below the integer rank in Perminov's table. After the substitution the scheme was passed through a flip-based reduction (seed 1337).

What the agent's notes document: the method text in `how-we-built-it/PREREG.md`, the script `how-we-built-it/tools/run_q_upgrades.py` and the construction line quoted in `how-we-built-it/README.md`. The run log of the commands is not in the snapshot.
