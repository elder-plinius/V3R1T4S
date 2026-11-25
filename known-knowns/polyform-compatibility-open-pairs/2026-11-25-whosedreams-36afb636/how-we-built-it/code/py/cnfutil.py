"""Minimal DIMACS CNF builder with sequential-counter cardinality."""
from __future__ import annotations


class CNF:
    def __init__(self):
        self.clauses: list[list[int]] = []
        self.nvars = 0

    def new_var(self) -> int:
        self.nvars += 1
        return self.nvars

    def add(self, *lits: int) -> None:
        self.clauses.append(list(lits))

    def add_clause(self, lits) -> None:
        self.clauses.append(list(lits))

    def exactly_one(self, lits: list[int]) -> None:
        if not lits:
            self.add()  # unsat
            return
        self.add(*lits)  # at least one
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                self.add(-lits[i], -lits[j])

    def exactly_k(self, lits: list[int], k: int) -> None:
        """Sequential counter: sum(lits) == k."""
        n = len(lits)
        if k < 0 or k > n:
            self.add()
            return
        if k == 0:
            for x in lits:
                self.add(-x)
            return
        if k == n:
            for x in lits:
                self.add(x)
            return
        if k == 1:
            self.exactly_one(lits)
            return
        # s[i][j] <=> first i lits sum to >= j+1 (j=0..k-1), i=0..n-1
        # Use standard Sinz sequential counter for at-most-k and at-least-k.
        self._at_most_k(lits, k)
        self._at_least_k(lits, k)

    def _at_most_k(self, lits: list[int], k: int) -> None:
        n = len(lits)
        if k >= n:
            return
        if k == 0:
            for x in lits:
                self.add(-x)
            return
        s = [[self.new_var() for _ in range(k)] for _ in range(n)]
        self.add(-lits[0], s[0][0])
        for j in range(1, k):
            self.add(-s[0][j])
        for i in range(1, n):
            self.add(-lits[i], s[i][0])
            self.add(-s[i - 1][0], s[i][0])
            for j in range(1, k):
                self.add(-lits[i], -s[i - 1][j - 1], s[i][j])
                self.add(-s[i - 1][j], s[i][j])
            self.add(-lits[i], -s[i - 1][k - 1])

    def _at_least_k(self, lits: list[int], k: int) -> None:
        # sum(lits) >= k  <=>  sum(~lits) <= n-k
        n = len(lits)
        self._at_most_k([-x for x in lits], n - k)

    def write(self, path) -> None:
        with open(path, "w") as f:
            f.write(f"p cnf {self.nvars} {len(self.clauses)}\n")
            for cl in self.clauses:
                f.write(" ".join(str(x) for x in cl) + " 0\n")
