"""drat-trim's parser can misread a formula that has a comment line after its header line (a satisfiable formula
with such a line was reported "trivial UNSAT ... s VERIFIED" in a test made by the panel's reproduce skeptic on
2026-11-12). This script checks that no formula file of the certificate is exposed to that: the first line of every
file is the header "p cnf V C" and every later line is a clause line (it starts with a digit or a minus sign).
Standard library only; reads the files, writes nothing.
Usage: python no_comment_lines.py FILE_OR_FOLDER [FILE_OR_FOLDER ...]     (folders are searched for *.cnf)"""
import glob, os, sys

files = []
for a in sys.argv[1:]:
    files += sorted(glob.glob(os.path.join(a, '**', '*.cnf'), recursive=True)) if os.path.isdir(a) else [a]
bad = 0
for p in files:
    with open(p, 'rb') as f:
        first = f.readline()
        odd = sum(1 for line in f if line[:1] not in b'-123456789')
    if not first.startswith(b'p cnf ') or odd:
        bad += 1
        print('ODD %s: first line %r, %d later lines that are not clause lines' % (p, first[:30], odd))
print('%d formula files read; %d with a first line that is not the header or with a later line that is not a clause' % (len(files), bad))
print('NO COMMENT LINES: %s' % ('PASS' if files and bad == 0 else 'FAIL'))
sys.exit(0 if files and bad == 0 else 1)
