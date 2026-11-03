# How we found it (contributor text, unverified)
We started from the organisers' published best solution for i18 and ran a simulated annealer (how-we-built-it/anneal.cc)
that keeps every hard constraint satisfied while it moves nurses between rooms, moves patients between rooms, theatres
and admission days, and schedules or drops optional patients. Run 1 used 150 s and seed 1, run 2 continued for 300 s with
seed 2. Most of the gain came from nurse-to-room assignments (skill mismatch and workload). On 46 of the 60 instances
the same search found nothing in 150 s, and on 5 more cells other contributors' open pull requests were already lower.
