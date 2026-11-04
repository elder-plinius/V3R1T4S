#!/bin/bash
# timed.sh OUTPREFIX cmd... : runs cmd, records wall seconds and peak RSS (sampled 1/s from /proc)
pre=$1; shift
s=$(date +%s.%N); "$@" > $pre.out 2> $pre.err & pid=$!; echo $pid > $pre.pid; peak=0
while kill -0 $pid 2>/dev/null; do r=$(awk '/VmHWM/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "$r" ] && [ "$r" -gt "$peak" ] && peak=$r; sleep 1; done
wait $pid; ec=$?; e=$(date +%s.%N); echo "exit=$ec wall_s=$(python3 -c "print(round($e - $s,1))") peak_rss_kb=$peak" > $pre.time
