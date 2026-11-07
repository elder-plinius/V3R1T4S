# Commands (Windows 11, single thread)

Requirements: .NET Framework 4.x C# compiler (csc.exe, shipped with Windows); Python 3.14 with numpy 2.4.2 and
scipy 1.17.0 (HiGHS through scipy.optimize.milp). HiGHS only proposes candidates; the object is checked exactly.

    csc -optimize+ -platform:x64 -out:EnumDom.exe EnumDom.cs
    csc -optimize+ -platform:x64 -out:EnumDomSub.exe EnumDomSub.cs
    EnumDom.exe 11 dom 5 dominating-5-sets-Q11.txt              # 2 sets (Lauri's count)
    EnumDom.exe 11 dom 6 minimal-dominating-6-sets-Q11.txt 1    # 432 minimal sets, about 20 s
    python drive19.py dominating-5-sets-Q11.txt minimal-dominating-6-sets-Q11.txt EnumDomSub.exe WORKDIR 500 1000

drive19.py picks pairwise disjoint 5/6-sets with 2*t5 + t6 >= 12 (no-good cuts between iterations), enumerates all
minimal dominating 7- and 8-sets inside the remaining squares with EnumDomSub.exe, packs them, and writes
FOUND-dom-Q11-19.txt in WORKDIR when 19 disjoint dominating sets are found (iteration 3 in our run). Leftover squares
join class 0, which keeps every class dominating.
Calibration of EnumDom: Q_9 -> 114 dominating 5-sets, Q_10 -> 8, Q_11 -> 2 (the counts published by Lauri).
