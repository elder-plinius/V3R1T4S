#!/bin/sh
set -eu
exec nice -n 19 python3 -B verify-it-yourself/verify.py
