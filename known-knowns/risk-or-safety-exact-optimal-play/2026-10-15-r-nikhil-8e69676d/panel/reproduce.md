# REPRODUCE skeptic report: risk-or-safety-exact-optimal-play, run 2026-10-15-0312

Role: REPRODUCE skeptic (one of three). I used only the claim package and the public paper arXiv:2603.01002. I fetched the abs page and the PDF with one plain request each. Both returned HTTP 200 on 2026-10-15 at about 09:17Z. The PDF is v1, 12 pages, submitted 1 Mar 2026, with sha256 88978bcfbe6bc5af5ca9456de471d53b5b4a4478985e2952b8490bf5d652aa91. I extracted its text with pdftotext. Files are named relative to claim/. My own code and outputs were kept in a scratch folder outside claim/, written `<scratch>` below. I treated claim/ as read-only. A sha256 snapshot of all 39 files in claim/, taken before any author code ran, is identical to one taken after all runs, and no new file appeared in claim/.

Order of work:
1. I read claim.md, REPRODUCE.md, values.txt, data/ and the certificate format.
2. I wrote my own checker and my own exact solver from the definition quoted in claim.md, ran both on all 30 certificates, and mutation-tested the checker.
3. I fetched and read the paper (Sections 1-5 and Table 1).
4. Only then did I open checker/ros_cert_check.py, solver/solver.py and solver/my_verify.py and run the REPRODUCE.md commands.

## 1. The equations (quoted)

From claim.md, "The game (definition as used; quoted from the bank statement)":

> Two players race to n banked points. On a turn the player tosses a fair coin: each head adds one open point and the player may then stop, banking the open points (turn passes), or toss again; a tail loses all open points and passes the turn. First to n points wins; equivalently each turn chooses a number x of coins and banks x points iff all are heads.
>
> Position (a, b, c): a open points and b banked points of the player to move, c banked points of the opponent.
> P(a, b, c) = 1 when a + b >= n. Forced toss at a = 0: P(0, b, c) = (1/2)(1 - P(0, c, b)) + (1/2) P(1, b, c).
> For a >= 1: P(a, b, c) = max(continue, stop), continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a + 1, b, c),
> stop = 1 - P(0, c, a + b). The claimed answer for n is P(0, 0, 0).

From the success criterion in claim.md (verbatim from the bank entry):

> ... satisfying exactly P(a, b, c) = max(continue, stop) for a >= 1 and the forced toss for a = 0, where continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a + 1, b, c) and stop = 1 - P(0, c, a + b), with P = 1 when a + b >= n (equations of Sections 3-4 of arXiv:2603.01002), all checked in exact arithmetic. The same code must reproduce the published terms for n <= 15 (or certify a correction, see p1).

From the paper, Section 1 (the rules):

> A player whose turn it is tosses a coin. If it is heads they earn a point, and they can choose to go for safety, put the point aside in a save box, and give the turn to their opponent. Or they take the risk to continue and toss the coin again. If it is heads again, the number of "open" points increases by one, and they can choose again to continue or stop, converting the "open" points to "saved" points. Whenever it is tails, all the open points are lost, and it is the turn of the other player. Who collects n points first wins.

From the paper, Section 4. This is the pdftotext rendering with the stacked fractions retyped inline:

> For any b and c, we have P(0, b, c) = 1/2 (1 - P(0, c, b)) + 1/2 P(1, b, c) and P(0, c, b) = 1/2 (1 - P(0, b, c)) + 1/2 P(1, c, b). Inserting the second equation into the first yields P(0, b, c) = 1/3 + 2/3 P(1, b, c) - 1/3 P(1, c, b) (7). Applying Eq. 7 at position (a, b, c) for a >= 1 we get: P(a, b, c) = 1/2 (1 - P(0, c, b)) + 1/2 P(a + 1, b, c) = 1/3 - 1/3 P(1, c, b) + 1/6 P(1, b, c) + 1/2 P(a + 1, b, c) when the current player chooses to continue and P(a, b, c) = 1 - P(0, c, a + b) = 2/3 - 2/3 P(1, c, a + b) + 1/3 P(1, a + b, c) when the current player chooses to stop. [...] Note that if a+b=n, then Pmin(a, b, c) := Pmax(a, b, c) := 1.

I re-derived Eq. (7) by hand. Let x = P(0,b,c), y = P(0,c,b), p = P(1,b,c), q = P(1,c,b). Then x = 1/2 - y/2 + p/2 and y = 1/2 - x/2 + q/2, which gives 3x/4 = 1/4 + p/2 - q/4, so x = 1/3 + 2p/3 - q/3. The paper's two expanded forms for continue and stop also follow from (7). In unexpanded form they are exactly the claim's continue and stop expressions.

## 2. My own checker, written from the definition before I read any author code

My checker is <scratch>/my_checker.py. It uses the Python 3.9 standard library and fractions.Fraction, with no floats anywhere. For each certificate it checks the following.

- **Strict JSON.** The file is ASCII. The top-level keys are exactly n, P000 and table. Duplicate JSON keys, float literals and NaN are rejected. The file name n<k>.json must match n.
- **(a) Positions.** Every row is [a, b, c, value, action]. The coordinates are ints (a bool is rejected), with 0 <= b < n, 0 <= c < n and 0 <= a < n - b. There are no duplicates, the position set equals the full set, and the row count is n^2(n+1)/2.
- **(b) Values.** Every value is a canonical string num/den, with no sign, no leading zeros and den >= 1. It must satisfy gcd(num, den) = 1 and num <= den, so it is a reduced fraction in [0,1].
- **(c) a = 0.** The action is "toss" and value == 1/2 (1 - P(0,c,b)) + 1/2 P(1,b,c).
- **(d) a >= 1.** value == max(continue, stop), where continue = 1/2 (1 - P(0,c,b)) + 1/2 P(a+1,b,c), stop = 1 - P(0,c,a+b), and P = 1 whenever a + b >= n. The claimed action's own value must equal that max. Exact ties are counted.
- **(e) P000.** The P000 field, also strictly parsed, must be the same string as the table value at (0,0,0). The checker prints P(0,0,0) and compares it exactly with values.txt and with the claim.md table (n >= 16). For n <= 15 it also compares with the b-files: the numerator must equal A387261(n) and the denominator A387262(n).

This is the core of the equation check, copied verbatim from my checker:

```
    def P(a, b, c):
        if a + b >= n:
            return ONE
        return vals[(a, b, c)]

    n_stop = n_toss_a1 = n_tie = 0
    for (a, b, c), v in vals.items():
        cont = HALF * (ONE - P(0, c, b)) + HALF * P(a + 1, b, c)
        act = acts[(a, b, c)]
        if a == 0:
            if v != cont:
                raise CertError("forced-toss equation fails at %r" % ((a, b, c),))
            if act != "toss":
                raise CertError("action at a=0 is %r, not toss, at %r" % (act, (a, b, c)))
        else:
            stop = ONE - P(0, c, a + b)
            best = cont if cont >= stop else stop
            if v != best:
                raise CertError("value != max(continue, stop) at %r" % ((a, b, c),))
            if act == "toss":
                if cont != v:
                    raise CertError("claimed toss does not attain the max at %r" % ((a, b, c),))
                n_toss_a1 += 1
            else:
                if stop != v:
                    raise CertError("claimed stop does not attain the max at %r" % ((a, b, c),))
                n_stop += 1
```

### 2.1 Real output: calibration/n1..n15, compared with values.txt and data/b387261.txt + data/b387262.txt

