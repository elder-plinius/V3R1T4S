# Exact `BB_PT(8) = 19`: Complete Classification of All `19,693` Size-8 2-Tag Systems

## What

Under the wiki convention (size |A|+sum|w_a|, start 00, halt below 2 symbols), all 19,693 size-8 2-tag systems either halt (maximum 19 steps, only 111_20_) or have a checkable cycle or DFA-invariant non-halting certificate (including all 7 wiki holdouts), meeting criterion (b)/p1 for S=8 only, subject to the novelty skeptic finding no prior or merged equal result.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in `< 1.5 s` on 1 core, Python 3 standard library only, zero external packages).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| BusyBeaverWiki (`Post_Tag_System`, `oldid=8554`) | Size `8` (`BB_PT(8)`) | `>= 19` (`111_20_`, `7` holdouts) | https://wiki.bbchallenge.org/wiki/Post_Tag_System | 2026-11-15T16:38:32Z |
| Shawn Ligocki (`sligocki/etc/post_tag`, `HEAD = 203c30b1`) | Size `8` enumerator | `7` holdouts (`a57d8a3d`), `4` holdouts (`HEAD`) | https://github.com/sligocki/etc/tree/main/post_tag | 2026-11-15T14:07:12Z |
| AzertyWasTaken (`Busy-Beaver/Post Tag System`) | `010_2_0` (`Chaotic 2`) | `"currently undecided"` | https://github.com/AzertyWasTaken/Busy-Beaver/tree/main/Post%20Tag%20System | 2026-11-15T14:07:12Z |

Snapshot details and SHA-256 digests: `the-record-we-beat/README.md`.

## Not claimed

- Settles `S = 8` (`BB_PT(8) = 19`) completely under Success Criterion `(b)` and `p1`; does not settle exact `BB_PT(9)` (`154` wiki holdouts) or claim a halting champion above `779` (`S = 10`) or `196,841` (`S = 11`).

## Credits

- **Emil L. Post** (*Amer. J. Math.* 65, 197–215, 1943): 2-tag systems and the tag halting problem.
- **Shawn Ligocki** (<https://wiki.bbchallenge.org/wiki/Post_Tag_System>; <https://github.com/sligocki/etc/tree/main/post_tag>): `BB_PT` definition, `BB_PT(1..7)` exact table, `111_20_` champion, and reduction of `S = 8` to `7` holdouts.
- **AzertyWasTaken and the bbchallenge community** (<https://bbchallenge.org/>): investigation of chaotic 2-tag holdouts (`010_2_0`).
