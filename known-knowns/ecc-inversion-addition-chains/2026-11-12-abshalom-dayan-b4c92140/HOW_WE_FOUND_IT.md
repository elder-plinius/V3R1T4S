# How we found it

_Contributor text, unverified._

The target asks for addition chains for the exponent n - 2 that inverts a scalar modulo the secp256k1 group order, shorter than every published one. A chain is a list of numbers starting at 1 in which each number is the sum of two earlier ones; its length is the number of group operations a fixed, constant-time inversion performs.

**First attempt, withdrawn.** On 2026-11-10 a first search (a small dictionary of values below 2^12, an exact dynamic program for the main line) gave 284 for this exponent, below the 288 and 290 we knew of. Before filing, a second novelty search found Neill Clift's page with Brian Smith's 2026 chains: 282 for secp256k1. The 284 was not a record and was not filed.

**Reading the published chain.** Smith's 282 chain has the same overall shape as ours (a dictionary that is itself an addition chain, a ladder for the top run of 127 ones, a main line of doublings and additions of dictionary values) but its dictionary values go up to 21 bits and its additions overlap: the running value stays below the target prefix for several steps and later additions catch up. Our first program could not represent that (values capped at 12 bits, at most two overlapping additions).

**A new evaluator.** We wrote acw.c: the main line is solved bottom-up from the exponent over states (bit position, deficit) kept in a hash table, so the size of the dictionary values no longer matters, with a ranked beam to keep it fast. On Smith's dictionaries for Curve25519, P-256 and P-384 it returns his published lengths exactly; for secp256k1 it needs a wide beam to see 282 (the narrow beam used during search reads it as 284).

**The search.** Simulated annealing over the dictionary (insert a sum of two values, insert a window of the exponent, delete, replace), two lineages kept apart: one from scratch and from our own earlier dictionaries, one started from Smith's dictionaries. For secp256k1 the seeded lineage reached 281 after about 560,000 moves (about 40 minutes of one core). The unseeded lineage reached 283. The exact builder then wrote the chain, and two independent checkers confirmed it.

**What the result is.** One addition fewer than the published chain, with the same number of doublings. Nine dictionary values differ from the seed (three dropped, six added); the top ladder is unchanged. No single edit of the seed dictionary gives 281 (how-we-built-it/baseline/one_edit.txt), so it is not a trivial edit, but it is a local improvement of Smith's chain and is presented as that.

**What did not work.** The same program gave ties, not gains, on the other three scalar cells (Curve25519 275, P-256 281 and P-384 419 only from Smith's dictionaries). Restarts from the 281 dictionary did not reach 280.
