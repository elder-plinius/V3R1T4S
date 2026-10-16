# Run it yourself
From this folder, in a fresh shell (python3, standard library only):
    sh verify-it-yourself/run_checks.sh
Expected output:
    object: L=463 E=14047 F=7.6304
    published Table 3 L=463: E=14439 F=7.4233 (printed F 7.4233)
    PASS
Rebuild the object: decode the L = 461 row of Table 3 of arXiv:2607.09688v1 (hex digit -> 4 bits, keep the last 461 bits,
1 -> +, 0 -> -), then write "-" + that string + "+" on one line. It must equal object/L463.txt.
