role: CRITERION
context: claude code headless session (claude -p --safe-mode in a copy of claim/ outside the workspace; fresh context, saw only claim/)

# CRITERION skeptic: wieferich-other-bases-fischer-table, partial win p1

## Verdict in brief

- **Partial win p1: met, literally and in full.** Every clause holds by my own code. Primality is proven by full trial division, not only Miller-Rabin. I re-fetched the tables live: they are byte-identical to the snapshot and contain neither p nor a row for base 56350. A live OEIS search for p returns no match.
- **Full win: does not apply.** It needs a base from 3 to 10125, and b = 56350 is above that range. There is no searched limit for this base to beat. The pair is also not a headline result: it does not hold mod p^3, and it is not a double Wieferich pair.
- **Hidden quantifier, stated plainly.** For the two named Fischer tables, "absent" is guaranteed by the base range. FermQ_Sorg.txt has rows only for bases 2..10125. FermQ_Sort.txt has rows only for bases 2..1052 plus 65537. So the tables only add real information in two ways: p does not appear anywhere in them, and OEIS has no match. The scope sentence below does not go beyond "absent from these named sources". It does not claim the pair was never computed anywhere.
- **Not subsumed.** b is not a perfect power. Among all bases from 2 to 65536, only a = 56350 has a^(p-1) ≡ 1 (mod p^2). So no pair for a base in Fischer's range (or any other base up to 65536) implies this one through powers or products. This agrees with FermQ_Sorg.txt: all its bases were searched to 4.8E+12, which is above p, and p appears in none of its rows. The pair is not trivial: b mod p^2 is neither 1 nor p^2 − 1.
- **Null model.** Under the standard 1/p heuristic, the 55237 eligible bases in 10126..65536 should give about 47 pairs with 1e12 below p and p at most 1024048960667. One such pair is ordinary. The result is a correct pair that is new relative to the named records, which is exactly what p1 enumerates. It is not a statistical anomaly, and the scope does not claim one.

## Clause-by-clause check of p1

The p1 text, verbatim from claim/claim.md: "New pair for a base 10125 < b < 65537 that is not a perfect power, with p above 1e12, b^(p-1) == 1 mod p^2 checked exactly, and absent from both Fischer tables and OEIS."

| clause | how I checked it (my own code: work/check.py, work/compare.py, work/extra.py) | result |
|---|---|---|
| base strictly between 10125 and 65537 | direct comparison | b = 56350: True |
| b not a perfect power | full factorisation of b, gcd of exponents, plus an exact integer k-th root for every k from 2 to the bit length | 2^1 * 5^2 * 7^2 * 23^1, gcd 1, no exact root: True |
| p above 1e12 | direct comparison | p / 1e12 = 1.024049: True |
| p prime (implicit in "pair") | trial division by 2 and every odd d up to isqrt(p) = 1011953, which is a complete proof; Miller-Rabin with bases 2..37 as a cross-check | no divisor, MR True |
| p does not divide b (implicit) | gcd | gcd(b, p) = 1 |
| b^(p-1) ≡ 1 mod p^2, exact | three independent exact computations: builtin pow, my own square-and-multiply, and the product over the prime factors of b; plus the Fermat-quotient identity q_p(b) = q_p(2)+2q_p(5)+2q_p(7)+q_p(23) ≡ 0 mod p | all three give 1, identity sum 0 |
| absent from both Fischer tables | snapshot sha256 matches claim/status_sources.md; live re-fetch byte-identical; search for p as an integer token and as substrings (incl. grouped and float forms); base-row parse | p absent; no row for 56350; Sorg rows 2..10125, Sort rows 2..1052 plus 65537 |
| absent from OEIS | one live request to the OEIS search for p (fmt=data) | page contains "Sorry, but the terms do not match anything in the table" |