```
$ python3 -I <scratch>/my_checker.py --values values.txt --bnum data/b387261.txt --bden data/b387262.txt calibration/n1.json ... calibration/n15.json
calibration/n1.json n=1 rows=1 expected=1 stop_actions=0 toss_actions_a>=1=0 ties=0 values.txt=match oeis=match 0.00s P000=2/3 OK
calibration/n2.json n=2 rows=6 expected=6 stop_actions=0 toss_actions_a>=1=2 ties=0 values.txt=match oeis=match 0.00s P000=4/7 OK
calibration/n3.json n=3 rows=18 expected=18 stop_actions=2 toss_actions_a>=1=7 ties=0 values.txt=match oeis=match 0.00s P000=6/11 OK
calibration/n4.json n=4 rows=40 expected=40 stop_actions=11 toss_actions_a>=1=13 ties=0 values.txt=match oeis=match 0.00s P000=2236/4165 OK
calibration/n5.json n=5 rows=75 expected=75 stop_actions=29 toss_actions_a>=1=21 ties=0 values.txt=match oeis=match 0.00s P000=1026/1925 OK
calibration/n6.json n=6 rows=126 expected=126 stop_actions=59 toss_actions_a>=1=31 ties=0 values.txt=match oeis=match 0.01s P000=275848876/521145625 OK
calibration/n7.json n=7 rows=196 expected=196 stop_actions=103 toss_actions_a>=1=44 ties=0 values.txt=match oeis=match 0.01s P000=649346842/1231278125 OK
calibration/n8.json n=8 rows=288 expected=288 stop_actions=165 toss_actions_a>=1=59 ties=0 values.txt=match oeis=match 0.01s P000=61550866190068/117192622421875 OK
calibration/n9.json n=9 rows=405 expected=405 stop_actions=247 toss_actions_a>=1=77 ties=0 values.txt=match oeis=match 0.01s P000=2737872156886/5225432428125 OK
calibration/n10.json n=10 rows=550 expected=550 stop_actions=354 toss_actions_a>=1=96 ties=0 values.txt=match oeis=match 0.02s P000=5556238701119487884/10634368774326171875 OK
calibration/n11.json n=11 rows=726 expected=726 stop_actions=487 toss_actions_a>=1=118 ties=0 values.txt=match oeis=match 0.03s P000=33857036312840796476194/64913928515324560546875 OK
calibration/n12.json n=12 rows=936 expected=936 stop_actions=650 toss_actions_a>=1=142 ties=0 values.txt=match oeis=match 0.04s P000=3393041394611453189295265268/6519012951936493553466796875 OK
calibration/n13.json n=13 rows=1183 expected=1183 stop_actions=844 toss_actions_a>=1=170 ties=0 values.txt=match oeis=match 0.05s P000=218370486707916654640780231642/420117998909827688127861328125 OK
calibration/n14.json n=14 rows=1470 expected=1470 stop_actions=1075 toss_actions_a>=1=199 ties=0 values.txt=match oeis=match 0.06s P000=112630244896738642814653528498087299988/217038092253876925088545128021240234375 OK
calibration/n15.json n=15 rows=1800 expected=1800 stop_actions=1344 toss_actions_a>=1=231 ties=0 values.txt=match oeis=match 0.08s P000=14364898791782224577113184680141626682/27711032758513212360715995025634765625 OK
my_checker summary: 15 OK, 0 FAIL, of 15 files
(exit code 0)
```

### 2.2 Real output: object/n16..n30, compared with values.txt and the claim.md table

```
$ python3 -I <scratch>/my_checker.py --values values.txt --claim claim.md object/n16.json ... object/n30.json
object/n16.json n=16 rows=2176 expected=2176 stop_actions=1655 toss_actions_a>=1=265 ties=0 values.txt=match claim.md=match 0.13s P000=1599710761252635467097849938052769718961535662524/3090007892803332518177914010771390705108642578125 OK
object/n17.json n=17 rows=2601 expected=2601 stop_actions=2010 toss_actions_a>=1=302 ties=0 values.txt=match claim.md=match 0.13s P000=1271934201995087824531562911568806911954931581879270794/2459066905905289914478405966393431096797847747802734375 OK
object/n18.json n=18 rows=3078 expected=3078 stop_actions=2413 toss_actions_a>=1=341 ties=0 values.txt=match claim.md=match 0.15s P000=28247088896509526684833556406803399555218653423253279570310576/54670177377720097529492873547468576365952718884944915771484375 OK
object/n19.json n=19 rows=3610 expected=3610 stop_actions=2867 toss_actions_a>=1=382 ties=0 values.txt=match claim.md=match 0.20s P000=669663748187798960299370649019840271261510564439147472414465579166/1297062327956481751434290613853888919555135964767181873321533203125 OK
object/n20.json n=20 rows=4200 expected=4200 stop_actions=3375 toss_actions_a>=1=425 ties=0 values.txt=match claim.md=match 0.25s P000=66496512444936569744985774803016169284564753386698071451174729031677100468/128914547048523848841946633205623295436534982031301567021310329437255859375 OK
object/n21.json n=21 rows=4851 expected=4851 stop_actions=3939 toss_actions_a>=1=471 ties=0 values.txt=match claim.md=match 0.39s P000=111506017688366777448294804048780848679891633742648200717299472558190830742933142/216312969043625586834394091016938476012952707399064376306031425297260284423828125 OK
object/n22.json n=22 rows=5566 expected=5566 stop_actions=4562 toss_actions_a>=1=520 ties=0 values.txt=match claim.md=match 0.37s P000=98464438447917488363682498105279276252661329626200725077373960946137587277745901020033888/191164528152750632498291857580802254790372867947797538744224673158205120265483856201171875 OK
object/n23.json n=23 rows=6348 expected=6348 stop_actions=5247 toss_actions_a>=1=572 ties=0 values.txt=match claim.md=match 0.37s P000=16804971339804096758701401983396389612430253637235128756923316729869921672392761537248494304314/32644552139761417392755728474915574806255682660139599218451756361121162763424217700958251953125 OK
object/n24.json n=24 rows=7200 expected=7200 stop_actions=5998 toss_actions_a>=1=626 ties=0 values.txt=match claim.md=match 0.32s P000=61641522672390175245757644635648262298380422505942592588283292482777067721800637786131054493341114886948/119824696944790069335614602894500771769506173197293213435836474253403683464919211934320628643035888671875 OK
object/n25.json n=25 rows=8125 expected=8125 stop_actions=6817 toss_actions_a>=1=683 ties=0 values.txt=match claim.md=match 0.37s P000=137799740253587894912750079334193352471902888649066272650494504655093000086917541531600474473921955918052077538/268001621353969033564488201183762263215809197939125044772058566108416328458450420290484116412699222564697265625 OK
object/n26.json n=26 rows=9126 expected=9126 stop_actions=7708 toss_actions_a>=1=742 ties=0 values.txt=match claim.md=match 0.59s P000=1809148908833348594429179385408107440488287589391109784528275292981556328694030057469124243164026099078084223921059592416/3520694156412391211453504380785833183621311911930851057416539725627792906208928233302221093388281879015266895294189453125 OK
object/n27.json n=27 rows=10206 expected=10206 stop_actions=8673 toss_actions_a>=1=804 ties=0 values.txt=match claim.md=match 0.93s P000=26978828619143617986506962181791275376141877848793476404504911821422889792150746055288205315610118902385415971911537007037686/52525408076411697592726002934532865350547697016760221422852045525839103999613242951841122687685152973863296210765838623046875 OK
object/n28.json n=28 rows=11368 expected=11368 stop_actions=9716 toss_actions_a>=1=868 ties=0 values.txt=match claim.md=match 0.67s P000=312160576922964658344907666418212246368316973188391968263343650805628616586935481907954960918612441256604098960643597286852349681744589484/608079889617649680999405301712627237930454343986707080286849263297541510325420914955502145856579496576274776012505753897130489349365234375 OK
object/n29.json n=29 rows=12615 expected=12615 stop_actions=10840 toss_actions_a>=1=934 ties=0 values.txt=match claim.md=match 0.87s P000=33705257918084471785019375413714503621216029613465763852036367174468480554838876567259337567412843015128753826028142180603642141147932125527875262/65682997455851143298074866368447290225455727005993252921753529111878847034002883960361175517390062566837828150454671447005239315330982208251953125 OK
object/n30.json n=30 rows=13950 expected=13950 stop_actions=12048 toss_actions_a>=1=1002 ties=0 values.txt=match claim.md=match 1.09s P000=9702985056846137933218838885572616340384403016127146978457034221965057701745757137014541922776337316721349279672358131437633281220605150594884452549908/18917905022615183330363147573849810192661703717605759820817809087417754543186212384734242490646960716312782354855096326940582002862356603145599365234375 OK
my_checker summary: 15 OK, 0 FAIL, of 15 files
(exit code 0)
```

### 2.3 Comparison summary

