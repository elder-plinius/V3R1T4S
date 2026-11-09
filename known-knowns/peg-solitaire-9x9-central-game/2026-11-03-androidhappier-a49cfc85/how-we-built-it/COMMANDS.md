# How the object was found (exact commands)

Programs here: beam9.c (the search that found sol31.txt; plain C, needs a compiler with `unsigned __int128`,
e.g. gcc or clang on 64-bit; no other headers or libraries), replay9.c (independent replay checker, the same file as
verify-it-yourself/replay9.c), PREREG.md (the run's pre-registration, frozen 2026-11-03T13:28:07Z).

Re-running the search is optional: the claim rests only on object/sol31.txt and the replay checkers.

```sh
cc -O2 -o beam9 beam9.c
# the run that produced the object (about 19 minutes and 1-2 GB RAM on one core; prints SOLVED moves=31 and the move list on stdout)
BEAM_V=2 BEAM_E=1 ./beam9 200000 1 > b200k_W1V2E1.out 2> b200k_W1V2E1.err
# smaller beams from the same run, for comparison:
BEAM_V=2 BEAM_E=1 ./beam9 20000 1    # SOLVED 34 moves (verify-it-yourself/fixtures/pos_beam_34.txt)
BEAM_V=2 BEAM_E=2 ./beam9 100000 1   # SOLVED 32 moves
```

Parameters: B = beam width (distinct D4-canonical boards kept per move layer), W = weight on filled Merson regions,
BEAM_V = isolated-peg penalty, BEAM_E = edge-peg penalty, BEAM_SEED default 0 (no noise). Each layer is the set of
boards reachable in one more move (any nonempty chain of jumps by one peg). The stdout move list after the first line,
`SOLVED moves=31`, is byte-for-byte the content of object/sol31.txt (`tail -n +2 b200k_W1V2E1.out`); check it with
`python3 ../verify-it-yourself/check9.py sol.txt` (after saving those lines as sol.txt).
