"""Run a command with a hard wall-clock cap (macOS has no coreutils timeout). Usage: capped.py SECONDS cmd..."""
import subprocess, sys
p = subprocess.Popen(sys.argv[2:])
try:
    sys.exit(p.wait(timeout=float(sys.argv[1])))
except subprocess.TimeoutExpired:
    p.terminate()
    try: p.wait(timeout=30)
    except subprocess.TimeoutExpired: p.kill()
    sys.exit(124)
