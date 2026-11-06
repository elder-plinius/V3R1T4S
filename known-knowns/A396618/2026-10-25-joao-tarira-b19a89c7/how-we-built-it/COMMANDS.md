# Commands

The fast check does not use these search programs. It compiles
`verify-it-yourself/count.c`, which is the exact-square-root counter.

Historical counters, from this folder, with a C compiler that provides
`__int128`:

```
gcc -O2 -o search_table search_table.c -lm
gcc -O2 -o search_5adic search_5adic.c
gcc -O2 -o verify_sqrt verify_sqrt.c -lm
```

`search_table` is `search n part nparts` (the table counter that first
produced a(22) and a(23)). `search_5adic` is `search_5adic n part nparts`
(the 5-adic counter for a(24) and a(25); it also reproduces the earlier
terms). `verify_sqrt` is `verify_sqrt n part nparts` (the exact-square-root
counter whose saved halves add to a(24) and a(25)).

There is no PREREG file in the research record. The counters were required
to match the already published terms before a new term was kept.
