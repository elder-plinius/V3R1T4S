# Commands used (from the run workspace; python-flint 0.9.0 in a venv)
- scan with bisection on d, window 8:  venv/bin/python scan.py CELLS.json OUTDIR 1536 8
  where CELLS.json held {"n":150,"k":1,"d":51,"shadow":true,"descend":true,"lower":33} (from the k = 1 sweep)
- single LP: python qlp.py 150 1 50 shadow   (full row set; slower)
- propagation: python3 parse_table.py TABLE.html parsed.json; python3 propagate.py parsed.json closure.json
