# Run it yourself

From this folder, in a fresh shell (Python 3.9 or newer, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output ends with:

```
FULL_GAME_COMPLETENESS: PASS
PASS
```

Equivalent direct call: `cd verify-it-yourself && python3 verify_completeness.py ../object`. The other modules in that
folder (`verify_no_initial_bet.py`, `verify_conditional_family.py`, `verify_normalization.py`, `verify_full_open.py`,
`verify_reduction.py`, `verify_offpath_k.py`, `exact_kuhn.py`, `family.py`) are imported by it.