- **object/n16..n30.** For every certificate, P(0,0,0) is the identical reduced-fraction string on lines 16..30 of values.txt and in the claim.md table: 15/15 match.
- **calibration/n1..n15.** For every n = 1..15, the numerator equals the data/b387261.txt term and the denominator equals the data/b387262.txt term, and the two b-file terms are coprime. Each value also equals lines 1..15 of values.txt: 15/15 match.
- **Paper cross-check.** The paper's own printed terms are 2/3 (n=1, Sec. 2), 4/7 (n=2, Sec. 3.1), 6/11 (n=3, Secs. 2 and 3.2), 2236/4165, 1026/1925 and 275848876/521145625 (n=4, 5, 6, Sec. 3.3). They agree with the b-files and the calibration certificates. I did not re-fetch OEIS, because the brief only allowed the arXiv fetches. For n = 7..15 the comparison is against the b-files as shipped and hash-checked in claim/.
- **All 30 certificates.** Each has a complete position set, every value reduced and in [0,1], and every equation holding exactly. Every claimed action attains the max. There are 0 exact ties (continue == stop) anywhere, so every claimed action is the unique optimal action.

### 2.4 Is my checker sensitive? Mutation tests

The script <scratch>/mutation_test.py starts from a real certificate and corrupts it. Every corrupted file must be rejected, and the unmodified and row-shuffled files must be accepted.

The "M10" cases are certificates that are self-consistent under a sub-optimal policy. I built them with my exact policy evaluator: one optimal action is flipped and the whole table is re-solved exactly, or the policy is always-toss or always-stop.

```
n=2 M00_unmodified               expect=accept -> accepted [as expected]
n=2 M13_rows_shuffled            expect=accept -> accepted [as expected]
n=2 M01_value_perturbed          expect=reject -> rejected: forced-toss equation fails at (0, 0, 1) [as expected]
n=2 M02_toss_to_stop             expect=reject -> rejected: claimed stop does not attain the max at (1, 0, 0) [as expected]
n=2 M04_a0_action_stop           expect=reject -> rejected: action at a=0 is 'stop', not toss, at (0, 0, 0) [as expected]
n=2 M05_row_deleted              expect=reject -> rejected: position set wrong: rows=5 expected=6 missing=1 extra=0 [as expected]
n=2 M06_row_duplicated           expect=reject -> rejected: row 6: duplicate position (0, 1, 1) [as expected]
n=2 M07_out_of_range_row         expect=reject -> rejected: row 6: position (2,0,0) out of range [as expected]
n=2 M08_non_reduced              expect=reject -> rejected: row 3 (1, 0, 1): fraction not reduced: 6/10 [as expected]
n=2 M09_P000_differs             expect=reject -> rejected: P000 field differs from table value at (0,0,0) [as expected]
n=2 M14_leading_zero             expect=reject -> rejected: row 3 (1, 0, 1): value not in canonical num/den form: '03/5' [as expected]
n=2 M15_bool_coordinate          expect=reject -> rejected: row 0: a is not an int: False [as expected]
n=2 M16_extra_key                expect=reject -> rejected: top-level keys are ['P000', 'extra', 'n', 'table'], expected exactly n, P000, table [as expected]
n=2 M17_n_mismatch               expect=reject -> rejected: file name n2.json does not match n=3 [as expected]
n=2 M20_float_value              expect=reject -> rejected: float literal in JSON: '0.5' [as expected]
n=2 M21_duplicate_json_key       expect=reject -> rejected: duplicate JSON key 'P000' [as expected]
n=2 M10_subopt_flip_1_0_0        expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=2 M10_subopt_always_toss       expect=reject -> accepted [UNEXPECTED]
n=2 M10_subopt_always_stop       expect=reject -> rejected: value != max(continue, stop) at (1, 0, 1) [as expected]
mutation summary n=2: SOME UNEXPECTED
n=6 M00_unmodified               expect=accept -> accepted [as expected]
n=6 M13_rows_shuffled            expect=accept -> accepted [as expected]
n=6 M01_value_perturbed          expect=reject -> rejected: value != max(continue, stop) at (1, 1, 5) [as expected]
n=6 M02_toss_to_stop             expect=reject -> rejected: claimed stop does not attain the max at (1, 0, 0) [as expected]
n=6 M03_stop_to_toss             expect=reject -> rejected: claimed toss does not attain the max at (2, 0, 0) [as expected]
n=6 M04_a0_action_stop           expect=reject -> rejected: action at a=0 is 'stop', not toss, at (0, 0, 0) [as expected]
n=6 M05_row_deleted              expect=reject -> rejected: position set wrong: rows=125 expected=126 missing=1 extra=0 [as expected]
n=6 M06_row_duplicated           expect=reject -> rejected: row 126: duplicate position (1, 0, 1) [as expected]
n=6 M07_out_of_range_row         expect=reject -> rejected: row 126: position (6,0,0) out of range [as expected]
n=6 M08_non_reduced              expect=reject -> rejected: row 63 (2, 1, 5): fraction not reduced: 10/66 [as expected]
n=6 M09_P000_differs             expect=reject -> rejected: P000 field differs from table value at (0,0,0) [as expected]
n=6 M14_leading_zero             expect=reject -> rejected: row 63 (2, 1, 5): value not in canonical num/den form: '05/33' [as expected]
n=6 M15_bool_coordinate          expect=reject -> rejected: row 0: a is not an int: False [as expected]
n=6 M16_extra_key                expect=reject -> rejected: top-level keys are ['P000', 'extra', 'n', 'table'], expected exactly n, P000, table [as expected]
n=6 M17_n_mismatch               expect=reject -> rejected: file name n6.json does not match n=7 [as expected]
n=6 M20_float_value              expect=reject -> rejected: float literal in JSON: '0.5' [as expected]
n=6 M21_duplicate_json_key       expect=reject -> rejected: duplicate JSON key 'P000' [as expected]
n=6 M10_subopt_flip_1_0_0        expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=6 M10_subopt_flip_2_0_0        expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=6 M10_subopt_always_toss       expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=6 M10_subopt_always_stop       expect=reject -> rejected: value != max(continue, stop) at (1, 0, 1) [as expected]
mutation summary n=6: ALL AS EXPECTED
exit=0
n=16 M00_unmodified               expect=accept -> accepted [as expected]
n=16 M13_rows_shuffled            expect=accept -> accepted [as expected]
n=16 M01_value_perturbed          expect=reject -> rejected: value != max(continue, stop) at (4, 4, 13) [as expected]
n=16 M02_toss_to_stop             expect=reject -> rejected: claimed stop does not attain the max at (1, 0, 0) [as expected]
n=16 M03_stop_to_toss             expect=reject -> rejected: claimed toss does not attain the max at (2, 0, 0) [as expected]
n=16 M04_a0_action_stop           expect=reject -> rejected: action at a=0 is 'stop', not toss, at (0, 0, 0) [as expected]
n=16 M05_row_deleted              expect=reject -> rejected: position set wrong: rows=2175 expected=2176 missing=1 extra=0 [as expected]
n=16 M06_row_duplicated           expect=reject -> rejected: row 2176: duplicate position (7, 0, 0) [as expected]
n=16 M07_out_of_range_row         expect=reject -> rejected: row 2176: position (16,0,0) out of range [as expected]
n=16 M08_non_reduced              expect=reject -> rejected: row 1088 (4, 4, 13): fraction not reduced: 677049826/13418291250 [as expected]
n=16 M09_P000_differs             expect=reject -> rejected: P000 field differs from table value at (0,0,0) [as expected]
n=16 M14_leading_zero             expect=reject -> rejected: row 1088 (4, 4, 13): value not in canonical num/den form: '0338524913/6709145625' [as expected]
n=16 M15_bool_coordinate          expect=reject -> rejected: row 0: a is not an int: False [as expected]
n=16 M16_extra_key                expect=reject -> rejected: top-level keys are ['P000', 'extra', 'n', 'table'], expected exactly n, P000, table [as expected]
n=16 M17_n_mismatch               expect=reject -> rejected: file name n16.json does not match n=17 [as expected]
n=16 M20_float_value              expect=reject -> rejected: float literal in JSON: '0.5' [as expected]
n=16 M21_duplicate_json_key       expect=reject -> rejected: duplicate JSON key 'P000' [as expected]
n=16 M10_subopt_flip_1_0_0        expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=16 M10_subopt_flip_2_0_0        expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=16 M10_subopt_always_toss       expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=16 M10_subopt_always_stop       expect=reject -> rejected: value != max(continue, stop) at (1, 0, 1) [as expected]
mutation summary n=16: ALL AS EXPECTED
exit=0
n=30 M00_unmodified               expect=accept -> accepted [as expected]
n=30 M13_rows_shuffled            expect=accept -> accepted [as expected]
n=30 M01_value_perturbed          expect=reject -> rejected: value != max(continue, stop) at (21, 8, 27) [as expected]
n=30 M02_toss_to_stop             expect=reject -> rejected: claimed stop does not attain the max at (1, 0, 0) [as expected]
n=30 M03_stop_to_toss             expect=reject -> rejected: claimed toss does not attain the max at (2, 0, 0) [as expected]
n=30 M04_a0_action_stop           expect=reject -> rejected: action at a=0 is 'stop', not toss, at (0, 0, 0) [as expected]
n=30 M05_row_deleted              expect=reject -> rejected: position set wrong: rows=13949 expected=13950 missing=1 extra=0 [as expected]
n=30 M06_row_duplicated           expect=reject -> rejected: row 13950: duplicate position (7, 0, 0) [as expected]
n=30 M07_out_of_range_row         expect=reject -> rejected: row 13950: position (30,0,0) out of range [as expected]
n=30 M08_non_reduced              expect=reject -> rejected: row 6975 (21, 8, 27): fraction not reduced: 14/18 [as expected]
n=30 M09_P000_differs             expect=reject -> rejected: P000 field differs from table value at (0,0,0) [as expected]
n=30 M14_leading_zero             expect=reject -> rejected: row 6975 (21, 8, 27): value not in canonical num/den form: '07/9' [as expected]
n=30 M15_bool_coordinate          expect=reject -> rejected: row 0: a is not an int: False [as expected]
n=30 M16_extra_key                expect=reject -> rejected: top-level keys are ['P000', 'extra', 'n', 'table'], expected exactly n, P000, table [as expected]
n=30 M17_n_mismatch               expect=reject -> rejected: file name n30.json does not match n=31 [as expected]
n=30 M20_float_value              expect=reject -> rejected: float literal in JSON: '0.5' [as expected]
n=30 M21_duplicate_json_key       expect=reject -> rejected: duplicate JSON key 'P000' [as expected]
n=30 M10_subopt_flip_1_0_0        expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=30 M10_subopt_flip_2_0_0        expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=30 M10_subopt_always_toss       expect=reject -> rejected: value != max(continue, stop) at (1, 0, 0) [as expected]
n=30 M10_subopt_always_stop       expect=reject -> rejected: value != max(continue, stop) at (1, 0, 1) [as expected]
mutation summary n=30: ALL AS EXPECTED
exit=0
```

