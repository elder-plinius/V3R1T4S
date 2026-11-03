# Covering design C(57,14,3) with 108 blocks

## What

As of 2026-10-18 14:34Z, object/C_57_14_3_b108.json is 108 distinct 14-subsets of {1..57} (no repeated points) covering all 29260 3-subsets by my own exhaustive check, 108 >= Schonheim 90, strictly below the 109 I read live on the coveringrepository.com plain m=3 row for (57,14,3) and below the 110 (LJCR GitHub) and 109 (Zenodo v1.2) values from the same-day novelty fetches; the live dmgordon.org page holds no value, and no hobbyist or recent-literature claim for (57,14,3) was found, though my own arXiv/GitHub-code search was not completed.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: python3 3.8 or later, standard library only.
- **Rough laptop time**: about a second.
- **Expected last line**: `ALL CHECKS PASS`

The object `object/C_57_14_3_b108.json` has sha256 f133e94dd68370e1e8001f34d0f021032948f2380962a71e8a4d80b15bee0803.

## Compared to

| Source | Cell | Listed value | Ours | URL | UTC fetch time |
|---|---|---|---|---|---|
| coveringrepository.com, plain table, m = t = 3 | C(57,14,3) | 109 (Franco Atzeni, 14/02/2025) | **108** | https://coveringrepository.com/systems.aspx | 2026-10-18T14:24:06Z |
| LJCR data on GitHub (dmgordo/LJCR) | C(57,14,3) | 110 | **108** | https://raw.githubusercontent.com/dmgordo/LJCR/master/coverings/coverdata.json | 2026-10-18T14:24:23Z |
| LJCR on Zenodo v1.2 | C(57,14,3) | 109 | **108** | https://zenodo.org/api/records/19735294/files/coverdata.json/content | 2026-10-18T14:24:38Z |
| La Jolla Covering Repository page | C(57,14,3) | no value listed (prose page; points to coveringrepository.com) | **108** | https://dmgordon.org/covering-designs/ | 2026-10-18T14:34:22Z |

The panel's criterion skeptic read the coveringrepository.com value again at 2026-10-18T14:34:14Z (109). The margin is one block. Hashes and the other sources read: `the-record-we-beat/README.md`.

## Not claimed

- Only the cell C(57,14,3). Nothing for other parameters, and no claim that 108 is optimal: the Schonheim lower bound is 90.
- The tables change often; the comparison holds for the values recorded above. The panel's search of GitHub and arXiv for unlisted claims on (57,14,3) found none, but it was not complete (see `panel/criterion.md`).
- The panel's first criterion run (`panel/criterion_run1.md`) did not pass the claim because the claim folder lacked a live re-fetch of the coveringrepository.com value; `panel/gate.md` explains, and the second run (`panel/criterion.md`) passed.
- Not peer reviewed. Checked by a three-skeptic panel (`panel/`) and the standalone checker shipped here.

## Credits

- **Giovanni Acerbi**, the Covering Repository at https://coveringrepository.com/, the status source, and its tables.
- **Dan Gordon**, the La Jolla Covering Repository: https://dmgordon.org/covering-designs/, the data on GitHub https://github.com/dmgordo/LJCR and the Zenodo record https://zenodo.org/records/19472830 (versions 1.1 and 1.2).
- **Franco Atzeni**, whose 109-block design for (57,14,3) (14/02/2025) this one improves on; the search here started from a 109-block design.
- **W. Schonheim** for the lower bound used as a sanity check.
- Search: an AI agent (Gemini, called Argon) for the contributor `calgulbenkian`.
