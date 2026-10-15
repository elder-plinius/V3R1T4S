# Game and quantity to check

Source: Angel Y. He and Mark Holmes, *All In: Give me your money!*, arXiv:2410.15329v1, abstract and Section 1; the comparison is Conjecture 9 in Section 5.3. A saved source copy is in data/paper.pdf and data/paper.txt.

Start with three strictly positive real stacks (x,y,z). Independently at each round, choose one of the three unordered pairs with probability 1/3 and choose which member wins with probability 1/2. The loser transfers the smaller of the two pre-round stacks to the winner. Stop at the first zero stack. The function f(x,y,z) is the probability that player 1 is the player eliminated at that stopping time.

The theorem to check is f(x,y,z)>f(y,y,z) for every positive real x,y,z with x<y. This changes the first initial stack while preserving the other two. It does not swap the players' stacks and does not preserve the total initial stack.

The checker must cover arbitrary real ratios and all admissible equality cases z=x and z=y. The exact criterion and enumerated partial win are copied in target.md.
