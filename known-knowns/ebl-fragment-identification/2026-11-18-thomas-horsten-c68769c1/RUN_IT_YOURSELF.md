# Run it yourself (fresh shell, from this folder)

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. It re-derives, with stdlib python3 only (no network, no
third-party packages), from this folder:
- the (b) top-hit alignment (frozen aligner, pure-python port of
  how-we-built-it/code/swalign.c): /L/3/10/Standard Babylonian/-, score 612, 270
  aligned signs, 9.26% mismatch, 24 consecutive lines, spans (3,26)/(56,66);
- the (b/attested) split (11/24 lines, 128/281 signs attested — the restoration
  pitfall, reported not hidden);
- the (c) frozen p-rule arithmetic from the saved K=1,000,000 null summary
  (p_raw = 1/1000001 = 9.99999e-07, p_bonf = 40 × p_raw = 3.999996e-05 < 1e-4,
  real 612 > control_max 46, 0 of 1,000,000 controls ≥ 612);
- the (d) eBL public ngram-matcher TF-IDF top-10 (re-implementation of commit
  e8918de), claimed chapter at rank 0;
- the (e) recurrence of the 24-line/297-sign block (exactly 1 unrelated textId,
  /L/1/1 Old Babylonian/I, threshold 118 < 5 ⇒ not a formula);
- the (a) unplaced-fragment rule (joins empty, no chapter manuscript link, no
  naming; genre-level 'lexical' partial flagged);
- the sha256 of every object file against the pins in the checker.

Rough laptop time: < 1 minute (stdlib only; two full-corpus alignment scans).

## Rebuild the object from scratch (how it was made; not needed to check it)

All inputs are pinned public eBL dumps + the frozen aligner; every RNG draw is seeded.

    # 1. the K=1,000,000 "line order shuffled" null (the 4 MB control array, ~35 min, 24 threads)
    cd how-we-built-it
    printf '["BM.68403"]' > fids.json
    python3 code/null_big2.py 1000000 fids.json 24
    #    (null_big2.py resolves its corpus from the run's data/ dir; to run it from this
    #    package, point it at object/corpus_toks.json + the fragment dump, or run it in the
    #    original run folder as recorded in the run's null_test.md 'command:' line)
    #    -> output/null_1000000_null_claimant.json.npz (control scores) + .json (summary)
    #    p computed per the frozen PREREG rule: p_raw=(1+n_ge)/(K+1), p_bonf=min(1, p_raw*N), N=40

Pinned input refs (sha256, from the run folder):
- corpus dump (228 chapters, 15,025,936 B): sha256 8c1edadb4e2fa9cc59af3cc99a5d947cb9d57b18455208b8fddaa208c71421f0
  (package ships the compact object/corpus_toks.json + corpus_signs.json; re-derivation
  from the raw dump gives the same aligned result)
- fragment bulk dump: sha256 8038665b1eb4c467d49c2ad46bd008544e84b0bac7dace24eebf856b6c77b26c
- eBL fragment record BM.68403 (2026-11-18 00:31 UTC fetch): sha256 373beff3f84f61283e8e9a909e0b77fd523bac73b3c45f26dfa05fd19d80f1fe
- frozen C aligner: sha256 2e92d05cad100bc0a65b49766b29056425db5d7d06c2ecbbd94d98d6bf627c9e
- the 4 MB control array (kept out of git): output/null_1000000_null_claimant.json.npz,
  4,000,532 B, sha256 dc61a3b121b7ef70 (see README.md "Large object files").

Deterministic: seed grid 20261117+k (np.random.default_rng(seed).permutation(11461),
corpus pool 11,461 lines / 124,324 tokens, sign content unchanged); aligner tie-break
frozen in swalign.c. ~35 min at 24 threads for the 1M-control null; the checker itself
runs in seconds.
