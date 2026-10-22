context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

# reproduce: cubic-dimer-he-table2 (p1, reproduction of He's Table 2)

Scope: whether the 12 entries of He's Table 2 (the values are listed in the-record-we-beat/README.md; the excerpt itself is not shipped) are reproduced by an independent exact computation. Novelty and criterion belong to the other skeptics. No network.

## 0. Integrity
The contributor's hash list verified from the package folder: all OK. I worked on a private copy of the package; my code is not shipped in this package.

## 1. Claim and definition
Claim: "all 12 entries, (2,2) to (6,3) at p = 4 and (5,5) at p = 2, rounded up to six decimals, using exact integer arithmetic with cross-multiplied ratios." p1 text: "Independent reimplementation that reproduces He's 0.452130 at (m, n) = (5, 5) and every smaller entry of his Table 2 to six decimals (rounded upward) with exact arithmetic."
Definition used (quoted from object/DERIVATION.md): A[u,v] = 1 iff v-u in {(0,0),(1,0),(0,1)} on Z/m x Z/n; T[U,V] = per A[U, V\V'] if |U|+|V'| = mn. For each sector i = 0..floor(mn/2), X_i Y_i acts on orbits of i-subsets under G = V x| K (K = automorphisms phi of Z/m x Z/n with phi(D) a translate of D). Iterate x_{q+1} = X_i Y_i x_q from the all-ones vector; C_p = max_u (A^{p+1}1)_u/(A^p 1)_u; the entry is (1/(2mn)) log of the maximum over sectors of C_p, rounded up. (He's Section 4: p = 4 except (5,5) with p = 2. The semantics of p are inferred; see section 3.)

## 2. My own checker (written before opening verify-it-yourself/)
My own C program (not shipped in this package): an independent program (layer, group K from the images of the two generators, orbit representatives, X and Y by depth-first search over injective forward maps, 256-bit unsigned integers, 12 threads) for any (m,n); its driver script (also not shipped) compares ratios by Python integer cross-multiplication, takes the maximum over ALL sectors 0..floor(mn/2) at the stated p, and takes the logarithm and ceiling with mpmath at 60 digits. Property C spot test (300 random orbit members per run): 0 failures in every run. Runs: the driver with arguments M N 4 4 for each of the eleven small entries (the (5,4) one too) and with arguments 5 5 2 12 for (5,5). Their outputs are not shipped.

## 3. Results (my exact values; He's entries from the saved excerpt)
Entry | my bound | rounded up to 6 places | He | sector of the maximum
- (2,2) p=4 | 0.486477537264 | 0.486478 | 0.486478 | 2
- (3,2) p=4 | 0.471407877736 | 0.471408 | 0.471408 | 3
- (3,3) p=4 | 0.458557216116 | 0.458558 | 0.458558 | 4
- (4,2) p=4 | 0.465969915824 | 0.465970 | 0.465970 | 4
- (4,3) p=4 | 0.457379268024 | 0.457380 | 0.457380 | 6
- (4,4) p=4 | 0.454672566947 | 0.454673 | 0.454673 | 8
- (5,2) p=4 | 0.463400092486 | 0.463401 | 0.463401 | 5
- (5,3) p=4 | 0.454662776205 | 0.454663 | 0.454663 | 7
- (5,4) p=4 | 0.453364136825 | 0.453365 | 0.453365 | 10
- (6,2) p=4 | 0.462009756329 | 0.462010 | 0.462010 | 6
- (6,3) p=4 | 0.454617427868 | 0.454618 | 0.454618 | 9
- (5,5) p=2 | 0.452129162602 | 0.452130 | 0.452130 | 12

All 12 entries agree with He's Table 2 to six decimals (rounded up). The (5,5) entry was computed over all 13 sectors (sector bounds 0.178779, 0.236587, 0.280676, 0.316595, 0.346543, 0.371698, 0.392779, 0.410265, 0.424480, 0.435650, 0.443930, 0.449398, 0.452129); sector 12 ratio 465736652230808449294072966961/70840300670346690445.
The meaning of p (iterate A = X Y from the all-ones vector, A^{p+1}1 over A^p 1) is not spelled out in the saved excerpt beyond "p = 4 ... (5,5) p = 2"; the fact that this reading reproduces all 12 published six-decimal figures, including the one entry that uses p = 2 (which differs from the converged value 0.4520095976), supports it.

## 4. Author's script
sh verify-it-yourself/run_checks.sh with CW_QUICK=1 (skips (5,4) in Python; I did (5,4) myself above), CW_PROCS=12, CWSEC_THREADS=12. Its output is not shipped separately; it ends "PASS (5,5) p=2: 13 sectors, maximum 0.4521291626 in sector 12, rounded up 0.45213, He 0.452130" and "ALL CHECKS PASS". Its 10-digit values equal mine where it ran them ((6,3) 0.4546174279, (3,3) 0.4585572161, (4,4) 0.4546725669, (5,3) 0.4546627762).

## 5. Mismatches inside the object file
object/RESULTS.md (section 1 table) prints two ten-digit figures that are wrong: (5,4) is printed 0.4533648604 but the exact value is 0.4533641368 (object/he_55_64_out.txt shows the right 0.4533641368); (6,3) is printed 0.4546179726 but the exact value is 0.4546174279. Both round up to the correct six-place value (0.453365, 0.454618), so the claim as worded (six decimals, rounded up) is not affected. Several orbit counts in that table also disagree with my rebuilt counts: mine are (3,3) sector 4: 5; (4,3) sector 6: 80; (4,4) sector 8: 157; (5,2) sector 5: 26; (5,3) sector 7: 429; (5,4) sector 10: 9252; (6,3) sector 9: 1404; (5,5) sector 12: 35070; RESULTS.md prints 6, 86, 166, 28, 435, 9,296, 1,401, 35,070. My 9252 and 1404 agree with the run log and the author's checker, so the table counts are wrong; no bound depends on them. RESULTS.md also states a (6,4) entry that He did not compute; I did not check the (6,4) entry.
Open question 1 (which file is the claimed object): the claim sentence concerns only the six-decimal rounded-up entries, which I reproduce. I do not count the two wrong ten-digit figures against it, but they must not be quoted as exact.

## 6. Other open questions
Q2: the (5,5) entry is reproduced here with exact 256-bit integers, and by the author's 128-bit C with overflow detection, both giving 0.4521291626. Q4: the other nine cases are reproduced from scratch here, independent of the log.

Mismatch count against He's six-decimal entries: 0. Non-determinism: none seen.
pass: true