Beyond the criterion, I also searched Fischer's other files: ErstBasen.txt, ErstPBasen.txt, News.txt, FermatQ3.txt (mod P^3) and SwitchFermQ.txt (double pairs). None contains p or the integer 56350. The only substring hit for "56350" in any file is inside the number 3563501 in the base-2450 row of FermQ_Sorg.txt (" 2450,  23, 71, 3563501"), which is unrelated.

## Full win

It does not apply. The full criterion requires "an integer base 3 <= b <= 10125", and b = 56350 is outside that range (extra_out: "full win base range 3 <= b <= 10125 applies: False"). The pair is also neither a new Mirimanoff prime nor a double Wieferich pair ("double Wieferich p^(b-1) == 1 mod b^2: False"), so it is not a headline result. It counts only as one p1 pair.

## Hidden quantifiers and stretched definitions

1. **"absent from both Fischer tables" is guaranteed by the range.** Neither table covers any base from 10126 to 65536, so no base in p1's range could ever have a row. The clause only does real work through the global search for the number p (absent) and through OEIS (no match). I do not count range-guaranteed absence as evidence that nobody has ever found this pair. The scope sentence says only "absent from the named tables and from an OEIS search for p".
2. **OEIS search scope.** An OEIS term search covers sequence data fields, not b-files. "Absent from OEIS" therefore means "the OEIS search for p returns no match", and the scope says exactly that.
3. **"p above 1e12"**: p exceeds the bound by 2.4%, which strictly satisfies it.
4. **"pair" implies p is prime.** p1 does not say "proven prime" explicitly, but I proved it anyway (trial division to isqrt(p)).
5. **"not a perfect power"**: checked exactly with integers, not floats (my iroot is a binary search over integers).
6. **"checked exactly"**: all arithmetic is exact integer arithmetic modulo p^2, about 1.05e24, computed three ways.
7. **Snapshot freshness.** The claim's snapshot was fetched 2026-11-07T21:59Z (claim/status_sources.md). My re-fetches, made before the timestamp 2026-11-07T22:06:28Z printed by date -u, are byte-identical. Fischer's index shows the two tables were last updated on 21.10.2026.
8. **OEIS reply hash.** My OEIS reply's sha256 differs from the scout's. That is expected, because the page has dynamic parts such as the search timing and the greeting banner. Both replies contain the same "Sorry, but the terms do not match anything in the table" result.

## Null models

- **Abundance (1/p heuristic).** For a fixed base, the chance of a Wieferich prime with 1e12 below p and p at most 1024048960667 is about 8.597e-04. Over the 55237 bases in 10126..65536 that are not perfect powers, about 47.49 pairs are expected in that window, about 190 up to 1.1e12, and about 3050 up to 4.8e12. So the find is unremarkable as mathematics. Its value is that it is a correct pair, verified exactly and new relative to the record, which is what p1 asks for.
- **Trivial or derived pairs.**
  - b mod p^2 is not 1 or p^2 − 1, so this is not a trivial pair.
  - b is not a power of a smaller base.
  - Among all bases from 2 to 65536, only a = 56350 makes p a Wieferich prime. So the pair does not follow from any listed pair through products or powers.
  - The scan's empty result for bases up to 10125 matches Fischer's FermQ_Sorg.txt. That table was searched to 4.8E+12, above p, and p is absent from it.

## Evidence (verbatim command output)

The claim's checker, run as `python3 -I -B claim/verify.py claim/object/pair.json` (saved as work/verify_out.txt):

```
ok   10125 < b < 65537
ok   b is not a perfect power
ok   p > 1e12
ok   p is prime (deterministic Miller-Rabin)
ok   p does not divide b
ok   b^(p-1) == 1 mod p^2
b = 56350, p = 1024048960667, Fermat quotient q_p(b) mod p = 0
PASS
```

My own checker, run as `python3 -I -B work/check.py claim/object/pair.json claim/inputs` (saved as work/check_out.txt):

