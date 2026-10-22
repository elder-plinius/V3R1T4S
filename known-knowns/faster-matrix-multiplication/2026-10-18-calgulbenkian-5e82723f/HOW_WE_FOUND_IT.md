contributor text, unverified

# How we found it

Start: Perminov's published rational (Q) scheme `12x14x14_m1449_Q.json`, rank 1449. Inside it the agent looked for runs of 63 consecutive terms that together form a known small scheme for the format <3,4,7> over the rationals (rank 63), found 23 such runs, and replaced each run by an integer-coefficient scheme of the same small format with rank 64, which costs one or two extra multiplications per run (here 23 x 1 = 23). The result is valid over the integers and its rank is above the Q rank but below the integer rank in Perminov's table. After the substitution the scheme was passed through a flip-based reduction (seed 1337).

What the agent's notes document: the method text in `how-we-built-it/PREREG.md`, the script `how-we-built-it/tools/run_q_upgrades.py` and the construction line quoted in `how-we-built-it/README.md`. The run log of the commands is not in the snapshot.
