#!/usr/bin/env python3
"""Run a command and report peak RSS (kB) of the process tree (best-effort)."""
import os, sys, time, subprocess, resource

cmd = sys.argv[1:]
if not cmd:
    print("usage: measure_peak.py CMD...", file=sys.stderr)
    sys.exit(2)
# resource.ru_maxrss is KB on Linux for this process only; run in-process via fork
pid = os.fork()
if pid == 0:
    os.execvp(cmd[0], cmd)
else:
    peak = 0
    while True:
        try:
            # read child VmHWM
            st = open(f"/proc/{pid}/status").read()
            for line in st.splitlines():
                if line.startswith("VmHWM"):
                    peak = max(peak, int(line.split()[1]))
        except FileNotFoundError:
            break
        except ProcessLookupError:
            break
        w = os.waitpid(pid, os.WNOHANG)
        if w[0] == pid:
            break
        time.sleep(0.05)
    # final wait
    try:
        _, status = os.waitpid(pid, 0)
    except ChildProcessError:
        status = 0
    print(f"PEAK_RSS_KB {peak}")
    sys.exit(os.WEXITSTATUS(status) if os.WIFEXITED(status) else 1)
