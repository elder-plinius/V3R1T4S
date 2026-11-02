# Build commands (as run; gcc 14.2, Linux, one core per job)

    gcc -O2 -march=native -o beam3 beam3.c
    BEAM_V=2 ./beam3 12 200000 3 45 > logs/T12_B200000_W3_V2.txt 2> logs/T12_B200000_W3_V2.log     # SOLVED moves=25 (the object)
    ./beam3 12 100000 2 45 > logs/T12_B100000_W2_V0.txt 2> logs/T12_B100000_W2_V0.log              # NOT SOLVED within 45 moves
    BEAM_V=2 BEAM_SEED=21 ./beam3 12 200000 3 45 > logs/T12_B200000_W3_V2_s21.txt 2> logs/T12_B200000_W3_V2_s21.log   # 25
    BEAM_V=2 BEAM_SEED=22 ./beam3 12 200000 3 45 > logs/T12_B200000_W3_V2_s22.txt 2> logs/T12_B200000_W3_V2_s22.log   # 25

usage: beam n B W [maxmoves] [start_hole_index|-1]. Rank key = W*filled_Merson_regions + pegs (+ BEAM_V * isolated
pegs), lower is better; BEAM_SEED adds a small hashed tie-break. The last line of the .txt file is the solution;
object/T12_25moves.txt is that line from logs/T12_B200000_W3_V2.txt. No requirements beyond a C compiler with
unsigned __int128. PREREG.md is the run's preregistration, copied as frozen (2026-11-02T17:34:07Z).
