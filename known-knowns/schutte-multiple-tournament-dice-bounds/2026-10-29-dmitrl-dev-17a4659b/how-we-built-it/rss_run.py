"""Run a command, then print its wall time and peak resident set size (getrusage of children; bytes on macOS)."""
import subprocess, resource, sys, time
t0 = time.time(); r = subprocess.run(sys.argv[1:]); dt = time.time() - t0
mx = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
print(f"rc={r.returncode} wall={dt:.1f}s peak_rss={mx / 2**20:.0f} MiB", file=sys.stderr)
sys.exit(r.returncode)
