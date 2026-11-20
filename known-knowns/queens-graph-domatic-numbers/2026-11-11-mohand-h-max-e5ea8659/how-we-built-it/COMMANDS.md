# Commands (Windows 11, single thread)

Requirements: the .NET Framework 4.x C# compiler (csc.exe, shipped with Windows). No solver is needed.

    csc -optimize+ -platform:x64 EnumCov.cs
    csc -optimize+ -platform:x64 Skel.cs
    EnumCov.exe 12 6 dominating-6-sets-Q12.txt 0        # 8 sets (Lauri's count), under a second
    EnumCov.exe 12 7 seven-raw.txt 0                    # 6712 minimal sets, about 10 s
    sort -n seven-raw.txt > minimal-dominating-7-sets-Q12.txt
    Skel.exe dominating-6-sets-Q12.txt minimal-dominating-7-sets-Q12.txt 3 18 any 300 grid.txt

Skel.exe looks for 3 pairwise disjoint dominating 6-sets and 18 pairwise disjoint minimal dominating 7-sets that
together cover the 144 squares exactly. It tries one family of 6-sets per symmetry class of the board and searches
depth-first, always branching on the free square that lies in the fewest available 7-sets. In our run the third family
gave the object after about 70 s (grid.txt, byte-identical to object/dom-Q12-21-partition.txt).
Calibration of EnumCov: Q_9 -> 114 dominating 5-sets, Q_11 -> 2 dominating 5-sets and 432 minimal dominating 6-sets,
Q_12 -> 8 dominating 6-sets (Lauri's published counts, and our earlier enumerators for the 432).
