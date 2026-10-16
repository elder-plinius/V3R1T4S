# Reproducible local-inference experiments

Use this card for a bounded local inference comparison. It is a protocol, not a claim that a configuration is faster or better. Keep raw prompt/answer records when permitted; redact secrets and private data. Do not publish personal data, proprietary prompts, model weights, or provider credentials.

## Freeze before running

1. Pin source revision, runner/runtime versions, model identifier and local artifact digest (if already available), hardware/software environment, and exact command. Do not download weights as part of this card.
2. Save one immutable request set and its SHA-256. Include prompt/input identifiers, input token counts, decoding parameters, and expected output quality rubric. Do not put sensitive prompt content in a public manifest.
3. Define baseline and intervention before observing results. Use the same requests, order, concurrency, warmup policy, and stopping rule for both. Record deviations and rerun both arms if the protocol changes.
4. Define a task-specific quality threshold and deterministic or blinded scoring method. Throughput is not an improvement if the quality gate fails.

## Record separately

For every request, retain raw answer or a content hash when retention is restricted, correctness/quality score, time-to-first-token, request latency, and end-to-end latency (including queueing and preprocessing). Report throughput (completed tokens or requests per unit time) separately from per-request latency. State token-counting convention, failures, timeouts, warmups, and excluded observations.

Summarize baseline and intervention with sample count, quality-gate result, median and p95 request latency, median and p95 end-to-end latency, and throughput. Provide the raw per-request table or a reproducible privacy-safe substitute, command output, source revision and artifact hashes. Do not infer a speedup from a single run or compare unmatched request sets. Report null/negative outcomes; do not claim an efficiency improvement unless the preregistered quality gate passes and the measured comparison supports it.

## Minimal manifest

See `INFERENCE_EXPERIMENT.json` for the required fields. Run the standard-library validator and tests before sharing. The zero-filled SHA-256 values in the JSON are placeholders and must be replaced with measured digests. The manifest validates bookkeeping only; it does not validate a model, benchmark design, or performance claim.
