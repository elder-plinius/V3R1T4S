#!/bin/sh
# Negative tests for lantx (PREREG N1, N2).
X=./code/lantx2
echo "N1: 4x4 mask 0 has tcap 9977 (enum4). cap 9976 must NOT capture, cap 9977 must capture:"
$X range 4 4 0 1 9976
$X range 4 4 0 1 9977
echo "N2: empty-grid run (6x6 mask 0); planted black cell at the ant's position at step 20000 of the unplanted run"
P=$(python3 -c "
g=set();x=y=h=0
for t in range(20000):
    b=(x,y) in g; h=(h+1+2*b)&3
    g.symmetric_difference_update({(x,y)}); x+=(0,1,0,-1)[h]; y+=(1,0,-1,0)[h]
print(x,y)")
echo "plant at $P"
echo "unplanted:"; $X range 6 6 0 1
echo "planted (must not certify before step 20000; tcap expected > 20000 since the highway is disrupted):"
$X plant 6 6 0 $P
echo "N3: planted black cell at the unplanted ant's position at step 100000 (far down the highway): certification must happen after step 100000"
P=$(python3 -c "
g=set();x=y=h=0
for t in range(100000):
    b=(x,y) in g; h=(h+1+2*b)&3
    g.symmetric_difference_update({(x,y)}); x+=(0,1,0,-1)[h]; y+=(1,0,-1,0)[h]
print(x,y)")
echo "plant at $P"; $X plant 6 6 0 $P
