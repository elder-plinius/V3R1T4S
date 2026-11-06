# Commands (from the harvest run folder; RUN_DIR is that folder)

Environment: Python 3.13 venv with python-lifelib 2.5.6, numpy, tqdm; Shinjuku at data/Shinjuku (commit
3615babf001146507a1e9ec901cb3eabba9f5fd0). All jobs ran with nice -n 19.

1. Sweep (5 shards; this object came from shard 3):
   `LT_MEM=150 nice -n 19 venv/bin/python code/sweep1g.py --inputs attempts/sweep1g/inputs_xs24-28.txt --shard 3 --nshards 5 --out attempts/sweep1g/out_3.txt`
   Output line (data/sweep1g_out_3_hits.txt): `xs28_651ugmmz69706221 11 2 10 0 1 xs26_08ehmkk8z6a87066`
2. Lookup against cached Catagolue cost tables (code/lookup1g.py) gave the candidate line in
   data/candidate_line_1105a_new.txt: `IMPROVE xs26_08ehmkk8z6a87066 new 12 cur 58 from xs28_651ugmmz69706221 11 rot 2 lane 10 ph 0 per 1`
3. Shinjuku route of the input (code/extract_paths.py writes attempts/multistage/paths.json; the entry used is
   data/paths_entry_xs28_651ugmmz69706221.json, 3 stages, 11 gliders).
4. Stitch and verify (code/batch_ms2.sh on the candidate file; for this object the first try, pre 32, won):
   `nice -n 19 venv/bin/python code/compose_ms.py --in-apg xs28_651ugmmz69706221 --rot 2 --lane 10 --ph 0 --target xs26_08ehmkk8z6a87066 --out attempts/compose_tmp/xs26_08ehmkk8z6a87066.p32.rle --pre 32`
   `nice -n 19 venv/bin/python code/verify_synthesis.py --rle attempts/compose_tmp/xs26_08ehmkk8z6a87066.p32.rle --target xs26_08ehmkk8z6a87066 --out attempts/compose_tmp/xs26_08ehmkk8z6a87066.p32.json`
   Logs: data/xs26_08ehmkk8z6a87066.p32.mlog, data/xs26_08ehmkk8z6a87066.p32.json. The stitched RLE is byte-identical to object/xs26_08ehmkk8z6a87066.rle.
The only change to the copied code is the first `cd` line of batch_ms2.sh, whose absolute path was replaced by RUN_DIR.
