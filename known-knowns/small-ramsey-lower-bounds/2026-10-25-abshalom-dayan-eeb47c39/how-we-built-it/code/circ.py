"""Helpers: load circulant colouring files (mcheck.py format), write adjacency files for alpha.c.
A clique K_k in colour c is an independent k-set in the complement of colour c, so for alpha.c we write the
complement of colour c (all edges not of colour c)."""
import sys, os


def load_circ(path):
    lines = [l.strip() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    head = lines[0].split()
    assert head[0] == 'circulant'
    N, r = int(head[1]), int(head[2])
    col = {}
    for l in lines[1:1 + r]:
        c, ds = l.split(':', 1)
        c = int(c)
        for d in map(int, ds.split()):
            d %= N
            for e in (d, N - d):
                assert col.get(e, c) == c
                col[e] = c
    assert all(d in col for d in range(1, N))
    return N, r, col


def classes(N):
    return list(range(1, N // 2 + 1))


def write_adj_complement_of(N, col, c, out):
    """adjacency matrix of the graph whose edges are those NOT of colour c (circulant)."""
    with open(out, 'w') as f:
        for i in range(N):
            f.write(''.join('0' if i == j else ('0' if col[(j - i) % N] == c else '1') for j in range(N)) + '\n')


def write_adj_matrix_complement(M, c, out):
    N = len(M)
    with open(out, 'w') as f:
        for i in range(N):
            f.write(''.join('0' if i == j else ('0' if M[i][j] == c else '1') for j in range(N)) + '\n')


if __name__ == '__main__':
    # usage: circ.py <circ file> <colour> <out.adj>
    N, r, col = load_circ(sys.argv[1])
    write_adj_complement_of(N, col, int(sys.argv[2]), sys.argv[3])
    print(N, r, 'colour', sys.argv[2], 'degree', sum(1 for d in range(1, N) if col[d] == int(sys.argv[2])))