Two notes on how these runs were set up:
- My first n=2 run aborted inside my test harness, which looked for a non-existent row index. I fixed the harness and the n=2 output above is the rerun.
- For n=2 the "always toss" case is correctly accepted. The optimal n=2 policy really is all-toss: calibration/n2.json has no "stop", and the generated file is byte-identical to calibration/n2.json.

I also ran two control runs of the comparison step:
- values.txt with the n=16 numerator changed (still a reduced fraction) gives "values.txt=MISMATCH ... FAIL(comparison)" and exit code 1.
- data/b387261.txt with the n=10 numerator changed gives "oeis=MISMATCH ... FAIL(comparison)".

### 2.5 Independent exact solver (also mine, written before I opened solver/solver.py)

My solver is <scratch>/my_solver.py. It processes pairs {(.,b,c),(.,c,b)} in decreasing order of the banked total b + c. Every stop successor (0,c,a+b) has a larger banked total and is therefore already exact, so the only cycle is through the two tail values x = P(0,b,c) and y = P(0,c,b). For a policy pair, summarised by the first stop index k, the solver solves x = (1-2^-k)(1-y) + 2^-k T and the matching equation for y exactly. It then re-runs the exact Bellman max recursion at the solution and accepts the pair only if that recursion reproduces (x, y) exactly. Floats are used only for the first policy guess.

The solver compares all values and actions with the certificates:

```
n=1 positions=1 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.01s IDENTICAL
n=2 positions=6 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.01s IDENTICAL
n=3 positions=18 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.01s IDENTICAL
n=4 positions=40 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.02s IDENTICAL
n=5 positions=75 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.02s IDENTICAL
n=6 positions=126 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.03s IDENTICAL
n=7 positions=196 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.06s IDENTICAL
n=8 positions=288 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.06s IDENTICAL
n=9 positions=405 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.08s IDENTICAL
n=10 positions=550 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.10s IDENTICAL
n=11 positions=726 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.13s IDENTICAL
n=12 positions=936 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.18s IDENTICAL
n=13 positions=1183 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.19s IDENTICAL
n=14 positions=1470 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.25s IDENTICAL
n=15 positions=1800 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.30s IDENTICAL
n=16 positions=2176 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.34s IDENTICAL
n=17 positions=2601 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.39s IDENTICAL
n=18 positions=3078 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.48s IDENTICAL
n=19 positions=3610 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.52s IDENTICAL
n=20 positions=4200 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.64s IDENTICAL
n=21 positions=4851 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.68s IDENTICAL
n=22 positions=5566 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 1.06s IDENTICAL
n=23 positions=6348 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 0.84s IDENTICAL
n=24 positions=7200 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 1.03s IDENTICAL
n=25 positions=8125 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 1.19s IDENTICAL
n=26 positions=9126 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 1.36s IDENTICAL
n=27 positions=10206 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 1.44s IDENTICAL
n=28 positions=11368 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 1.60s IDENTICAL
n=29 positions=12615 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 1.93s IDENTICAL
n=30 positions=13950 my_ties=0 max_policy_iters=1 value_mismatches=0 action_mismatches=0 P000_equal=True 2.12s IDENTICAL
my_solver summary: all identical
```

All 30 tables, n = 1..30 and 112,840 positions in total, are reproduced value-for-value and action-for-action by code that shares nothing with the author's.

### 2.6 Extra consistency checks (<scratch>/extra_checks.py)

```
cross-certificate shift check P_n(a,b,c) == P_{n+1}(a,b+1,c+1) (value and action): 98890 positions checked over n=1..29, 0 mismatches
Table 1 rows parsed: 19 (labels [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
Table 1 entries compared: 361, mismatches: 0 []
```

- **Shift check.** The game depends only on the points each player still needs, so P_n(a,b,c) must equal P_{n+1}(a,b+1,c+1). This holds with 0 mismatches across all 30 certificates.
- **Paper Table 1.** Table 1 gives the coins to toss for needs 2..20 x 2..20. All 361 entries equal the first stop index in object/n20.json.
- **Paper Section 3.3, n=4.** The paper says the optimal strategy is "to stop at (1, 2, 0), (2, 0, 0) and (2, 0, 2) and else to continue". Under the certificate's own policy, starting from (0,0,0), the reachable stop positions of calibration/n4.json are exactly (1,2,0), (2,0,0) and (2,0,2). The other 8 stop positions are unreachable under optimal play.
- **Paper Section 2, n=3.** The values P(0,2,0)=8/9, P(0,1,0)=8/11, P(0,0,0)=6/11, P(0,2,1)=4/5, P(0,2,2)=2/3, P(0,1,1)=4/7, P(0,1,2)=2/5, P(0,0,1)=4/11 and P(0,0,2)=2/9 all equal the entries of calibration/n3.json. So does Section 3.2's P(1,0,2) = 1/3, where continue = 1/3 and stop = 1/5.

## 3. Does the definition match the paper?

- **Rules.** Section 1, quoted above, matches the claim's game statement point by point. A head adds one open point, after which the player stops (banks, turn passes) or continues. A tail loses all open points and passes the turn. The first to n points wins. Section 1 also states the x-coins variant as "logically exactly the same game". **Match.**
- **Equations.** Section 4 gives P(0,b,c) = 1/2 (1 - P(0,c,b)) + 1/2 P(1,b,c), with no max. For a >= 1 it gives continue = 1/2 (1 - P(0,c,b)) + 1/2 P(a+1,b,c) and stop = 1 - P(0,c,a+b), and the player picks the better one. These are identical to the claim's equations, including both "1 - P" terms. After a tail the opponent moves at (0,c,b); after a stop the opponent moves at (0,c,a+b). **Match.**
- **"Reaching n with open points is a win" is the paper's convention: yes.**
  - Section 4: "if a+b=n, then Pmin(a, b, c) := Pmax(a, b, c) := 1", where a counts open points.
  - Section 2, n=3: "If player 1 tosses heads they win", so x2 = 1/2 + 1/2 y2 at (0,2,0). Also "stops after 3. throw, then x0 = 7/8 y0 + 1/8".
  - Section 3.1, n=2: "P100 = 1/2 (1 - P000) + 1/2".
  - Section 5: "If player 1 needs only one more point ... they toss only one more time".
  - A must-bank variant would give the same values anyway. Stopping is always allowed at a >= 1, and each head adds exactly one point, so a + b reaches exactly n and the player would bank at once.
