# FJSSP-W: 91 instances below their listed UB

## What
For the 91 distinct instance files listed in INDEX.csv (from instances/Example_Instances_FJSSP-WF, sha256-identical to repo commit eb1d283), the supplied schedules pass an independently recomputed check of eligibility, pair durations, job precedence and machine/worker no-overlap, with makespans 1 to 171 below the integer UB of the data.csv-confirmed row of best_known.csv as re-fetched live at 2026-10-31T12:37Z (UB > LB in every case), which meets p2's threshold of at least 10 instances. The panel checked 95 candidates; four were dropped on novelty grounds (see Not claimed), leaving these 91.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. It downloads 91 instance file(s) from the organisers' repository; a few seconds per file.

## Compared to
best_known.csv of jrc-rodec/FJSSP-W-Benchmarking, fetched 2026-10-31T10:24:20Z (the-record-we-beat/snapshot.md).

| instance | row | ours | listed UB |
|---|---|---|---|
| Behnke1 | behnkegeiger1 | 83 | 85 |
| Behnke2 | behnkegeiger2 | 85 | 86 |
| Behnke4 | behnkegeiger4 | 88 | 90 |
| Behnke5 | behnkegeiger5 | 84 | 85 |
| BrandimarteMk4 | brandimarte4 | 55 | 56 |
| ChambersBarnes1 | chambersbarnes1 | 863 | 880 |
| ChambersBarnes10 | chambersbarnes10 | 855 | 893 |
| ChambersBarnes11 | chambersbarnes11 | 846 | 871 |
| ChambersBarnes12 | chambersbarnes12 | 853 | 859 |
| ChambersBarnes13 | chambersbarnes13 | 864 | 890 |
| ChambersBarnes14 | chambersbarnes14 | 848 | 874 |
| ChambersBarnes2 | chambersbarnes2 | 852 | 860 |
| ChambersBarnes3 | chambersbarnes3 | 857 | 863 |
| ChambersBarnes5 | chambersbarnes5 | 789 | 805 |
| ChambersBarnes6 | chambersbarnes6 | 863 | 888 |
| ChambersBarnes7 | chambersbarnes7 | 840 | 846 |
| ChambersBarnes8 | chambersbarnes8 | 875 | 896 |
| ChambersBarnes9 | chambersbarnes9 | 860 | 892 |
| Fattahi19 | fattahi19 | 994 | 1024 |
| Hurinkedata10 | hurinkedata10 | 738 | 741 |
| Hurinkedata11 | hurinkedata11 | 813 | 817 |
| Hurinkedata12 | hurinkedata12 | 851 | 855 |
| Hurinkedata17 | hurinkedata17 | 1071 | 1077 |
| Hurinkedata2 | hurinkedata2 | 812 | 825 |
| Hurinkedata25 | hurinkedata25 | 819 | 850 |
| Hurinkedata26 | hurinkedata26 | 937 | 942 |
| Hurinkedata44 | hurinkedata44 | 1086 | 1117 |
| Hurinkedata45 | hurinkedata45 | 862 | 884 |
| Hurinkedata49 | hurinkedata49 | 5956 | 6007 |
| Hurinkedata50 | hurinkedata50 | 6067 | 6223 |
| Hurinkedata51 | hurinkedata51 | 6494 | 6524 |
| Hurinkedata57 | hurinkedata57 | 916 | 924 |
| Hurinkedata58 | hurinkedata58 | 810 | 826 |
| Hurinkedata59 | hurinkedata59 | 889 | 910 |
| Hurinkedata60 | hurinkedata60 | 917 | 948 |
| Hurinkedata61 | hurinkedata61 | 794 | 812 |
| Hurinkedata62 | hurinkedata62 | 897 | 916 |
| Hurinkedata63 | hurinkedata63 | 364 | 366 |
| Hurinkedata64 | hurinkedata64 | 825 | 832 |
| Hurinkedata65 | hurinkedata65 | 875 | 885 |
| Hurinkedata66 | hurinkedata66 | 864 | 893 |
| Hurinkrdata2 | hurinkrdata2 | 640 | 651 |
| Hurinkrdata20 | hurinkrdata20 | 592 | 593 |
| Hurinkrdata21 | hurinkrdata21 | 618 | 624 |
| Hurinkrdata22 | hurinkrdata22 | 649 | 663 |
| Hurinkrdata23 | hurinkrdata23 | 706 | 709 |
| Hurinkrdata49 | hurinkrdata49 | 4840 | 4857 |
| Hurinkrdata51 | hurinkrdata51 | 5408 | 5426 |
| Hurinkrdata53 | hurinkrdata53 | 5410 | 5581 |
| Hurinkrdata54 | hurinkrdata54 | 5859 | 5895 |
| Hurinkrdata56 | hurinkrdata56 | 5350 | 5423 |
| Hurinkrdata57 | hurinkrdata57 | 704 | 722 |
| Hurinkrdata59 | hurinkrdata59 | 664 | 671 |
| Hurinkrdata60 | hurinkrdata60 | 692 | 702 |
| Hurinkrdata62 | hurinkrdata62 | 704 | 710 |
| Hurinkrdata63 | hurinkrdata63 | 281 | 289 |
| Hurinkrdata64 | hurinkrdata64 | 590 | 595 |
| Hurinkrdata65 | hurinkrdata65 | 657 | 660 |
| Hurinkrdata66 | hurinkrdata66 | 701 | 712 |
| Hurinkrdata8 | hurinkrdata8 | 438 | 444 |
| Hurinksdata19 | hurinksdata19 | 883 | 907 |
| Hurinksdata2 | hurinksdata2 | 870 | 894 |
| Hurinksdata22 | hurinksdata22 | 793 | 800 |
| Hurinksdata23 | hurinksdata23 | 842 | 847 |
| Hurinksdata24 | hurinksdata24 | 1000 | 1031 |
| Hurinksdata25 | hurinksdata25 | 861 | 869 |
| Hurinksdata27 | hurinksdata27 | 904 | 924 |
| Hurinksdata28 | hurinksdata28 | 908 | 909 |
| Hurinksdata44 | hurinksdata44 | 1132 | 1135 |
| Hurinksdata45 | hurinksdata45 | 874 | 886 |
| Hurinksdata51 | hurinksdata51 | 7043 | 7141 |
| Hurinksdata53 | hurinksdata53 | 7337 | 7376 |
| Hurinksdata55 | hurinksdata55 | 6174 | 6244 |
| Hurinksdata56 | hurinksdata56 | 7895 | 7916 |
| Hurinksdata57 | hurinksdata57 | 1000 | 1033 |
| Hurinksdata58 | hurinksdata58 | 822 | 837 |
| Hurinksdata59 | hurinksdata59 | 954 | 976 |
| Hurinksdata6 | hurinksdata6 | 573 | 574 |
| Hurinksdata60 | hurinksdata60 | 935 | 960 |
| Hurinksdata62 | hurinksdata62 | 939 | 951 |
| Hurinksdata64 | hurinksdata64 | 842 | 855 |
| Hurinksdata65 | hurinksdata65 | 874 | 882 |
| Hurinksdata66 | hurinksdata66 | 874 | 877 |
| Hurinkvdata4 | hurinkvdata4 | 546 | 549 |
| Hurinkvdata50 | hurinkvdata50 | 5608 | 5612 |
| Hurinkvdata51 | hurinkvdata51 | 5406 | 5474 |
| Hurinkvdata56 | hurinkvdata56 | 4223 | 4264 |
| Hurinkvdata58 | hurinkvdata58 | 560 | 565 |
| Hurinkvdata6 | hurinkvdata6 | 456 | 458 |
| Hurinkvdata7 | hurinkvdata7 | 480 | 486 |
| Hurinkvdata8 | hurinkvdata8 | 437 | 439 |


