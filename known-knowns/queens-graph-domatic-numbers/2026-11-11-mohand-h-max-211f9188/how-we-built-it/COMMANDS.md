# Commands (Windows 11, single thread)

Requirements: the .NET Framework 4.x C# compiler (csc.exe, shipped with Windows). No solver is needed.

    csc -optimize+ -platform:x64 EnumCovK.cs
    csc -optimize+ -platform:x64 Q10Fin.cs
    EnumCovK.exe 10 6 total-dominating-6-sets-Q10.txt 0 tdom   # 216 sets, under a second
    EnumCovK.exe 10 7 seven.txt 0 tdom                         # 259820 minimal 7-sets, a few seconds
    Q10Fin.exe total-dominating-6-sets-Q10.txt seven.txt 600 grid.txt

Q10Fin.exe enumerates families of 14 pairwise disjoint total dominating 6-sets (in increasing index order) and, for
each, tests all splits of the 16 remaining squares into two total dominating sets. In our run the sixth family gave
the object after about 46 s (grid.txt, byte-identical to object/tdom-Q10-16-partition.txt). The list of 7-sets is read
by the program but is only used for families of 13 or 12 six-sets, which were not reached; it is not included here
(259,820 lines) and can be rebuilt with the command above.
Calibration of EnumCovK with the option tdom: no total dominating set of size 4 on Q_9, 5 on Q_10, 6 on Q_11 and Q_12,
and some at the next size (Lauri's total domination numbers 5, 6, 7, 7).
PREREG.v2.md records one correction made after the result existed: a checker named in PREREG.md does not test total
domination and was dropped.
