#!/bin/bash
cd "$(dirname "$0")"
while kill -0 200855 2>/dev/null; do sleep 20; done
./ladder.sh 14 60 600; ./ladder.sh 15 70 600; ./ladder.sh 16 88 600; ./ladder.sh 17 110 600; ./ladder.sh 18 142 900
