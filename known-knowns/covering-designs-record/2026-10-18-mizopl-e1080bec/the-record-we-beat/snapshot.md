# Prior Record Snapshot (`C(94, 13, 5)`)

All live covering-design tables and repositories were fetched by single honest HTTP GET requests on `2026-10-18` immediately before the panel gate:

1. **Covering Repository (`coveringrepository.com` plain `(v,k,t)` archive, `m = t` section)**
   - **URL:** `https://coveringrepository.com/download_archive_vkt.aspx`
   - **Fetch timestamp (UTC):** `2026-10-18T09:40:05Z`
   - **HTTP status:** `200`
   - **Size:** `171,740` bytes (`9,629` lines)
   - **SHA-256:** `78bf5453858b476b90eeebd8ee8a35454e5f31866dd5f629934083ca0cd9bee3`
   - **Exact row for `(94, 13, 5)` (line `3648`):**
     ```text
     94	13	05	05		129203
     ```
   - **Prior record value:** `b = 129,203` (fetched `2026-10-18T09:40:05Z`).

2. **La Jolla Covering Repository (LJCR live site & Zenodo v1.1 / v1.2)**
   - **Status page URL:** `https://dmgordon.org/covering-designs/`
     - **Fetch timestamp (UTC):** `2026-10-18T09:40:05Z`, HTTP `200`, `9,200` bytes, `sha256: a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3` (`Site last updated 2026-09-03`).
   - **Zenodo LJCR v1.2 `coverdata.json` (latest published dataset, `2026-04-24`):**
     - **URL:** `https://zenodo.org/api/records/19735294/files/coverdata.json/content`
     - **Fetch timestamp (UTC):** `2026-10-18T09:40:54Z`, HTTP `200`, `8,319,503` bytes (uncompressed) / `3,705,056` bytes (wire), `sha256: 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87`.
     - **Exact entry for `C(94, 13, 5)`:**
       ```json
       {"v": 94, "k": 13, "t": 5, "size": 129337, "low_bd": 42705, "improvements": [["129337", "Dynamic programming construction", "LJCR", "2026-03-02 16:50:18"], ["133359", "Simple construction: combined (93,13,5) and  (93,12,4)", "LJCR", "2026-03-02 07:59:27"]]}
       ```
   - **Prior LJCR value:** `b = 129,337` (recorded `2026-03-02 16:50:18`, fetched `2026-10-18T09:40:54Z`).

3. **$47 + 47$ LJCR Ingredient Combining Baseline (`125,236` blocks)**
   - **Source archive:** Zenodo LJCR v1.2 (`https://zenodo.org/records/19735294`, published `2026-04-24`, fetched `2026-10-18T09:40:54Z`, `coverdata.json` `sha256: 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87`, `covers.json` `md5: bb59d977afd6724b32dcc187f68a229c`).
   - **Ingredients ($v_1 = 47, v_2 = 47$):**
     - $C(47, 13, 5) \le 2,849$ (**Jan de Heer & Steve Muir**, `2026-02-28 23:37:09`, https://ljcr.dmgordon.org/show_cover.php?v=47&k=13&t=5)
     - $C(47, 11, 4) \le 866$ (**Jan de Heer & Steve Muir**, `2026-02-28 23:37:09`, https://ljcr.dmgordon.org/show_cover.php?v=47&k=11&t=4)
     - $C(47, 8, 3) \le 345$ (**Jan de Heer & Steve Muir**, `2009-07-02 00:39:14`, https://ljcr.dmgordon.org/show_cover.php?v=47&k=8&t=3)
     - $C(47, 5, 2) \le 113$ (**Michael Dambmann**, `2008-11-22 20:38:48`, https://ljcr.dmgordon.org/show_cover.php?v=47&k=5&t=2)
     - $C(47, 2, 1) = 24$ (trivial pairs) and $(47, 0, 0) = 1$ (trivial empty block).
   - **Combining block count ($j = 0, \dots, 5$):** $1 \times 2,849 + 24 \times 866 + 113 \times 345 + 345 \times 113 + 866 \times 24 + 2,849 \times 1 = 125,236$ blocks (`built/94-13-5.txt`, `sha256: 4ddf66cf9edf0cf96165e7514dbcd0cafb9c3dc67198326ea0586a63661ffcfb`).

4. **Comparison Summary**
   - **Our explicit certificate (`object/design_94_13_5_part1.txt .. part5.txt`):** `b = 125,184` (`sha256: e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`)
   - **Improvement over $47+47$ LJCR combining baseline (`125,236`):** `52` fewer blocks (`-0.0415%`, via `how-we-built-it/merge.c`)
   - **Improvement over Covering Repository (`129,203`, fetched `2026-10-18T09:40:05Z`):** `4,019` fewer blocks (`-3.1106%`)
   - **Improvement over LJCR (`129,337`, fetched `2026-10-18T09:40:05Z` / `2026-10-18T09:40:54Z`):** `4,153` fewer blocks (`-3.2110%`)
