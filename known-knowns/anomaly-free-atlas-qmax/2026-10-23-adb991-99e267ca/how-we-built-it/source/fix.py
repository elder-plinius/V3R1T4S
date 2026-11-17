# Fix(Q, nu): self-conjugate solutions (every species triple is {-a,0,a}, a in 0..Q), zero included.
# Linear and cubic ACCs hold automatically; the quadratic one is aQ^2 - 2au^2 + ad^2 - aL^2 + ae^2 = 0;
# nu (if present) is unconstrained, giving a factor Q+1. Counted by matching aQ^2+ad^2+ae^2 = 2au^2+aL^2.
import sys
from collections import Counter
def fix(Q, nu):
    left = Counter(a*a + b*b + c*c for a in range(Q+1) for b in range(Q+1) for c in range(Q+1))
    right = Counter(2*a*a + b*b for a in range(Q+1) for b in range(Q+1))
    n = sum(v * left[k] for k, v in right.items())
    return n * (Q+1 if nu else 1)
if __name__ == "__main__":
    print(fix(int(sys.argv[1]), int(sys.argv[2])))
