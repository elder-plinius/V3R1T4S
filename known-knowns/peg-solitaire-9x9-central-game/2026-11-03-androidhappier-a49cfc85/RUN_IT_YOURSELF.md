# Run it yourself

All commands from this folder, in a fresh shell. Needs python3 (standard library only); a C compiler is optional.

## 1. One command

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: the last line is `PASS` (seconds). Full expected output: verify-it-yourself/RECEIPTS.md.

## 2. The same checks by hand

```sh
sha256sum object/sol31.txt
# a49cfc85ce7d20bd828fd9f168fd3beea6d4bfb0fbe90df350944a85bd60093a  object/sol31.txt

python3 verify-it-yourself/check9.py object/sol31.txt --claim-max 33
# jumps=79 moves=31 pegs_left=1 final=e5
# VALID central game e5->e5 in 31 moves

cc -O2 -o replay9 verify-it-yourself/replay9.c && ./replay9 object/sol31.txt
# jumps=79 moves=31 left=1 centre=1
# PASS

# negatives must be rejected (non-zero exit, ILLEGAL or INVALID):
python3 verify-it-yourself/check9.py verify-it-yourself/fixtures/neg_diag.txt            # ILLEGAL (diagonal jump)
python3 verify-it-yourself/check9.py verify-it-yourself/fixtures/neg_occupied.txt        # ILLEGAL (jumps back over the hole just emptied)
python3 verify-it-yourself/check9.py verify-it-yourself/fixtures/neg_sol31_swapped.txt   # ILLEGAL (moves 3 and 4 swapped)
python3 verify-it-yourself/check9.py verify-it-yourself/fixtures/neg_sol31_truncated.txt # INVALID (last move removed)
python3 verify-it-yourself/check9.py verify-it-yourself/fixtures/neg_unfinished.txt      # INVALID (not one peg at e5)
# positive calibration (an earlier 34-move solution from the same search; ties Maye, not a win):
python3 verify-it-yourself/check9.py verify-it-yourself/fixtures/pos_beam_34.txt         # VALID ... in 34 moves
```

## 3. Rebuild the object (optional, about 19 minutes, 1-2 GB RAM)

```sh
cd how-we-built-it
cc -O2 -o beam9 beam9.c
BEAM_V=2 BEAM_E=1 ./beam9 200000 1 > b200k.out 2> b200k.err
tail -n +2 b200k.out | cmp - ../object/sol31.txt && echo identical
```

The first stdout line is `SOLVED moves=31`; the rest is byte-identical to object/sol31.txt. Details:
how-we-built-it/COMMANDS.md.