- **"Forced toss at a = 0" is the paper's convention: yes.** Section 1 says "A player whose turn it is tosses a coin", and the Section 4 equation for P(0,b,c) has no stop option.
- **Positions.** The paper says there are n/2 (3n - 1) new positions per step (12, 22, 35 and 51 for n = 3..6) and (n-1)n^2/2 decision positions with a >= 1. These are consistent with the claim's n^2(n+1)/2 total: n^2(n+1)/2 - (n-1)^2 n/2 = n(3n-1)/2.
- **Observation, not a defect of the claim.** In Section 3.2 the paper's printed equation list gives the stop alternative for positions with one open point as, for example, "P100 = 1/2 (1 - P000) + 1/2 (1 - P001)", and similarly "(1 - P011)" for P101 and "(1 - P021)" for P102. That form fits neither the Section 3.1 reading, where stopping after the next head would bank 2 points, nor the Section 4 reading, where stop = 1 - P001 with no coin factor. It looks like a typesetting slip. The paper's own Section 3.2 numbers (1/3 versus 1/5 at (1,0,2), the result 6/11, stop at (1,0,0)) follow the Section 4 convention, which is the one the claim uses. Every number the paper prints is reproduced by the certificates.

## 4. The proof note, re-derived step by step

Notation: P and Q are two exact solutions, e = |P - Q|, and D = max e. D is finite because the state space is finite.

1. **Non-expansion: "|P - Q| at a position is at most the maximum over actions of the expected |P - Q| at the successors". Verified.**
   - At a = 0: e(0,b,c) <= 1/2 e(0,c,b) + 1/2 e(1,b,c), because |(1-P)-(1-Q)| = |P-Q|.
   - At a >= 1: |max(x1,x2) - max(y1,y2)| <= max(|x1-y1|, |x2-y2|), with |x1-y1| <= 1/2 e(0,c,b) + 1/2 e(a+1,b,c) and |x2-y2| = e(0,c,a+b).
   - At terminal positions (a + b >= n), both solutions equal 1, so e = 0.
2. **Unrolling: "after K steps |P - Q|(s) <= D * r_K(s)". Verified.** Induction on K gives e(s) <= sup E[e(S_K)], where the sup is over action choices at every position for both players, possibly history-dependent; that is a strategy pair. Since e = 0 at terminal states and e <= D elsewhere, this is at most D * Pr(the game is running at step K) <= D * r_K(s).
3. **"In any block of 2n steps there are at least n tosses (a stop is always followed by a forced toss)". Verified.** A stop moves to an a = 0 position, where the toss is forced, so two stops are never consecutive. At most n of any 2n consecutive steps can be stops.
4. **"if they are all heads (probability >= 2^-n, independent of the strategies) the player who tossed first either reaches n (game over) or banks >= 1 point". Verified, with a precise reading.**
   - Read the event as "the first n tosses of the block are heads". That has probability exactly 2^-n whatever the strategies: the coins are fair and independent, and the strategies only decide whether a toss happens.
   - Under this event, let X be the first player to toss in the block. At most one step precedes that toss: a stop by the other player, which itself banks >= 1.
   - After that, X has a >= 1 and each further toss by X is a head. Within at most n tosses, X either reaches a + b >= n (at most n - b <= n heads are needed) or stops with a >= 1 open points and banks >= 1.
   - This uses at most n + 2 <= 2n steps for n >= 2. For n = 1 no stop position exists and the first head wins.
   - Wording note: if "they" is read as every toss in the block (up to 2n of them), the probability is only >= 2^-2n. Steps 5-6 still give r_K < 1 and D = 0 with that constant. The wording is loose but the conclusion holds.
5. **"banked totals never fall and stay below n, so after 2n - 1 such blocks the game has ended". Verified.** While the game runs, b + c lies in {0, ..., 2n-2}. Tails remove only open points, so b + c never decreases, and each successful block raises it by >= 1. So 2n - 1 successful blocks cannot all happen while the game is still running.
6. **"Hence r_K <= 1 - 2^(-n(2n-1)) < 1 for K = 2n(2n-1), and D = 0". Verified.** Each block succeeds with conditional probability >= 2^-n given the past. Multiplying over the blocks, Pr(game over by step K) >= 2^(-n(2n-1)), uniformly over starting positions and strategy pairs. Then D <= D * max_s r_K(s) gives D (1 - max r_K) <= 0, so D = 0.
7. **Existence. Verified.** The certificate itself supplies a solution, and sections 2.1 and 2.2 show each certificate satisfies every equation exactly. It is therefore the unique solution.
8. **"the unique solution ... is the game value, and any action attaining the max is optimal". Verified.** The note cites this as KNOWN (Jehn Section 2; Glenn-Fang-Kruskal Theorem 2; Shapley 1953). I re-derived it with the standard argument. Let V be the solution and let player 1 play the argmax actions.
   - Player 1's value process W_t is V at player 1's turns and 1 - V at the opponent's turns. It is a submartingale against any opponent strategy. Player 1's argmax moves keep the expectation equal. At the opponent's turns, every action satisfies V(s) >= E[V(next), seen from the mover], because V is a max, so player 1's value 1 - V can only rise in expectation.
   - Steps 3-6 show the game ends almost surely under all strategies, with geometric tails.
   - W is bounded, so optional stopping gives Pr(player 1 wins) = E[W_T] >= V(0,0,0). The symmetric argument for the opponent bounds it from above.
   - There are 0 ties in every certificate, so the optimal action is unique at every position.

**Conclusion on the proof:** every step holds. A table that satisfies the equations exactly, as checked, is the optimal-play value table, and its P(0,0,0) is the claimed term.

## 5. The author's commands from REPRODUCE.md: real output

All commands ran from inside claim/. For step 5, REPRODUCE.md writes to claim/_rerun. To keep claim/ read-only I wrote to <scratch>/rerun1 and <scratch>/rerun2 instead and compared those against claim/. The commands are otherwise exactly as given.

### Step 1: hashes

```
$ shasum -a 256 -c SHA256SUMS
REPRODUCE.md: OK
calibration/n1.json: OK
calibration/n10.json: OK
calibration/n11.json: OK
calibration/n12.json: OK
calibration/n13.json: OK
calibration/n14.json: OK
calibration/n15.json: OK
calibration/n2.json: OK
calibration/n3.json: OK
calibration/n4.json: OK
calibration/n5.json: OK
calibration/n6.json: OK
calibration/n7.json: OK
calibration/n8.json: OK
calibration/n9.json: OK
checker/ros_cert_check.py: OK
claim.md: OK
data/b387261.txt: OK
data/b387262.txt: OK
object/n16.json: OK
object/n17.json: OK
object/n18.json: OK
object/n19.json: OK
object/n20.json: OK
object/n21.json: OK
object/n22.json: OK
object/n23.json: OK
object/n24.json: OK
object/n25.json: OK
object/n26.json: OK
object/n27.json: OK
object/n28.json: OK
object/n29.json: OK
object/n30.json: OK
solver/my_verify.py: OK
solver/solver.py: OK
values.txt: OK
(exit code 0; the only file in claim/ not listed in SHA256SUMS is SHA256SUMS itself)
```

### Step 2: checker on object/n16..n30

