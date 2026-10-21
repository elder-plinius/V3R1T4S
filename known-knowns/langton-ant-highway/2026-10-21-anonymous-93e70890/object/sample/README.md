# Sample data
sample_units.txt: one line per (pass, chunk) unit, 4 x 4096 = 16,384 lines, produced by lantx (v1 of lantx2; the only difference is the stop rule for masks with T_cap within ~312 steps of the cap, where v1 could report UNCAPTURED; no sampled mask is near the cap, and every v1 CAP line equals v2's — recheck with code/scripts/check_sample_blocks.sh). Selection rule: METHOD.md section 4. sample_summary.txt: aggregate (687,234,013 masks, all CAP).
Run: 4 workers, 2026-10-20T23:18:03Z to 2026-10-21T00:32:31Z (74.5 min wall), 3.60e12 simulated steps.
