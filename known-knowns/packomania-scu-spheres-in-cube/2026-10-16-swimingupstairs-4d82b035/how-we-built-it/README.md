Code that produced object/scu884.txt and object/scu881.txt (needs numpy, scipy, mpmath). The same method produced the N=886 claim (#238, merged).
Chain from Lu Peng's posted scu880.txt (Packomania scu_coords.tar.gz): python3 chain.py ./data/coords/scu880.txt 880 12 400 out/chain880  (inserts one sphere at the largest hole found by hole.py, penalty-inflates with plib.py, saves scu<N>_chain.txt). object/scu881.txt is the chain step after one insertion; object/scu884.txt after four.
Preregistration: PREREG.md.
