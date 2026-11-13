# Run it yourself

From the package directory in a fresh shell:

`sh verify-it-yourself/run_checks.sh`

Python 3 standard library only, no account or network. Final line PASS.
Expected: population 35, 7 gliders; rewind T=852 and 1180; exact repeat from 759, period 1,
population 28, exact target and no debris; exact strict partition test passes.
The semantic checker measured less than one second locally. The actual RLE and hash are checked;
an altered object must FAIL/nonzero. Live table absence is a dated record, not rerun offline.
Before a new public claim re-fetch xs28 table and object honestly and stop on block or new listing.
See how-we-built-it/COMMANDS.md for optional reconstruction using separately supplied Shinjuku.

Pinned kit automatic corruption warning: .rle is not in its text-extension list. Manual mutated-RLE controls reject both by wrapper and directly by semantic checker; see verify-it-yourself/NEGATIVE_CONTROL.md. The warning is retained, not hidden or fixed around.