```
$ python3 -I checker/ros_cert_check.py object/n16.json ... object/n30.json
n16.json: n=16 positions_checked=2176 P000=1599710761252635467097849938052769718961535662524/3090007892803332518177914010771390705108642578125 PASS
n17.json: n=17 positions_checked=2601 P000=1271934201995087824531562911568806911954931581879270794/2459066905905289914478405966393431096797847747802734375 PASS
n18.json: n=18 positions_checked=3078 P000=28247088896509526684833556406803399555218653423253279570310576/54670177377720097529492873547468576365952718884944915771484375 PASS
n19.json: n=19 positions_checked=3610 P000=669663748187798960299370649019840271261510564439147472414465579166/1297062327956481751434290613853888919555135964767181873321533203125 PASS
n20.json: n=20 positions_checked=4200 P000=66496512444936569744985774803016169284564753386698071451174729031677100468/128914547048523848841946633205623295436534982031301567021310329437255859375 PASS
n21.json: n=21 positions_checked=4851 P000=111506017688366777448294804048780848679891633742648200717299472558190830742933142/216312969043625586834394091016938476012952707399064376306031425297260284423828125 PASS
n22.json: n=22 positions_checked=5566 P000=98464438447917488363682498105279276252661329626200725077373960946137587277745901020033888/191164528152750632498291857580802254790372867947797538744224673158205120265483856201171875 PASS
n23.json: n=23 positions_checked=6348 P000=16804971339804096758701401983396389612430253637235128756923316729869921672392761537248494304314/32644552139761417392755728474915574806255682660139599218451756361121162763424217700958251953125 PASS
n24.json: n=24 positions_checked=7200 P000=61641522672390175245757644635648262298380422505942592588283292482777067721800637786131054493341114886948/119824696944790069335614602894500771769506173197293213435836474253403683464919211934320628643035888671875 PASS
n25.json: n=25 positions_checked=8125 P000=137799740253587894912750079334193352471902888649066272650494504655093000086917541531600474473921955918052077538/268001621353969033564488201183762263215809197939125044772058566108416328458450420290484116412699222564697265625 PASS
n26.json: n=26 positions_checked=9126 P000=1809148908833348594429179385408107440488287589391109784528275292981556328694030057469124243164026099078084223921059592416/3520694156412391211453504380785833183621311911930851057416539725627792906208928233302221093388281879015266895294189453125 PASS
n27.json: n=27 positions_checked=10206 P000=26978828619143617986506962181791275376141877848793476404504911821422889792150746055288205315610118902385415971911537007037686/52525408076411697592726002934532865350547697016760221422852045525839103999613242951841122687685152973863296210765838623046875 PASS
n28.json: n=28 positions_checked=11368 P000=312160576922964658344907666418212246368316973188391968263343650805628616586935481907954960918612441256604098960643597286852349681744589484/608079889617649680999405301712627237930454343986707080286849263297541510325420914955502145856579496576274776012505753897130489349365234375 PASS
n29.json: n=29 positions_checked=12615 P000=33705257918084471785019375413714503621216029613465763852036367174468480554838876567259337567412843015128753826028142180603642141147932125527875262/65682997455851143298074866368447290225455727005993252921753529111878847034002883960361175517390062566837828150454671447005239315330982208251953125 PASS
n30.json: n=30 positions_checked=13950 P000=9702985056846137933218838885572616340384403016127146978457034221965057701745757137014541922776337316721349279672358131437633281220605150594884452549908/18917905022615183330363147573849810192661703717605759820817809087417754543186212384734242490646960716312782354855096326940582002862356603145599365234375 PASS
ALL_PASS
(exit code 0)
```

### Step 3: checker on calibration/n1..n15 with --oeis data

```
$ python3 -I checker/ros_cert_check.py --oeis data calibration/n1.json ... calibration/n15.json
n1.json: n=1 positions_checked=1 P000=2/3 oeis_match=yes PASS
n2.json: n=2 positions_checked=6 P000=4/7 oeis_match=yes PASS
n3.json: n=3 positions_checked=18 P000=6/11 oeis_match=yes PASS
n4.json: n=4 positions_checked=40 P000=2236/4165 oeis_match=yes PASS
n5.json: n=5 positions_checked=75 P000=1026/1925 oeis_match=yes PASS
n6.json: n=6 positions_checked=126 P000=275848876/521145625 oeis_match=yes PASS
n7.json: n=7 positions_checked=196 P000=649346842/1231278125 oeis_match=yes PASS
n8.json: n=8 positions_checked=288 P000=61550866190068/117192622421875 oeis_match=yes PASS
n9.json: n=9 positions_checked=405 P000=2737872156886/5225432428125 oeis_match=yes PASS
n10.json: n=10 positions_checked=550 P000=5556238701119487884/10634368774326171875 oeis_match=yes PASS
n11.json: n=11 positions_checked=726 P000=33857036312840796476194/64913928515324560546875 oeis_match=yes PASS
n12.json: n=12 positions_checked=936 P000=3393041394611453189295265268/6519012951936493553466796875 oeis_match=yes PASS
n13.json: n=13 positions_checked=1183 P000=218370486707916654640780231642/420117998909827688127861328125 oeis_match=yes PASS
n14.json: n=14 positions_checked=1470 P000=112630244896738642814653528498087299988/217038092253876925088545128021240234375 oeis_match=yes PASS
n15.json: n=15 positions_checked=1800 P000=14364898791782224577113184680141626682/27711032758513212360715995025634765625 oeis_match=yes PASS
ALL_PASS
(exit code 0)
```

### Step 4: solver/my_verify.py

```
$ python3 -I solver/my_verify.py --oeis data calibration/n*.json object/n*.json
PASS calibration/n1.json n=1 positions=1 stop_actions=0 exact_ties=0 OEIS-MATCH P(0,0,0)=2/3
PASS calibration/n10.json n=10 positions=550 stop_actions=354 exact_ties=0 OEIS-MATCH P(0,0,0)=5556238701119487884/10634368774326171875
PASS calibration/n11.json n=11 positions=726 stop_actions=487 exact_ties=0 OEIS-MATCH P(0,0,0)=33857036312840796476194/64913928515324560546875
PASS calibration/n12.json n=12 positions=936 stop_actions=650 exact_ties=0 OEIS-MATCH P(0,0,0)=3393041394611453189295265268/6519012951936493553466796875
PASS calibration/n13.json n=13 positions=1183 stop_actions=844 exact_ties=0 OEIS-MATCH P(0,0,0)=218370486707916654640780231642/420117998909827688127861328125
PASS calibration/n14.json n=14 positions=1470 stop_actions=1075 exact_ties=0 OEIS-MATCH P(0,0,0)=112630244896738642814653528498087299988/217038092253876925088545128021240234375
PASS calibration/n15.json n=15 positions=1800 stop_actions=1344 exact_ties=0 OEIS-MATCH P(0,0,0)=14364898791782224577113184680141626682/27711032758513212360715995025634765625
PASS calibration/n2.json n=2 positions=6 stop_actions=0 exact_ties=0 OEIS-MATCH P(0,0,0)=4/7
PASS calibration/n3.json n=3 positions=18 stop_actions=2 exact_ties=0 OEIS-MATCH P(0,0,0)=6/11
PASS calibration/n4.json n=4 positions=40 stop_actions=11 exact_ties=0 OEIS-MATCH P(0,0,0)=2236/4165
PASS calibration/n5.json n=5 positions=75 stop_actions=29 exact_ties=0 OEIS-MATCH P(0,0,0)=1026/1925
PASS calibration/n6.json n=6 positions=126 stop_actions=59 exact_ties=0 OEIS-MATCH P(0,0,0)=275848876/521145625
PASS calibration/n7.json n=7 positions=196 stop_actions=103 exact_ties=0 OEIS-MATCH P(0,0,0)=649346842/1231278125
PASS calibration/n8.json n=8 positions=288 stop_actions=165 exact_ties=0 OEIS-MATCH P(0,0,0)=61550866190068/117192622421875
PASS calibration/n9.json n=9 positions=405 stop_actions=247 exact_ties=0 OEIS-MATCH P(0,0,0)=2737872156886/5225432428125
PASS object/n16.json n=16 positions=2176 stop_actions=1655 exact_ties=0 n/a P(0,0,0)=1599710761252635467097849938052769718961535662524/3090007892803332518177914010771390705108642578125
PASS object/n17.json n=17 positions=2601 stop_actions=2010 exact_ties=0 n/a P(0,0,0)=1271934201995087824531562911568806911954931581879270794/2459066905905289914478405966393431096797847747802734375
PASS object/n18.json n=18 positions=3078 stop_actions=2413 exact_ties=0 n/a P(0,0,0)=28247088896509526684833556406803399555218653423253279570310576/54670177377720097529492873547468576365952718884944915771484375
PASS object/n19.json n=19 positions=3610 stop_actions=2867 exact_ties=0 n/a P(0,0,0)=669663748187798960299370649019840271261510564439147472414465579166/1297062327956481751434290613853888919555135964767181873321533203125
PASS object/n20.json n=20 positions=4200 stop_actions=3375 exact_ties=0 n/a P(0,0,0)=66496512444936569744985774803016169284564753386698071451174729031677100468/128914547048523848841946633205623295436534982031301567021310329437255859375
PASS object/n21.json n=21 positions=4851 stop_actions=3939 exact_ties=0 n/a P(0,0,0)=111506017688366777448294804048780848679891633742648200717299472558190830742933142/216312969043625586834394091016938476012952707399064376306031425297260284423828125
PASS object/n22.json n=22 positions=5566 stop_actions=4562 exact_ties=0 n/a P(0,0,0)=98464438447917488363682498105279276252661329626200725077373960946137587277745901020033888/191164528152750632498291857580802254790372867947797538744224673158205120265483856201171875
PASS object/n23.json n=23 positions=6348 stop_actions=5247 exact_ties=0 n/a P(0,0,0)=16804971339804096758701401983396389612430253637235128756923316729869921672392761537248494304314/32644552139761417392755728474915574806255682660139599218451756361121162763424217700958251953125
PASS object/n24.json n=24 positions=7200 stop_actions=5998 exact_ties=0 n/a P(0,0,0)=61641522672390175245757644635648262298380422505942592588283292482777067721800637786131054493341114886948/119824696944790069335614602894500771769506173197293213435836474253403683464919211934320628643035888671875
PASS object/n25.json n=25 positions=8125 stop_actions=6817 exact_ties=0 n/a P(0,0,0)=137799740253587894912750079334193352471902888649066272650494504655093000086917541531600474473921955918052077538/268001621353969033564488201183762263215809197939125044772058566108416328458450420290484116412699222564697265625
PASS object/n26.json n=26 positions=9126 stop_actions=7708 exact_ties=0 n/a P(0,0,0)=1809148908833348594429179385408107440488287589391109784528275292981556328694030057469124243164026099078084223921059592416/3520694156412391211453504380785833183621311911930851057416539725627792906208928233302221093388281879015266895294189453125
PASS object/n27.json n=27 positions=10206 stop_actions=8673 exact_ties=0 n/a P(0,0,0)=26978828619143617986506962181791275376141877848793476404504911821422889792150746055288205315610118902385415971911537007037686/52525408076411697592726002934532865350547697016760221422852045525839103999613242951841122687685152973863296210765838623046875
PASS object/n28.json n=28 positions=11368 stop_actions=9716 exact_ties=0 n/a P(0,0,0)=312160576922964658344907666418212246368316973188391968263343650805628616586935481907954960918612441256604098960643597286852349681744589484/608079889617649680999405301712627237930454343986707080286849263297541510325420914955502145856579496576274776012505753897130489349365234375
PASS object/n29.json n=29 positions=12615 stop_actions=10840 exact_ties=0 n/a P(0,0,0)=33705257918084471785019375413714503621216029613465763852036367174468480554838876567259337567412843015128753826028142180603642141147932125527875262/65682997455851143298074866368447290225455727005993252921753529111878847034002883960361175517390062566837828150454671447005239315330982208251953125
PASS object/n30.json n=30 positions=13950 stop_actions=12048 exact_ties=0 n/a P(0,0,0)=9702985056846137933218838885572616340384403016127146978457034221965057701745757137014541922776337316721349279672358131437633281220605150594884452549908/18917905022615183330363147573849810192661703717605759820817809087417754543186212384734242490646960716312782354855096326940582002862356603145599365234375
my_verify summary: 30 passed, 0 failed, of 30 certificates
(exit code 0)
```

