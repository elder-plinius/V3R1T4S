# How we built it
mc2w.c: min-conflicts local search over m vectors of length n (cost = number of colliding pair-ORs). Random vectors and
moves have weight MC2W (here 4), but single bit flips are allowed, so weights can drift. It writes the family only at
cost 0 and is deterministic given its seed. ladder_W16.log is the run's ladder log (paths relative; 600 s per attempt;
m = 93..100 found, four failed tries at 101, then seed 360013 from a random start found 101 at 2026-10-19T19:27:43Z and
seed 360014, warm-started from that 101 plus one random vector, found 102 at 19:27:44Z). W16_*.log are the two
programs' own logs. parent_W16_n16_m101_s360013.txt is the 101-family the 102 grew from.
Rebuild byte for byte (C compiler; from this package folder, about 1 to 15 minutes):
  mkdir -p work && gcc -O2 -o work/mc2w how-we-built-it/mc2w.c -lm
  MC2W=4 work/mc2w 16 101 900 360013 work/regen101 | tail -1
  cmp work/regen101 how-we-built-it/parent_W16_n16_m101_s360013.txt && echo "cmp101: identical"
  MC2W=4 work/mc2w 16 102 120 360014 work/regen102 work/regen101 | tail -1
  cmp work/regen102 object/A054961_n16_m102.txt && echo "cmp102: identical"
structure_check.py prints the weight profile and column sums. PREREG.md is the run's preregistration, frozen
2026-10-19T17:47:37Z (B(16) = 92, budget end 20:47:37Z). null_test: not needed (explicit object, deterministic checker).
