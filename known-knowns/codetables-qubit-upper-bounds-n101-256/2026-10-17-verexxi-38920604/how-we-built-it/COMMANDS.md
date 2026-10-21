# Commands used (from the run workspace; python-flint 0.9.0 in a venv)
- scan (bisection on d when 'descend' is set), window 8: venv/bin/python scan.py CELLS.json OUTDIR 1536 8
  with CELLS.json entries like {"n":135,"k":1,"d":D,"shadow":true,"descend":true,"lower":L}
- single LP: python qlp.py 135 1 45 shadow   (full row set; slower)
- propagation: python3 parse_table.py TABLE.html parsed.json; python3 propagate.py parsed.json closure.json
