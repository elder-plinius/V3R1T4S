"""Colour-3 join of a (3,3,m) circulant colouring of K_n with a 2-colouring of K5 that has no monochromatic triangle
(pentagon in colour 1, pentagram in colour 2): every edge between the K5 block and the old vertices gets colour 3.
Colour 1 and 2 triangles cannot use a block-old edge, the block has none of its own, and a colour-3 clique holds at
most one block vertex, so omega_3 grows by exactly 1: a (3,3,m+1)-colouring of K_{n+5}.
usage: join_k5.py <circulant (3,3,m) file> <out matrix file>
Output: a matrix file, one row per vertex, entry j = colour of edge ij (0 on the diagonal); vertices 0..n-1 are the
circulant, n..n+4 the block."""
import sys
lines = [l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
h = lines[0].split(); assert h[0] == 'circulant' and h[2] == '3'
n = int(h[1]); col = {}
for l in lines[1:4]:
    c, ds = l.split(':', 1)
    for d in map(int, ds.split()):
        col[d % n] = int(c); col[(-d) % n] = int(c)
assert all(d in col for d in range(1, n))
N = n + 5
M = [[0] * N for _ in range(N)]
for i in range(n):
    for j in range(n):
        if i != j:
            M[i][j] = col[(j - i) % n]
for b in range(5):
    for i in range(n):
        M[n + b][i] = M[i][n + b] = 3
    for b2 in range(5):
        if b != b2:
            M[n + b][n + b2] = 1 if (b - b2) % 5 in (1, 4) else 2
with open(sys.argv[2], 'w') as f:
    f.write('# colour-3 join of %s (vertices 0..%d) with a triangle-free 2-colouring of K5 (vertices %d..%d)\n'
            % (sys.argv[1].rsplit('/', 1)[-1], n - 1, n, N - 1))
    f.write('matrix %d 3\n' % N)
    for r in M:
        f.write(''.join(map(str, r)) + '\n')
print('wrote', sys.argv[2], 'N', N)
