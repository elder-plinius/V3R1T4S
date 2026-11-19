# Commands (from the harvest run folder; RUN_DIR is that folder)

Environment: Python 3.13 venv with python-lifelib 2.5.6, numpy, tqdm; Shinjuku at data/Shinjuku (commit
3615babf001146507a1e9ec901cb3eabba9f5fd0). All jobs ran with nice -n 19.

1. Sweep (5 shards; this object came from shard 0):
   `LT_MEM=150 nice -n 19 venv/bin/python code/sweep1g.py --inputs attempts/sweep1g/inputs_xs24-28.txt --shard 0 --nshards 5 --out attempts/sweep1g/out_0.txt`
   Output line (data/sweep1g_out_0_hits.txt): `xs27_3lkmz01iu1u8zw1221 10 3 12 0 1 xs26_oo0o4qabqiczx321`
2. Lookup against cached Catagolue cost tables (code/lookup1g.py) gave the candidate line in
   data/candidate_line_1010.txt: `IMPROVE xs26_oo0o4qabqiczx321 new 11 cur 35 from xs27_3lkmz01iu1u8zw1221 10 rot 3 lane 12 ph 0 per 1`
3. Shinjuku route of the input (code/extract_paths.py writes attempts/multistage/paths.json; the entry used is
   data/paths_entry_xs27_3lkmz01iu1u8zw1221.json, 3 stages, 10 gliders).
4. Stitch and verify (the earlier driver of the same two commands, with compose_ms.py's default stage-0 spacing,
   i.e. no --pre; batch_ms2.sh in code/ is the later driver that adds --pre 32/0/128 and gives the same RLE logic):
   `nice -n 19 venv/bin/python code/compose_ms.py --in-apg xs27_3lkmz01iu1u8zw1221 --rot 3 --lane 12 --ph 0 --target xs26_oo0o4qabqiczx321 --out attempts/compose_tmp/xs26_oo0o4qabqiczx321.ms.rle`
   `nice -n 19 venv/bin/python code/verify_synthesis.py --rle attempts/compose_tmp/xs26_oo0o4qabqiczx321.ms.rle --target xs26_oo0o4qabqiczx321 --out attempts/compose_tmp/xs26_oo0o4qabqiczx321.ms.json`
   Logs: data/xs26_oo0o4qabqiczx321.mlog, data/xs26_oo0o4qabqiczx321.ms.json. The stitched RLE is byte-identical to object/xs26_oo0o4qabqiczx321.rle.
The only change to the copied code is the first `cd` line of batch_ms2.sh, whose absolute path was replaced by RUN_DIR.
Two earlier single-stage attempts for this object (code not packaged) failed, because the input's Catagolue RLE is
multi-stage; the multi-stage stitch above is what produced the claimed RLE.
