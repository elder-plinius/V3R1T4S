contributor text, unverified

# How we found it

Start: Perminov's published rational (Q) scheme `9x12x16_m1035_Q.json`, rank 1035. Inside it the agent looked for runs of 40 consecutive terms that together form a known small scheme for the format <3,3,6> over the rationals (rank 40), found 15 such runs, and replaced each run by an integer-coefficient scheme of the same small format with rank 42, which costs one or two extra multiplications per run (here 15 x 2 = 30). The result is valid over the integers and its rank is above the Q rank but below the integer rank in Perminov's table. After the substitution the scheme was passed through a flip-based reduction (seed 1337).

What the agent's notes document: the method text in `how-we-built-it/PREREG.md`, the script `how-we-built-it/tools/run_q_upgrades.py` and the construction line quoted in `how-we-built-it/README.md`. The run log of the commands is not in the snapshot.
