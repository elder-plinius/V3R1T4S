"""Check that every row's best_known in certificates.csv equals the 'Best known' value of the same instance on the saved table page
(standard library only). Usage: python3 check_table.py <matsp.html> <certificates.csv>   Prints PASS if all rows match."""
import sys, re, html, csv
cells = re.findall(r'<td[^>]*>(.*?)</td>', open(sys.argv[1], errors='replace').read(), re.S); cells = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in cells]
table = {}
for k in range(0, len(cells) - 5):
    if cells[k].isdigit() and all(c.isdigit() for c in cells[k + 1:k + 5]) and re.fullmatch(r'[A-Z][A-Za-z0-9]+', cells[k + 5]):
        table.setdefault(cells[k], (int(cells[k + 4]), cells[k + 5]))
rows = list(csv.DictReader(open(sys.argv[2]))); bad = [r['instance'] for r in rows if table.get(r['instance'], (None,))[0] != int(r['best_known'])]
print('table rows read: %d; certificate rows: %d; mismatches: %s' % (len(table), len(rows), bad or 'none'))
print('PASS' if rows and not bad and len(table) == 225 else 'FAIL'); sys.exit(0 if rows and not bad and len(table) == 225 else 1)
