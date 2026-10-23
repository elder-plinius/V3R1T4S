# Semantic corruption controls

The mathematical object in object/scheme.json is the unchanged confirmed object. Corrupted controls are deliberately invalid copies constructed in memory; they are never replacements for that object.

Run `python3 verify-it-yourself/semantic_controls.py` from this package directory. The same command is included in run_checks.sh. It calls the two unchanged mathematical checker implementations directly, bypassing pinned-object checksum checks. The original must pass both. Two fixed output-sign changes must be rejected, with an actual tensor/basis mismatch required for the whole-output sign change. Four additional cases alter cost metadata, use an out-of-range reference, set the wrong ring flag, or remove a product; the independent checker must reject each with a relevant semantic/schema diagnostic. Every fixture remains valid JSON.

The saved semantic-controls.json receipt contains the actual results, diagnostic counts/errors, fixture hashes, and unchanged original/checker hashes. This is a finite set of regression controls, not a guarantee of exhaustive fault detection or a new skeptical panel. No mathematical object or checker implementation was corrected or replaced.

The initial reporting harness failed to recognise the checker message "candidate must operate over Z" as the expected wrong-ring rejection. It reported that case as a control failure even though the mathematical checker rejected the object correctly. The original harness and receipt are retained in semantic-controls-history. The current harness recognises that exact diagnostic. No mathematical checker, case, fixture or observed checker outcome changed; the saved final receipt records the classification correction.
