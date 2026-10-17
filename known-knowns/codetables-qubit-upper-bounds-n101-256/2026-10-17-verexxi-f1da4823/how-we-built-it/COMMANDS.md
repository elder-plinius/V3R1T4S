# Commands used (from the run workspace; python-flint 0.9.0 in a venv)
- scan (bisection on d when 'descend' is set), window 8: venv/bin/python scan.py CELLS.json OUTDIR 1536 8
  with CELLS.json entries like {"n":195,"k":2,"d":D,"shadow":true,"descend":true,"lower":L}
- single LP: python qlp.py 195 2 65 shadow   (full row set; slower)
- propagation: python3 parse_table.py TABLE.html parsed.json; python3 propagate.py parsed.json closure.json