```
pair.json content: {"b": 56350, "p": 1024048960667, "partial_win": "p1", "target_id": "wieferich-other-bases-fischer-table"}
b = 56350, p = 1024048960667
C1 10125 < b < 65537: True
factorisation of b: 2^1 * 5^2 * 7^2 * 23^1
gcd of exponents: 1 -> perfect power: False
C2 exact integer k-th roots of b for k = 2..bit_length that are exact: [] -> not a perfect power: True
C3 p > 10^12: True (p / 1e12 = 1.024049)
C4a trial division: isqrt(p) = 1011953, smallest divisor found = None -> p prime: True
C4b Miller-Rabin bases 2..37 (cross-check): True
factorisation of p-1: 2^1 * 512024480333^1
C5 p does not divide b: True | gcd(b, p) = 1
C6 b^(p-1) mod p^2 by builtin pow: 1
C6 b^(p-1) mod p^2 by own square-and-multiply: 1
C6 b^(p-1) mod p^2 via factorisation of b: 1
Fermat quotients q_p(q) mod p of the prime factors of b: {2: 366008234196, 5: 29806142339, 7: 70436202038, 23: 457556037717}
sum e*q_p(q) mod p (must be 0 iff b is Wieferich at p): 0
trivial pair check: b mod p^2 in {1, p^2-1}? False
all bases a in 2..65536 with a^(p-1) == 1 mod p^2: [56350]
bases at most 10125 among them (would have to be in Fischer's FermQ_Sorg, searched to 4.8e12, above p): []
--- ErstBasen.txt: bytes=115771 lines=1269 sha256=e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 matches status_sources.md: True
    substring '56350': 0 | integer token 56350: False
    substring '1024048960667': 0
    substring '1,024,048,960,667': 0
    substring '1.024.048.960.667': 0
    substring '1 024 048 960 667': 0
    substring '1.024048960667': 0
    substring '1.024049E+12': 0
    substring '1.02404896': 0
    substring '1024048': 0
    integer token 1024048960667: False
    integers in (1e12, 1e16): 414; those within 5e10 of p: [1000158170385, 1036253048315, 1054768584965, 1056305858813, 1061395940649, 1061646187872, 1071150435875, 1072355035046]
    'P:' entries: 554; P = 1024048960667 present: False; max P entry: 119079791436527
    limit line: Durchsucht bis zur Primzahl 1120000031
    limit line: Durchsucht bis zur Primzahl 1120000031
--- ErstPBasen.txt: bytes=81696 lines=972 sha256=3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 matches status_sources.md: True
    substring '56350': 0 | integer token 56350: False
    substring '1024048960667': 0
    substring '1,024,048,960,667': 0
    substring '1.024.048.960.667': 0
    substring '1 024 048 960 667': 0
    substring '1.024048960667': 0
    substring '1.024049E+12': 0
    substring '1.02404896': 0
    substring '1024048': 0
    integer token 1024048960667: False
    integers in (1e12, 1e16): 187; those within 5e10 of p: [1069929736297]
    'P:' entries: 532; P = 1024048960667 present: False; max P entry: 18088417183289
    limit line: Durchsucht bis zur Primzahl 1120000031
    limit line: Durchsucht bis zur Primzahl 1120000031
--- FermQ_Sorg.txt: bytes=288459 lines=10166 sha256=35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 matches status_sources.md: True
    substring '56350': 1 | integer token 56350: False
    substring '1024048960667': 0
    substring '1,024,048,960,667': 0
    substring '1.024.048.960.667': 0
    substring '1 024 048 960 667': 0
    substring '1.024048960667': 0
    substring '1.024049E+12': 0
    substring '1.02404896': 0
    substring '1024048': 0
    integer token 1024048960667: False
    integers in (1e12, 1e16): 549; those within 5e10 of p: [1000436194319, 1002205496401, 1002545906249, 1003364577899, 1006363479007, 1007840228201, 1008360911707, 1010499405017, 1013674942057, 1015405022287, 1016812692871, 1017480110861, 1018124410087, 1022322763277, 1029546197321, 1030771280039, 1034329079317, 1036499468651, 1040477449643, 1043812431511, 1044288030757, 1046769059261, 1052847001489, 1056149396051, 1056258922679, 1056305858813, 1060973961673, 1063213431361, 1063956942197, 1064548400077, 1067125106459, 1069003457101, 1072673379383]
    base rows: count=10001 min=2 max=10125 bases > 10125: [] row for 56350: False
    limit line: Die Basen sind gegenwaertig durchsucht bis 4.8E+12
--- FermQ_Sort.txt: bytes=33141 lines=1032 sha256=bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b matches status_sources.md: True
    substring '56350': 0 | integer token 56350: False
    substring '1024048960667': 0
    substring '1,024,048,960,667': 0
    substring '1.024.048.960.667': 0
    substring '1 024 048 960 667': 0
    substring '1.024048960667': 0
    substring '1.024049E+12': 0
    substring '1.02404896': 0
    substring '1024048': 0
    integer token 1024048960667: False
    integers in (1e12, 1e16): 158; those within 5e10 of p: []
    base rows: count=981 min=2 max=65537 bases > 10125: [65537] row for 56350: False
    limit line: Die Basen, die einen maximalen Primteiler bis 149 haben, sind durchsucht bis 2.00E+14
    limit line: Die restlichen Basen sind gegenwaertig durchsucht bis 7.4E+13
null model: 55237 non-perfect-power bases in 10126..65536; expected pairs with 1e12 < p <= 1.024e+12: 47.49
null model: 55237 non-perfect-power bases in 10126..65536; expected pairs with 1e12 < p <= 1.1e+12: 190.21
null model: 55237 non-perfect-power bases in 10126..65536; expected pairs with 1e12 < p <= 4.8e+12: 3050.03
null model: chance a fixed base has a Wieferich prime in (1e12, p]: 8.597e-04
```

