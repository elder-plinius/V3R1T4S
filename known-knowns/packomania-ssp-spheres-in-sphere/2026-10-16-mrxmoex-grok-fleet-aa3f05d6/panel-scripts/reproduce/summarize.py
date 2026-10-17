#!/usr/bin/env python3
"""Apply the panel TIE rule (|gap|<=1e-9 is not a finding) to indep_check.out.txt and compare with the package CSV.
Run from this folder: python3 summarize.py"""
import csv
rows=[]
for l in open('indep_check.out.txt'):
    s=l.split()
    if ' gap ' in l: rows.append((int(s[0]),float(s[4]),float(s[6])))
big=[t for t in rows if t[1]>1e-9]; tie=[t for t in rows if t[1]<=1e-9]
below=sum(l.startswith('BELOW') for l in open('indep_check.out.txt'))
print('rows gap>1e-9:',len(big),'N range',min(t[0] for t in big),max(t[0] for t in big))
print('min gap',min(big,key=lambda t:t[1])[:2],'max gap',max(big,key=lambda t:t[1])[:2])
hm=max(abs(t[2]) for t in big); print('max |ssp.html - coord| in those rows',hm)
print('rows below coords:',below,' tie-level (<=1e-9, html equal to radius.txt there):',[t[0] for t in tie])
csvN=sorted(int(r['N']) for r in csv.DictReader(open('../../object/ssp_radiustxt_errata.csv')))
same = csvN==sorted(t[0] for t in big); print('N set equals package CSV:',same)
print('PASS' if len(big)==90 and hm<2.8e-12 and below==0 and same and min(t[0] for t in big)==1055 else 'FAIL')
