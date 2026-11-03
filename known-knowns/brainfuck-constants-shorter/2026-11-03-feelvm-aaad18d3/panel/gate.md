# Honesty gate

status: CONFIRMED_PARTIAL
confirmed_scope: The 41-instruction program object/program.bf, started from all zeros, halts after 305379 steps with the pointer on cell 1 holding exactly 114514, never moves left of cell 0, never holds a negative cell, and 41 is strictly less than every instruction count listed for 114514 on the live esolangs Brainfuck constants page (58, 78, 92 numbered, plus unnumbered BF-RLE and CESU-8 blocks), literally satisfying the over-255 partial win for this one constant.

## Gate reasoning (main session, after reading all three panel files)

- REPRODUCE (context: subagent, pass: true): two independently written interpreters agree with the claim's
  checker on every property; the object file is byte-exact; the quoted 92/78/58 comparators were re-run.
- NOVELTY (context: subagent, pass: true): the named seed was tested literally — 18,854 trivial edits of the
  three published seed instances plus a closure over edits of all 1440 published strings on the page produced
  21 distinct 114514 programs, all of length 93–107 (edits of the cell's own 92), so no trivial edit of any
  published object gives the 41-instruction object; Sourcegraph found no copy of the object string and no
  `.bf` file with `114514`; the talk page has nothing in the last 24 months; the human-run authenticated
  GitHub code searches returned zero results. Recorded caveat: the wiki's `/w/index.php` history/search view
  returned 403 (one request, not retried), so older page revisions could not be checked; the gate accepts
  this because the status source itself was readable and fetched three times today with an identical sha256,
  and the page's stated convention is to list the shortest known sequences.
- CRITERION (context: subagent, pass: true): the object meets the full clause for n = 114514 under every
  reading of "smallest listed count" (58 all-listing minimum, 92 value-in-cell minimum, both non-soft
  competitors), one object, not a tie; `confirmed_scope` is exactly the CRITERION panelist's sentence.
- Downgrade checklist: no hedging panelist; no reproduction mismatch; strictly better than the live table;
  no stretched quantifier; scope not wider than reproduced; no sample presented as complete; the only capped
  search (run 1's affine family) is claimed as a family optimum, not as exhaustiveness, and the claim's
  "Not claimed" section disclaims minimality; no bundled objects (257/97104 remain unpanelled companions);
  no baseline to resolve (explicit-object target); the panel's table fetches are minutes old.
- The gate did not overturn any panel vote.
