Code that produced object/scu881.txt (paths shown as .; needs numpy, scipy, mpmath).
Same method as the N=882, 883, 884, 886 claims (draft PRs #235-#238). Chain from Lu Peng's posted scu880.txt (Packomania scu_coords.tar.gz): python3 chain.py ./data/coords/scu880.txt 880 12 400 out/chain880  (inserts one sphere at the largest hole found by hole.py, penalty-inflates with plib.py, saves scu<N>_chain.txt).
Preregistration: PREREG.md.