### Step 5: regeneration from scratch, run 1

```
$ mkdir -p <scratch>/rerun1 && python3 -I solver/solver.py 30 <scratch>/rerun1 1 30 <scratch>/rerun1/values.txt --b-dir data
solver: N = 30 (points-needed table 1 <= i, j <= N), certs n = 1..30
exact solve time: 4.00 s; components: 465; h-evaluations: total 1746, max 5; bisection steps: 0
histogram of h-evaluations per component: [(2, 58), (3, 15), (4, 375), (5, 17)]
exact ties (cont == stop) found: 0
wrote values table <scratch>/rerun1/values.txt
OEIS n= 1: MATCH  mine=2/3  oeis=2/3
OEIS n= 2: MATCH  mine=4/7  oeis=4/7
OEIS n= 3: MATCH  mine=6/11  oeis=6/11
OEIS n= 4: MATCH  mine=2236/4165  oeis=2236/4165
OEIS n= 5: MATCH  mine=1026/1925  oeis=1026/1925
OEIS n= 6: MATCH  mine=275848876/521145625  oeis=275848876/521145625
OEIS n= 7: MATCH  mine=649346842/1231278125  oeis=649346842/1231278125
OEIS n= 8: MATCH  mine=61550866190068/117192622421875  oeis=61550866190068/117192622421875
OEIS n= 9: MATCH  mine=2737872156886/5225432428125  oeis=2737872156886/5225432428125
OEIS n=10: MATCH  mine=5556238701119487884/10634368774326171875  oeis=5556238701119487884/10634368774326171875
OEIS n=11: MATCH  mine=33857036312840796476194/64913928515324560546875  oeis=33857036312840796476194/64913928515324560546875
OEIS n=12: MATCH  mine=3393041394611453189295265268/6519012951936493553466796875  oeis=3393041394611453189295265268/6519012951936493553466796875
OEIS n=13: MATCH  mine=218370486707916654640780231642/420117998909827688127861328125  oeis=218370486707916654640780231642/420117998909827688127861328125
OEIS n=14: MATCH  mine=112630244896738642814653528498087299988/217038092253876925088545128021240234375  oeis=112630244896738642814653528498087299988/217038092253876925088545128021240234375
OEIS n=15: MATCH  mine=14364898791782224577113184680141626682/27711032758513212360715995025634765625  oeis=14364898791782224577113184680141626682/27711032758513212360715995025634765625
OEIS comparison n<=15: ALL MATCH
wrote <scratch>/rerun1/n1.json (1 positions, 51 bytes) P000 = 2/3
wrote <scratch>/rerun1/n2.json (6 positions, 156 bytes) P000 = 4/7
wrote <scratch>/rerun1/n3.json (18 positions, 416 bytes) P000 = 6/11
wrote <scratch>/rerun1/n4.json (40 positions, 952 bytes) P000 = 2236/4165
wrote <scratch>/rerun1/n5.json (75 positions, 1792 bytes) P000 = 1026/1925
wrote <scratch>/rerun1/n6.json (126 positions, 3217 bytes) P000 = 275848876/521145625
wrote <scratch>/rerun1/n7.json (196 positions, 5298 bytes) P000 = 649346842/1231278125
wrote <scratch>/rerun1/n8.json (288 positions, 8346 bytes) P000 = 61550866190068/117192622421875
wrote <scratch>/rerun1/n9.json (405 positions, 12500 bytes) P000 = 2737872156886/5225432428125
wrote <scratch>/rerun1/n10.json (550 positions, 18311 bytes) P000 = 5556238701119487884/10634368774326171875
wrote <scratch>/rerun1/n11.json (726 positions, 26050 bytes) P000 = 33857036312840796476194/64913928515324560546875
wrote <scratch>/rerun1/n12.json (936 positions, 36181 bytes) P000 = 3393041394611453189295265268/6519012951936493553466796875
wrote <scratch>/rerun1/n13.json (1183 positions, 49360 bytes) P000 = 218370486707916654640780231642/420117998909827688127861328125
wrote <scratch>/rerun1/n14.json (1470 positions, 66384 bytes) P000 = 112630244896738642814653528498087299988/217038092253876925088545128021240234375
wrote <scratch>/rerun1/n15.json (1800 positions, 87290 bytes) P000 = 14364898791782224577113184680141626682/27711032758513212360715995025634765625
wrote <scratch>/rerun1/n16.json (2176 positions, 113871 bytes) P000 = 1599710761252635467097849938052769718961535662524/3090007892803332518177914010771390705108642578125
wrote <scratch>/rerun1/n17.json (2601 positions, 147147 bytes) P000 = 1271934201995087824531562911568806911954931581879270794/2459066905905289914478405966393431096797847747802734375
wrote <scratch>/rerun1/n18.json (3078 positions, 187610 bytes) P000 = 28247088896509526684833556406803399555218653423253279570310576/54670177377720097529492873547468576365952718884944915771484375
wrote <scratch>/rerun1/n19.json (3610 positions, 236269 bytes) P000 = 669663748187798960299370649019840271261510564439147472414465579166/1297062327956481751434290613853888919555135964767181873321533203125
wrote <scratch>/rerun1/n20.json (4200 positions, 295030 bytes) P000 = 66496512444936569744985774803016169284564753386698071451174729031677100468/128914547048523848841946633205623295436534982031301567021310329437255859375
wrote <scratch>/rerun1/n21.json (4851 positions, 364571 bytes) P000 = 111506017688366777448294804048780848679891633742648200717299472558190830742933142/216312969043625586834394091016938476012952707399064376306031425297260284423828125
wrote <scratch>/rerun1/n22.json (5566 positions, 447266 bytes) P000 = 98464438447917488363682498105279276252661329626200725077373960946137587277745901020033888/191164528152750632498291857580802254790372867947797538744224673158205120265483856201171875
wrote <scratch>/rerun1/n23.json (6348 positions, 544729 bytes) P000 = 16804971339804096758701401983396389612430253637235128756923316729869921672392761537248494304314/32644552139761417392755728474915574806255682660139599218451756361121162763424217700958251953125
wrote <scratch>/rerun1/n24.json (7200 positions, 658200 bytes) P000 = 61641522672390175245757644635648262298380422505942592588283292482777067721800637786131054493341114886948/119824696944790069335614602894500771769506173197293213435836474253403683464919211934320628643035888671875
wrote <scratch>/rerun1/n25.json (8125 positions, 790531 bytes) P000 = 137799740253587894912750079334193352471902888649066272650494504655093000086917541531600474473921955918052077538/268001621353969033564488201183762263215809197939125044772058566108416328458450420290484116412699222564697265625
wrote <scratch>/rerun1/n26.json (9126 positions, 944677 bytes) P000 = 1809148908833348594429179385408107440488287589391109784528275292981556328694030057469124243164026099078084223921059592416/3520694156412391211453504380785833183621311911930851057416539725627792906208928233302221093388281879015266895294189453125
wrote <scratch>/rerun1/n27.json (10206 positions, 1119382 bytes) P000 = 26978828619143617986506962181791275376141877848793476404504911821422889792150746055288205315610118902385415971911537007037686/52525408076411697592726002934532865350547697016760221422852045525839103999613242951841122687685152973863296210765838623046875
wrote <scratch>/rerun1/n28.json (11368 positions, 1320622 bytes) P000 = 312160576922964658344907666418212246368316973188391968263343650805628616586935481907954960918612441256604098960643597286852349681744589484/608079889617649680999405301712627237930454343986707080286849263297541510325420914955502145856579496576274776012505753897130489349365234375
wrote <scratch>/rerun1/n29.json (12615 positions, 1550909 bytes) P000 = 33705257918084471785019375413714503621216029613465763852036367174468480554838876567259337567412843015128753826028142180603642141147932125527875262/65682997455851143298074866368447290225455727005993252921753529111878847034002883960361175517390062566837828150454671447005239315330982208251953125
wrote <scratch>/rerun1/n30.json (13950 positions, 1811431 bytes) P000 = 9702985056846137933218838885572616340384403016127146978457034221965057701745757137014541922776337316721349279672358131437633281220605150594884452549908/18917905022615183330363147573849810192661703717605759820817809087417754543186212384734242490646960716312782354855096326940582002862356603145599365234375
certificate writing time: 1.95 s
python3 -I solver/solver.py 30 <scratch>/rerun1 1 30 <scratch>/rerun1/values.txt --b-dir data  1.47s user 0.09s system 23% cpu 6.643 total
(exit code 0)
$ for k in 1..15: cmp <scratch>/rerun1/n$k.json calibration/n$k.json && echo n$k identical; for k in 16..30: cmp ... object/n$k.json ...; cmp <scratch>/rerun1/values.txt values.txt && echo values identical
n1 identical
n2 identical
n3 identical
n4 identical
n5 identical
n6 identical
n7 identical
n8 identical
n9 identical
n10 identical
n11 identical
n12 identical
n13 identical
n14 identical
n15 identical
n16 identical
n17 identical
n18 identical
n19 identical
n20 identical
n21 identical
n22 identical
n23 identical
n24 identical
n25 identical
n26 identical
n27 identical
n28 identical
n29 identical
n30 identical
values identical
```

