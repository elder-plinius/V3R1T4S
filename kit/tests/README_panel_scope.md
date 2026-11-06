# Bind the gate scope to its CRITERION source

This focused change implements the existing RUN.md steps 6–7 contract:
CRITERION writes confirmed_scope, and the gate repeats that sentence exactly.
This consolidated proposal is based on upstream `8b5ba829baa4711791f2dda18e139ae2bd3beeff`.
It includes the confirmation/package gates and critical-field parser from fork PR2,
the manifest identity checks from fork PR6, and this panel-scope change from fork PR8.
Those dependencies are included together; do not reapply the old fork patches.
Merged PR30 diagnostics are preserved; the separate short-public-excerpt and receipt changes are not included.

## Mechanical boundary

Both files must supply one nonempty confirmed_scope. Missing, empty or duplicate
fields fail, including duplicate identical values. Compare the values returned by
the existing metadata parser, with no added normalization: case, punctuation and
internal whitespace must match. Existing kv() syntax strips surrounding whitespace
and edge Markdown backticks/asterisks, so this is equality of parsed metadata
values, not byte-for-byte file or raw-line equality. No scope is inferred from
prose, README, target descriptions, objects or another panel.

All confirmation paths use the same comparison:
- Open package: package panel/criterion.md and package panel/gate.md.
- Workspace: the chosen public or private CRITERION and that run's panel/gate.md.
- Envelope eligibility: a matching run target, that run's gate, and its chosen
  public or target-private CRITERION. Ambiguous target id fields cannot select a
  run. Confirmed workspace runs likewise reject ambiguous target ids; this does
  not add target-id validation to unconfirmed runs. A private panel does not need its own gate; if present, that gate is not
  authoritative for the run.

The existing public-before-private panel selection and any-matching-confirmed-run
lookup policies remain unchanged. This does not prove panel independence,
authenticate a target or object, establish scientific truth, or compare all
historical panels. It does not widen the confirmation status vocabulary.
PROMISING without a confirmation assertion remains allowed.

## Migration

Older test fixtures omitted criterion.confirmed_scope despite the documented
contract. The shared good-fixture builder now writes the scope into CRITERION,
and its commit-only fixture explicitly uses the matching private scope.

Real old records without that source field now fail confirmation. Do not fill it
automatically from gate/README: recover the actual CRITERION decision or obtain
a fresh panel decision under the existing workflow. This patch does not rewrite
historical submissions or infer their intended scope.

## Regressions

From repository root:
    python3 -m unittest discover -s kit/tests -p 'test_*.py' -v

Five entry paths cover two confirmed statuses and twelve cases each: exact match,
broader scope, changed case/internal spacing/punctuation, missing/empty/duplicate
criterion scope and missing/empty/duplicate gate scope. Additional cases cover
target mismatch/absence/duplicates and existing metadata framing equivalence.
Full private workspace and direct envelope controls have no private gate file.
The run-only case leaves the package's scope correct, isolating the workspace
gate check. Existing good/bad fixtures remain enabled.

All new fixtures are tiny and use --no-exec. The subprocess mock permits only
the fixture's read-only Git HEAD probe and raises on any other subprocess.
No submission scripts, scientific computations or external fetches run.

## Integration

Root SHA256SUMS is intentionally unchanged. Before integration, its maintainer
must reconcile complete path coverage and hashes against the final integrated
tree, including these tests/docs and other landed patches. Local tests and
partial source snapshots are not release-manifest validation.