The single "56350" substring hit in FermQ_Sorg.txt (Grep over claim/inputs):

```
claim\inputs\FermQ_Sorg.txt:2399: 2450,  23, 71, 3563501
```

Live re-fetches: one curl request per source with the kit's User-Agent, saved in work/fetch/. The HTTP status printed by curl -w was `200` for each of the nine requests: FermQ_Sorg.txt, FermQ_Sort.txt, ErstBasen.txt, ErstPBasen.txt, Fischer's index page, the OEIS search, News.txt, FermatQ3.txt and SwitchFermQ.txt. The statuses are saved in work/fetch_*_status.txt. `date -u` run after the first six requests printed:

```
2026-11-07T22:06:28Z
```

Comparison of the live copies with the snapshot, run as `python3 -I -B work/compare.py work/fetch claim/inputs` (saved as work/compare_out.txt; the long list of index links is omitted here):

```
FermQ_Sorg.txt: live bytes=288459 sha256=35273a263ecee70b98161c4127dce900b1e7605dc4a692f632e78e3c46e45ff4 | identical to snapshot: True
    live contains '1024048960667': False | integer token 56350: False
FermQ_Sort.txt: live bytes=33141 sha256=bda97784e89ed16b2162e9a47b06a3363160acd7f7d904b887a8115a0aaa202b | identical to snapshot: True
    live contains '1024048960667': False | integer token 56350: False
ErstBasen.txt: live bytes=115771 sha256=e4fd0d969381027a1dbb6c6f797d8231f02184305cff0265ac1a2ef5880bc820 | identical to snapshot: True
    live contains '1024048960667': False | integer token 56350: False
ErstPBasen.txt: live bytes=81696 sha256=3149a364f5531ff1f7ac65a31b0a3f9ecd57d24f27e5ece18b009f9f875ea362 | identical to snapshot: True
    live contains '1024048960667': False | integer token 56350: False
oeis.txt: bytes=6737 sha256=74c62b0d98fe2d8122341ec64a57825b08d639379a7ee9a4e064dccdb8eb39b2
    contains 'Sorry, but the terms do not match anything in the table': True (count 1)
    contains 'No results': False (count 0)
    contains 'Search: seq:1024048960667': False (count 0)
    contains '1024048960667': True (count 6)
    A-numbers mentioned: []
    text around 'Sorry': s in the A400K Celebration Hints (Greetings from The On-Line Encyclopedia of Integer Sequences !) Search: 1024048960667 Sorry, but the terms do not match anything in the table. &nbsp;&nbsp;&nbsp;&nbsp; Search completed in 0.000 seconds Lookup Welcome Wiki Register Music Plot 2 De
index.html: bytes=16104 sha256=42508627832b9d654ea777db3c10126d558bf7bf13c21c07c5b74452b8e84fd1
    contains '1024048960667': False | contains '56350': False
    index line: Tabelle bis Basis 1052 / List from base 2 until 1052 and base 65537 / Update 21.10.2026
    index line: Tabelle bis Basis 10125 / List from base 2 until 10125 / Update 21.10.2026
    index line: Extreme Erstbasen / Extreme first bases / Update 27.09.2025
    index line: Extreme Erstprimbasen / Extreme first prime bases / Update 27.09.2025
```

