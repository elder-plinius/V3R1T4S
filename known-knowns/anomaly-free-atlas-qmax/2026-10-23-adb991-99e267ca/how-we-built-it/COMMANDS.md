# How the object was built

Files here:
- `PREREG.md`: the run's pre-registration (criterion, rule and null-test decision, frozen 2026-10-18 05:56:28 UTC
  before any attack output). No null test: the claim is an exact count of explicit objects, each checked against the
  definition (no search statistic).
- `source/`: the claim's programs, unchanged: `acclist.c` (the lister that produced both lists), `count.c` and
  `count2.c` (raw counters, two different splits), `fix.py` (charge-conjugation-symmetric solutions, for Burnside)
  and `conventions.py` (turns raw counts into the candidate conventions; the published one is `prim_incl0`).
- `claim/`: the claim as the panel saw it (`CLAIM.md` with the six equations and the convention, `REPRODUCE.md`,
  `status.md`). `status.md` is the run's status record of 2026-10-18 (PENDING TABLE CHECK at the time); the
  table was read later from the owner-supplied PDFs (`the-record-we-beat/`).

The object `object/counts.txt` is the claim's file, unchanged. Commands used in the run (from the claim folder,
`claim/REPRODUCE.md`; the lens folders used the same programs):

```sh
gcc -O2 -o acclist source/acclist.c
gcc -O2 -o count source/count.c
gcc -O2 -o count2 source/count2.c
./acclist 11 0 | gzip -1 > SM_q11.txt.gz          # the stored object/SM_q11.txt.gz (sha256 of the stream: 723e21fb...)
./acclist 11 1 | gzip -1 > SMnuR_q11.txt.gz       # about 1 min, about 2.5 GB of memory (sha256 of the stream: f4e16ec8...)
python3 checker/check_list.py 11 0 SM_q11.txt.gz  # valid solutions: 37005, PASS
python3 checker/check_list.py 11 1 SMnuR_q11.txt.gz   # valid solutions: 45378377, PASS (about 15 min)
for q in $(seq 1 11); do ./count $q 0; done > N_sm.txt; (cd source && python3 conventions.py ../N_sm.txt 0)
for q in $(seq 1 11); do ./count $q 1; done > N_nu.txt; (cd source && python3 conventions.py ../N_nu.txt 1)
./count2 11 1; ./count2 11 0                       # same raw N as count: 90976848 and 74566
```

The checker `checker/check_list.py` of the run is `verify-it-yourself/check_list.py` here (same bytes). The `.gz`
hash depends on the gzip build; the sha256 of the uncompressed stream is the list's identity.
