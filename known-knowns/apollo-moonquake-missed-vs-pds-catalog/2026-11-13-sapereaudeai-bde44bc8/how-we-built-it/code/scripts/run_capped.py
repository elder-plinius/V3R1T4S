"""Run a script with scipy.fft threads capped (tools/threadcap.py, V3_WORKERS). usage: run_capped.py SCRIPT ARGS..."""
import sys, runpy
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import threadcap  # noqa: F401
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name='__main__')
