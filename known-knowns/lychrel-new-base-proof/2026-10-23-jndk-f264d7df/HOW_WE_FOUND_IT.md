# How we found it (contributor text, unverified)

Brief: find a base outside 2^k, 11, 17, 20, 26 where a reverse-and-add orbit provably never reaches a palindrome.

What failed: running orbits from small seeds (below one million, 4000 steps) in about twenty bases: no orbit ever
settled into a repeating shape, unlike base 2 and 4. Seal-type cycles are not reached from small seeds even in base 11.

What worked: reading the template from the outside in. Digit j from the left always pairs with digit j from the right,
so the outer digits of any template cycle of period p form a path in a finite state graph (carries, plus the shift
caused by a new leading digit). A template needs a self-loop in that graph. An exhaustive search over periods up to 7
(10 for some bases) showed that most bases have no such loop at all (base 10 included, up to period 10), while a few do.
Allowing the repeated block to be equal digits on both sides (not only 0 against b-1) opened base 13 at period 10:
the block alternates 4 -> 8 -> 4, doubling modulo 12. We then put the printed outer digits around a 24-digit block of 4s
and tried short middles; the empty middle already locked into a period-10 cycle, which an exact symbolic checker proved
for every block length. Three independent fresh-context reviewers then rechecked it.
