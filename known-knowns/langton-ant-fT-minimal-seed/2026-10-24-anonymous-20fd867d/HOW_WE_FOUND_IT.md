# How we found it (contributor text, unverified)
A literature check showed only isolated points (9977, Ke's 182-step 4-cell seed, Jillhewar's 11-cell instant seed).
We searched over the ant's first reads with an exact "on the highway at time t" test against the 104 blank-highway
phases (fsearch), deepening T until a seed appeared, then re-proved every value with a second search written from
scratch (lcone, no bounding box, turn-word test) and a separate brute force for k = 1, 2. Two separate simulators
reproduce every minimiser. Three fresh reviewers (criterion, novelty, reproduce) each passed it.
