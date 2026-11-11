# Run it yourself

Everything here is Python standard library; no installs.

## 1. Verify the object

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (last line):

```
PASS
```

The script (a) checks the object file's byte count and character set, (b) runs the standalone checker
(`verify-it-yourself/checker.py`, ~305k executed instructions, step limit 10^7), (c) confirms the checker
rejects a deliberately corrupted copy of the object, and (d) re-prints the PASS line.

## 2. Expected checker line

```sh
python3 verify-it-yourself/checker.py object/program.bf 114514
```

```
PASS len=41 value=114514 steps=305379 mincell=0
```

## 3. What the checker implements

The definition, directly: unbounded tape to the right, cells hold arbitrary-precision integers (no 8-bit
wrapping — this is the page's own convention for constants above 255, the same one its listed 92-instruction
sequence uses), tape all zeros at start, pointer starts at cell 0 and may never move below it, and the
program must halt with the cell under the pointer holding exactly 114514.

## 4. Rebuild the object from scratch (optional)

The object came from a deterministic search over a one-loop fold family; the search code is in
how-we-built-it/. With the esolangs table saved locally, the same procedure regenerates candidates that are
then verified by the checker above. The authoritative check is always step 1: the explicit 41-byte string in
object/program.bf.
