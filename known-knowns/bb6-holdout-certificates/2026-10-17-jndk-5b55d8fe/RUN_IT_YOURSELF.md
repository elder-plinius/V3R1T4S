# Run it yourself

From this folder, in a fresh shell (Python 3 with sympy, a C compiler):

    sh verify-it-yourself/run_checks.sh            # or: PYTHON=/path/to/python3 sh verify-it-yourself/run_checks.sh

Expected output (see verify-it-yourself/RECEIPTS.md):

    symbolic proofs: 7 of 7 PROVED
    all controls rejected: True
    parser test pass: True
    all real pass: True
    all mutants caught: True
    BB(5) champion: 47176869 defined transitions, then halt
    TOTAL scheduled=8365935 passed=8365935 failures=0
    replay controls (steps+1, flipped bit): passed=0, passed=0
    PASS

What each step does:
1. verify-it-yourself/prove.py + main_proofs.py: symbolic proof of every rule in object/rules.json for all parameter
   values (linear rules by block-copy induction, the three drains by induction on k).
2. main_controls.py: 12 mutated rules and proof plans, all of which must be rejected.
3. parser_test.py: the rule parser rejects exponents or step counts in any symbol other than k.
4. bruteforce.py: an independent naive window simulator (Python standard library), k up to 12, random exteriors.
5. replay_v2.c: naive single-step simulation from the blank tape; every occurrence of every rule's input pattern
   starting at t <= 1e8 is checked at t+steps (state, head, full window); controls with wrong step counts or a
   flipped bit must pass 0 times. It is first validated on the BB(5) champion.

Rebuilding the object: object/rules.json is the checked part of the panelled claim's rules file; the free-text proof
descriptions are in how-we-built-it/proof_notes.json. The notes evidence can be re-derived with
how-we-built-it/notes_check.py on freshly fetched pages (see the-record-we-beat/record.md for the URLs).
