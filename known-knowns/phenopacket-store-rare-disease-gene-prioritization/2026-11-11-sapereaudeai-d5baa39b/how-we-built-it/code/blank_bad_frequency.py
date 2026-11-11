"""PREREG.v4: blank HPOA frequency cells n/m with n > m (LIRICAL 2.4.1 refuses to load them). Other cells unchanged.
usage: python -I blank_bad_frequency.py <in.hpoa> <out.hpoa>"""
import sys, re
n = 0
with open(sys.argv[1], encoding='utf-8') as fi, open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as fo:
    for line in fi:
        if not line.startswith('#'):
            f = line.rstrip('\n').split('\t')
            if len(f) > 7:
                m = re.fullmatch(r'(\d+)/(\d+)', f[7])
                if m and int(m.group(1)) > int(m.group(2)):
                    f[7] = ''; n += 1; line = '\t'.join(f) + '\n'
        fo.write(line)
print(sys.argv[1].replace(chr(92), '/').split('/')[-1], 'blanked', n)