Other Fischer files and extra properties, run as `python3 -I -B work/extra.py work/fetch` (saved as work/extra_out.txt):

```
News.txt: bytes=8500 sha256=1970fbe5188e93b0fa0381beac91b0654b18c9491043bbdb42e256bc7f6080e7
    first lines: Thema: News und Rekorde mit Fermatquotienten B^(P-1) == 1 (mod P^2) | Main table of content: http://www.fermatquotient.com/ | Die letzten 10 gefundenen Fermatquotienten haben folgende Basen: | 655 (Rekord), 1023 (Record, new base), 852 (Rekord), 349 (prim), | 963 (Rekord), 1041, 770 (Record), 892, 8
    contains '1024048960667': False | integer token 56350: False | substring '56350': 0
FermatQ3.txt: bytes=11274 sha256=022855e8d16257ca4931bd9f7f9133012f17bbf1bc528f9a6cd12995b02a0a41
    first lines: Thema: Fermatquotient B^(P-1) == 1 (mod P^3) | Main table of content: http://www.fermatquotient.com/ | Fachartikel zu den Fermatquotienten == 1 (mod P^m) | http://go.helms-net.de/math/expdioph/fermatquot_ge2_table1.htm
    contains '1024048960667': False | integer token 56350: False | substring '56350': 0
SwitchFermQ.txt: bytes=10726 sha256=8190a7ca0bf2a31d9b03b77e97e5d09f45abc8b7df6f4321d706732b329f3faa
    first lines: Thema: Doppelpaar Wieferich-Primzahlen mit der Basis B und der Primzahl P | (double Wieferich prime pairs) | B^(P-1) == 1 (mod P^2) und P^(B-1) == 1 (mod B^2) | Main table of content: http://www.fermatquotient.com/
    contains '1024048960667': False | integer token 56350: False | substring '56350': 0
b^(p-1) == 1 mod p^3 (headline-type extra): False
double Wieferich p^(b-1) == 1 mod b^2: False
full win base range 3 <= b <= 10125 applies: False
```

## Scope

The scope covers one pair, (56350, 1024048960667), for partial win p1 only. It does not claim the full win or any headline result, and it does not claim the pair is absent from every possible source. It claims only that the pair is absent from Fischer's two tables as snapshotted and from an OEIS search for p.

confirmed_scope: The single pair in object/pair.json, base 56350 = 2·5^2·7^2·23 (not a perfect power, strictly between 10125 and 65537) with p = 1024048960667 (above 1e12, proven prime by trial division up to its square root), satisfies 56350^(p-1) ≡ 1 (mod p^2) in exact integer arithmetic and is absent from Fischer's FermQ_Sorg.txt and FermQ_Sort.txt as snapshotted in the-record-we-beat/RECORD.md (neither has a row for any base between 10125 and 65537 and neither contains p) and from an OEIS search for p made on 2026-11-07, so it meets partial win p1 of wieferich-other-bases-fischer-table but not the full win, which requires a base of at most 10125.

pass: true