### Step 5 again: regeneration run 2, the determinism check

```
$ mkdir -p <scratch>/rerun2 && python3 -I solver/solver.py 30 <scratch>/rerun2 1 30 <scratch>/rerun2/values.txt --b-dir data
(exit code 0)
$ (same cmp loops against claim/)
n1 identical
n2 identical
n3 identical
n4 identical
n5 identical
n6 identical
n7 identical
n8 identical
n9 identical
n10 identical
n11 identical
n12 identical
n13 identical
n14 identical
n15 identical
n16 identical
n17 identical
n18 identical
n19 identical
n20 identical
n21 identical
n22 identical
n23 identical
n24 identical
n25 identical
n26 identical
n27 identical
n28 identical
n29 identical
n30 identical
values identical
$ diff -r <scratch>/rerun1 <scratch>/rerun2
rerun1 and rerun2 directories identical
```

The two solver logs differ only in the two timing lines: "exact solve time: 4.00 s" versus "3.56 s", and "certificate writing time: 1.95 s" versus "1.82 s". The sha256 of the regenerated object/n30.json is 0e7ff5b9e9982c35d8e326fdb0eb0365997c731a4fff11be0630b0ea842df37f, which equals the SHA256SUMS entry.

Every author command produced exactly the output REPRODUCE.md says to expect:
- 15 PASS lines and ALL_PASS for the objects;
- 15 "oeis_match=yes PASS" lines and ALL_PASS for the calibration set;
- "my_verify summary: 30 passed, 0 failed, of 30 certificates";
- "OEIS comparison n<=15: ALL MATCH" in the solver log;
- 31 "identical" lines, twice.

## 6. Error hunt

- **A certificate self-consistent under a sub-optimal policy: not present.** At every a >= 1 position of all 30 certificates, the value equals max(continue, stop) exactly and the claimed action attains it, with 0 ties. My checker rejects sub-optimal certificates built by exact policy evaluation (M10 in section 2.4).
- **Positions out of range or duplicated: none.** My checker enforces strict range, duplicate, set-equality and row-count checks, and my mutations M05, M06 and M07 are caught.
- **Wrong terminal rule (must-bank variants): no.** P = 1 at a + b >= n is the paper's rule (Section 4), and a must-bank variant is value-equivalent (section 3).
- **Sign error in the 1 - P terms: no.** The equations match the paper's Section 4 and follow from the rules. The certificates satisfy them, and every number the paper prints is reproduced: the n=1..6 terms, the Section 2 intermediate values, the n=4 strategy and all 361 Table 1 entries.
- **Non-reduced fractions: none.** gcd(num, den) = 1 for every value in all 30 files. My checker checks this, and so does solver/my_verify.py.
- **A P000 field that differs from the table: no.** It is the identical string in all 30 files.
- **A solver that uses floats to decide actions: no.** solver/solver.py imports only json, os, sys, time and fractions.Fraction. Every action is decided by an exact Fraction comparison: `if cv > sv` / `elif cv < sv` / else tie, recorded as toss. The component root is an exact Newton step, which is the 2x2 solve for the current policy pair, with exact bisection as a fallback; the log shows 0 bisection steps and 0 exact ties. A grep finds float-like tokens only in docstrings. In any case, actions do not need trusting: they are re-verified exactly.
- **Weakness of checker/ros_cert_check.py, which does not affect the result.** It is lenient:
  - it does not check that fractions are reduced;
  - it coerces coordinates with int(), so 1.5 would be read as 1 and True as 1;
  - it accepts "continue" and whitespace;
  - a missing P000 field is not an error;
  - duplicate JSON keys go undetected.

  These gaps are covered here by my strict checker and by solver/my_verify.py, which checks reducedness and int types, and all 30 certificates pass both.
- **Minor provenance note.** claim.md's status record mentions a saved OEIS page "data/oeis_A387261.html", and that file is not in claim/. It is not among the files claim.md says the package contains, and nothing in the reproduction needs it. The b-file sha256 and byte count in the same record (9685600d...5e66, 335 bytes) match data/b387261.txt and SHA256SUMS.

## 7. Verdict

Every item of the REPRODUCE brief is confirmed:
- My checker, written from the quoted definition before I read the author's code, verifies every position of all 30 certificates in exact arithmetic. That covers completeness, reducedness, the forced toss, the Bellman max and action attainment, with 0 ties.
- P(0,0,0) of object/n16..n30 equals values.txt and claim.md exactly.
- P(0,0,0) of calibration/n1..n15 equals the OEIS b-files exactly.
- My independent exact solver reproduces all 30 tables entry for entry.
- The definition, the terminal rule and the forced toss are the paper's.
- Every step of the proof note holds, with one loose phrase whose conclusion is unaffected.
- The author's commands give the documented output.
- The regeneration is byte-identical to the package on two separate runs.
- All 38 hashes verify.

I found no mismatch, no missing claimed object and no non-determinism.

context: subagent
pass: true
