# Commands

The fast check is pure Python and only inspects the two witnesses. The C
files are the search programs from the research record. They are not run
by `sh verify-it-yourself/run_checks.sh`.

```
gcc -O2 -o search_a20 search_a20.c
gcc -O2 -o vf_a20 vf_a20.c
gcc -O2 -o search_a21 search_a21.c
gcc -O2 -o search_witness search_witness.c
gcc -O2 -o vf_a21 vf_a21.c
```

The historical exhaustive runs ask each program for a fixed number of marks,
a fixed diameter, and the earlier terms as span lower bounds. NONE on
diameters 51 through 55 (20 marks) and 57 through 61 (21 marks) is the
saved record. The 21-mark diameter-61 run is on the order of a few hours
on two cores.

There is no PREREG file in the research record. Both the left-to-right and
the right-to-left searches were required to reproduce a(3) through a(19)
before a(20) was kept, and a(20) was an input to the a(21) run.
