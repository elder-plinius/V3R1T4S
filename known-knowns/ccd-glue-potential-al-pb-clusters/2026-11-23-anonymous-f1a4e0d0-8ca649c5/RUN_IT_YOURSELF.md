# Run it yourself

From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh
    # expected: "inputs sha256 ok", 11 calibration lines with |E_posted - E_table| < 1e-6, mpmath iterations ending
    # with |grad| about 1e-23, object E = -198.4790291663 eV, margin -0.267632 eV, Hessian: near-zero modes 6,
    # negative 0, posted N=121 polished -198.2113965759 eV, last line PASS

Rebuilding the object (how-we-built-it/; python3 with numpy, scipy and mpmath, a C compiler). DATA holds lead_table.html,
lead.f, aluminum.f (the loader parses it at import) and the point archive extracted into lead_points/, arranged as
common.py expects (a run folder with data/, checker/ holding certify/*, and attempts/ holding common.py and the steps):
1. step1-bh-from-posted: `python3 driver.py Pb 60 160 120 <workers> <seedbase>` (120 s basin hopping per cell from each posted file; the
   worker count and seed base of the original run were not recorded);
   cell 121 ended at -198.2409841872 eV (result_121.json).
2. step2-bh-from-step1: `bh.py Pb 121 300 11 output start/Pb_121_obj.xyz` from that structure (run.sh); seed 11 ended at
   -198.47902916627 eV (results_121.jsonl). Basin hopping is stochastic and was run under machine load, so a rerun
   reaches it only with some probability; the object in object/ is the frozen result.
3. certify: `python3 certify_pb.py ../../object/Pb_121.txt 121 -198.211397 lead_points/121 out.xyz` (certify_output_2026-11-22.txt).
