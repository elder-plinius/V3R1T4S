#!/usr/bin/env python3
"""Standalone LABS checker (Python standard library), written from the definition:
for a +-1 sequence s of length L, C_k = sum_i s_i s_{i+k} (k = 1..L-1), E = sum_k C_k^2, F = L^2/(2E).
Checks object/L464.txt: alphabet {+,-}, length 464, exact integer energy, and compares it with the energy of the
published L = 464 sequence of Table 3 of arXiv:2607.09688v1 (Psenicnik, Boskovic, Popic, Brest), decoded here from the
hex string printed there (hex digit -> 4 bits, keep the last L bits, 1 -> +1, 0 -> -1)."""
import sys
TABLE3_L464_HEX = "fffffff0007fd80787e13f04f0dc393c8e58276cb978e466c3ce727932731a726cb4e646da1bce27586dcb1b48d2c52b16a5a558aa5552aaaaaa"
CLAIMED_E = 14396
def energy(s):
    L = len(s)
    return sum(sum(s[i] * s[i + k] for i in range(L - k)) ** 2 for k in range(1, L))
def main(path):
    line = open(path).readline().strip()
    if not line or set(line) - set("+-"):
        print("FAIL: alphabet"); return 1
    s = [1 if c == "+" else -1 for c in line]
    L = len(s)
    bits = bin(int(TABLE3_L464_HEX, 16))[2:].zfill(4 * len(TABLE3_L464_HEX))[-464:]
    t = [1 if b == "1" else -1 for b in bits]
    E, Et = energy(s), energy(t)
    print("object: L=%d E=%d F=%.4f" % (L, E, L * L / (2 * E)))
    print("published Table 3 L=464: E=%d F=%.4f (printed F 7.4569)" % (Et, 464 * 464 / (2 * Et)))
    ok = L == 464 and E == CLAIMED_E and Et == 14436 and E < Et
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1
if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "object/L464.txt"))