## Not claimed
No claim of optimality beyond what CP-SAT reported in its own run. Nothing about the classic FJSP instances these were derived from.
Not included (tied, or a lower value reported elsewhere; see panel/novelty.md):
- Hurinksdata61 (826) and Hurinksdata63 (373): tied by valid schedules from Yu Sun in FJSSP-W-Competition issue #11 (https://github.com/jrc-rodec/FJSSP-W-Competition/issues/11).
- Hurinkedata6 (537) and Hurinkrdata50 (5684): lower values (533 and 5681) reported by the HUST Operations Research and Optimization team in issue #14 (https://github.com/jrc-rodec/FJSSP-W-Competition/issues/14). Those schedules failed our worker no-overlap check, but we exclude both instances to be safe.

Closest competition value to a claimed instance: ChambersBarnes10, where the best valid competition value is 856 (Yu Sun, issue #11, https://github.com/jrc-rodec/FJSSP-W-Competition/issues/11); ours is 855.

## Credits
- Benchmark, instances and best_known.csv: David Hutter, Thomas Steinberger, Michael Hellwig (and Bianca Kasper),
  Josef Ressel Centre for Robust Decision Making, https://github.com/jrc-rodec/FJSSP-W-Benchmarking, arXiv:2501.16159.
- The original FJSP instance sets: Behnke and Geiger, Brandimarte, Chambers and Barnes, Dauzere-Peres and Paulli,
  Fattahi et al., Hurink et al., Kacem et al.
- Solver: Google OR-Tools CP-SAT, https://github.com/google/or-tools
- Model ideas (hierarchical alternatives, redundant cumulative): ScheduleOpt optalcp-benchmarks, flexible-jobshop-w.
- Credit for this result: Abdelghafour.
