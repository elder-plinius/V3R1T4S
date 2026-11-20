# Commands (from the harvest run folder; RUN_DIR is that folder)

Environment: Python 3.13 venv with python-lifelib 2.5.6, numpy, tqdm; Shinjuku at data/Shinjuku (commit
3615babf001146507a1e9ec901cb3eabba9f5fd0). All jobs ran with nice -n 19.

1. Sweep (5 shards; this object came from shard 1):
   `LT_MEM=150 nice -n 19 venv/bin/python code/sweep1g.py --inputs attempts/sweep1g/inputs_xs24-28.txt --shard 1 --nshards 5 --out attempts/sweep1g/out_1.txt`
   Output line (data/sweep1g_out_1_hits.txt): `xs27_cikm1da4ozxd8711 20 1 -2 0 1 xs25_69ar1mkiczx643`
2. Lookup against cached Catagolue cost tables (code/lookup1g.py) gave the candidate line in
   data/candidate_line_1105e_new.txt: `IMPROVE xs25_69ar1mkiczx643 new 21 cur 49 from xs27_cikm1da4ozxd8711 20 rot 1 lane -2 ph 0 per 1`
3. Shinjuku route of the input (code/extract_paths.py writes attempts/multistage/paths.json; the entry used is
   data/paths_entry_xs27_cikm1da4ozxd8711.json, 7 stages, 20 gliders).
4. Stitch and verify (code/batch_ms2.sh on the candidate file; for this object the first try, pre 32, won):
   `nice -n 19 venv/bin/python code/compose_ms.py --in-apg xs27_cikm1da4ozxd8711 --rot 1 --lane -2 --ph 0 --target xs25_69ar1mkiczx643 --out attempts/compose_tmp/xs25_69ar1mkiczx643.p32.rle --pre 32`
   `nice -n 19 venv/bin/python code/verify_synthesis.py --rle attempts/compose_tmp/xs25_69ar1mkiczx643.p32.rle --target xs25_69ar1mkiczx643 --out attempts/compose_tmp/xs25_69ar1mkiczx643.p32.json`
   Logs: data/xs25_69ar1mkiczx643.p32.mlog, data/xs25_69ar1mkiczx643.p32.json. The stitched RLE is byte-identical to object/xs25_69ar1mkiczx643.rle.
The only change to the copied code is the first `cd` line of batch_ms2.sh, whose absolute path was replaced by RUN_DIR.
