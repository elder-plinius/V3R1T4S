# Construction and provenance

Contributor text, unverified except the reproduced RLE and recorded checks.
Discovery was in harvest run 2026-11-03-glider, not this confirmation.
Actual environment: Python 3.13, python-lifelib 2.5.6, numpy 2.5.4;
Shinjuku commit 3615babf001146507a1e9ec901cb3eabba9f5fd0 (https://gitlab.com/parclytaxel/Shinjuku).
Supply that library checkout as data/Shinjuku inside how-we-built-it with prepared dependencies.
No third-party library source is redistributed. From how-we-built-it:

`nice -n 19 python3 -B code/compose_ms.py --paths data/predecessor_path.json --in-apg xs25_0ml1u8z643032ak8 --rot 1 --lane 11 --ph 0 --target xs28_69a4owgzxol5d1d96 --out rebuilt.rle --pre 32`

This confirmation reran these construction arguments and rebuilt.rle SHA256 equals object hash.
The predecessor is one published 6-glider component; the sweep adds one glider, total 7.
Sweep code is included to attribute the method, not to claim rerunning the entire harvest.
Original verifier JSON ok:false is preserved: it implements only listed-cost #CSYNTH comparison,
not the first-synthesis clause. Its structural fields are supporting evidence, not absence proof.
The original verifier was rerun with live fetch disabled; the package checker is independent stdlib.
