# Run it yourself
From this folder, in a fresh shell (python3, standard library only):
    sh verify-it-yourself/run_checks.sh
Expected output:
    object: L=464 E=14396 F=7.4776
    published Table 3 L=464: E=14436 F=7.4569 (printed F 7.4569)
    PASS
Rebuild the object: decode the L = 461 row of Table 3 of arXiv:2607.09688v1 (hex digit -> 4 bits, keep the last 461 bits,
1 -> +, 0 -> -), then write "--" + that string + "+" on one line. It must equal object/L464.txt.
