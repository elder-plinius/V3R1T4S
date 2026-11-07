#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
PY=$(command -v python3 || command -v python)
"$PY" verify-it-yourself/check_domatic.py object/dom-Q11-19-partition.txt 19 cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4,3beb06dc4cb19d7e3e5f690deaf36bf54d222d7ebd62a1eb541dbf25f160e78e
