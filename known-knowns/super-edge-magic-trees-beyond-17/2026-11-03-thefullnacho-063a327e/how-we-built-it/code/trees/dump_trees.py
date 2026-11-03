import sys, networkx as nx
n = int(sys.argv[1])
for T in nx.nonisomorphic_trees(n):
    print("%d;%s" % (n, ",".join("%d-%d" % tuple(sorted(e)) for e in sorted(T.edges()))))
