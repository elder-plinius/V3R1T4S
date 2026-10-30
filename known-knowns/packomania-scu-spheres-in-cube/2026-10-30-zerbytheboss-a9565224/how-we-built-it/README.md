# How We Built It: Packomania SCU N=344 Record

We initialized from an exact sphere deletion candidate of the $N=345$ configuration in Eckard Specht's Packomania repository (`scu345.txt`).
Using Active-Set Sequential Quadratic Programming (SQP) contact network optimization on the unit cube tangent bundle, we formulated linear programming steps to relax tight contact constraints and iteratively inflate the packing radius.
The resulting coordinates were refined and certified under 50-digit arbitrary precision arithmetic (`mpmath`), yielding a certified feasible radius strictly beating the published table value by more than $1.18 \times 10^{-11}$.
