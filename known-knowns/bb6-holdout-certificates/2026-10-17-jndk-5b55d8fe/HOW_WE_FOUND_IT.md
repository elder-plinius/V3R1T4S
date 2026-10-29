# How we found it (contributor text, unverified)

V3R1T4S agents picked 663 #523, an undocumented "Quadratic Mess" holdout, while scanning the BB(6) holdout list for
machines with simple run-length structure. One run found seven universal transfer identities by reading
traces of the tape in run-length form; later runs wrote an independent symbolic checker (context-carrying block
shifts proved by induction on the number of copies, plus induction on k for the quadratic drains) and a C replay
that checks every occurrence of every rule's input pattern in the first 1e8 steps.

What failed along the way: a proposed "no 00" invariant (false after 12 steps); plain one-copy shift rules (each copy
reads two cells ahead, so the shifts must carry context); a Python replay (too slow for 1e8 steps); and two panels
whose gates stopped at PROMISING, first for stale proof text and an exponent-parser hole (both repaired), then for
an unread community channel, which the workspace human then searched by hand.

The rules cover about 99.98% of the first 1e8 steps. Toward a full reduction, later work (not part of this package)
found further proved rules and a drain/reset structure, but the halting question stays open.
