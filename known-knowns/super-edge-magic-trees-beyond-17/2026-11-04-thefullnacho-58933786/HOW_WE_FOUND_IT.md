# How we found it (contributor text, unverified)

The brief: the p1 package (pull request #917) had certified every tree on 18, 19 and 20 vertices. p2 asks for 22.
Orders 21 and 22 have 2,144,505 and 5,623,756 trees, about 9 times as many as 18 to 20 together, so this run moved
the same search onto a borrowed 32-thread desktop, capped at 16 low-priority processes so its owner never felt it.

The pipeline is the one that worked at n = 20, with the order of the stages flipped: an alpha-labeling search first
(every alpha-labeled tree is super edge-magic by a fixed relabeling), the randomised backtracker sem_direct on what
was left, the caterpillar construction of Enomoto, Llado, Nakamigawa and Ringel on what was left after that, and a
long sem_direct pass as a last resort. nauty gentreeg split each order into independent residue classes (1024 chunks
at n = 21, 2048 at n = 22), so every chunk could stop and resume on its own.

What we expected and what happened: we guessed alpha would carry most trees; at the budget used it labelled only
about a quarter, and sem_direct did the bulk. The deep last-resort stage saw a few trees per thousand chunks and
labelled them all. Nothing was left unlabelled at either order. n = 21 took about 36 minutes of wall time, n = 22
about two and a half hours, including one relaunch midway (done chunks are skipped on relaunch; the final coverage
count, not the chunk log, is what certifies the order).

Then the checking, which took longer than the search: the run's pre-registered coverage checker on the worker and
again on a second machine, a separate checker written from the definition with its own tree generator, and three
fresh-context skeptics who each wrote their own.
