"""Assertions over check_sc.py output. Usage: assert_sc.py full|p2 COUNT OUTPUT_FILE"""
import sys, re
mode, n, path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = [l for l in open(path) if l.startswith('(')]
ok = len(lines) == n
for l in lines:
    ok &= l.rstrip().endswith(' OK') and ' star=False ' in l
    ok &= (' needs_opt=False ' in l) if mode == 'full' else (' needs_opt=True ' in l)
gains = [float(re.search(r'gain=(\S+)', l).group(1)) for l in lines]
print(f'rows checked: {len(lines)} (expected {n}); smallest gain {min(gains):.3g}; largest gain {max(gains):.3g}')
print('assertions:', 'PASS' if ok else 'FAIL', '(every row OK, no star, label ' + ('absent' if mode == 'full' else 'present') + ')')
sys.exit(0 if ok else 1)
