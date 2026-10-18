"""Optional: if env STUB_MPL=1, register an empty stand-in for matplotlib.pyplot BEFORE sigtypst2022 is imported.
sigtypst2022 imports pyplot at module level but uses it only in the CLI branches (--compare-systems plots, --evaluate
figure), never in compare_words / compare_systems / predict_words. Importing the real pyplot on macOS makes
matplotlib run `system_profiler -xml SPFontsDataType` to build its font cache, which is starved on this loaded machine."""
import os, sys, types
if os.environ.get("STUB_MPL") == "1":
    mpl = types.ModuleType("matplotlib"); plt = types.ModuleType("matplotlib.pyplot")
    mpl.pyplot = plt; sys.modules["matplotlib"] = mpl; sys.modules["matplotlib.pyplot"] = plt
    print("[calibrator] matplotlib.pyplot stubbed (STUB_MPL=1)", file=sys.stderr)
