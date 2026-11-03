# How the object was built (commands, relative to this folder)

The seed: seed_Z2cubed_latin_n8.prefs is the order-8 Latin instance of Z2^3. Man m ranks woman w at position (m xor w)+1, and the woman ranks him at 9 minus that position. It has 268 stable matchings. seed_ext9.prefs is the order-9 start file, with 268 stable matchings. It was made by appending a 9th man and woman at the bottom of every old list and giving them random lists of their own (latext.py SEED, or ext1.py on the order-8 file). The RNG seed for that file was not recorded, so the exact file is shipped here.

```sh
cc -O2 -o smcount3 smcount3.c -lm
./smcount3 count seed_ext9.prefs 1                                  # 268
./smcount3 climb 9 seed_ext9.prefs 951 7000 lat_n9_s951 2000 2      # iterated local search; best file lat_n9_s951.best.prefs
# run log: 268 -> 382 at t=59 s -> 412 at t=177 s (342858 exact evaluations); the 7000 s run and re-seeded books 961/962
# plus an anneal (seed 963) from the 412 file found nothing higher.
./smcount3 count lat_n9_s951.best.prefs 1                           # 412
```

Timing depends on the machine, so a rerun with the same seed should follow the same trajectory but at a different speed. The packaged object is that best file with only its comment line rewritten.
