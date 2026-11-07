# Novelty Audit (`ccd-binary-lennard-jones-clusters`)

- Context: Independent audit of live Cambridge Cluster Database server links and improvement archives.

1. Checked the live Cambridge Cluster Database table at `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/table.html` (HTTP `200`, SHA-256 `045161fcbc4117f5a4c52252cbe3c7680342aee55be9dde95e6d729d3fec449d`), Apache directory listings `/1.05/` through `/1.3/`, `all.tar`, and the 4 hosted improvement archives.
2. Across the 576 `N=5..100` cells linked by `table.html`:
   - `475` cells link to unchanged `1.X/N` files matching `all.tar` within `5e-7`.
   - `27` cells (`2` in `1.05/`, `25` in `1.1/`) link to `new` files (`HTTP 200`) hosted in the live server directories but omitted from `all.tar`; re-evaluating those 27 `new` files from coordinates confirms they match `table.html` within `5e-7`.
   - `70` cells (`1.1/46new` plus all `69` `new`/`newer` links in `1.15/`, `1.2/`, `1.25/`, and `1.3/`) return `HTTP 404 Not Found` on the live Cambridge server, leaving only the superseded `all.tar` coordinate file hosted on the server.
   - `4` cells (`1.05/31`, `1.05/36`, `1.05/97`, `1.1/66`) have updated energies in `table.html` (footnote `c`), while their `<A HREF="1.X/N">` link still resolves to the superseded `all.tar` file (discrepancies `0.007330` to `0.435164`).
3. Across all 63 files in the 4 hosted improvement archives, 33 distinct `(N, ratio)` cells strictly beat both `table.html` and the live linked point files by `> 1e-4` (up to `1.424056` below `table.html` at `N=100, ratio=1.30`, and `1.581534` below the live linked file at `N=99, ratio=1.30`).

pass: true
