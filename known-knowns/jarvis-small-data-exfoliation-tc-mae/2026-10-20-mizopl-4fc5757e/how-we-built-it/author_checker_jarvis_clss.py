#!/usr/bin/env python3
"""
Standalone Author Verification Wrapper for:
  target_id: jarvis-small-data-exfoliation-tc-mae
  tasks:
    1. dft_3d_exfoliation_energy (AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae, claimed primary + p2)
    2. tinnet_N_ead              (AI-SinglePropertyPrediction-ead-tinnet_N-test-mae, uncredited supplementary; p1 dropped)
"""
import subprocess
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
VERIFIER = PKG_ROOT / "verify-it-yourself" / "check_jarvis_clss_package.py"


def main():
    res = subprocess.run([sys.executable, str(VERIFIER)], check=False)
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
