# Run it yourself

## 1. The checker (seconds, standard library only)
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh            # offline: the files in object/ and the-record-we-beat/
    sh verify-it-yourself/run_checks.sh --live     # also refetches the ComCat and ISC absence queries once

Expected output: one `ok` line per check, then `VERIFIED p1: ...` and `PASS`. verify-it-yourself/RECEIPTS.md is a real
run.

## 2. The absence, by hand
- **ComCat:** https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradiuskm=50
  Expect the header line only.
- **ISC:** https://www.isc.ac.uk/fdsnws/event/1/query?starttime=2024-12-09T23:19:43&endtime=2024-12-09T23:20:44&latitude=39.1635&longitude=-119.0459&maxradius=0.45&format=text
  Expect HTTP 204.

## 3. Rebuilding the object from public waveforms (about 2 h on 12 cores)
The scripts are in how-we-built-it/code/. They expect the claim layout: code/, data/, event.json and picks.csv in one
folder. how-we-built-it/claim/REPRODUCE.md gives a command for every number.

**Before you start:** `run`, `summary` and early_null.py need data/templates.json (5.1 MB). It is not in this
package; it is archived at doi:10.5281/zenodo.23679540 (CC BY 4.0), and the curl line below fetches it.

    mkdir claim && cp -R how-we-built-it/code claim/ && cp object/event.json object/picks.csv claim/
    mkdir claim/data && cp how-we-built-it/data/* claim/data/
    cd claim
    curl -L -o data/templates.json https://zenodo.org/api/records/23679540/files/templates.json/content
    shasum -a 256 data/templates.json   # b854598020c132bc57cdcdfb609c8196739a52ae0f136e2548230c52b40f9a54
    pip install -r ../how-we-built-it/requirements.txt
    python -I code/null_full.py fetch      # 32 HHZ day files from service.earthscope.org
    python -I code/null_full.py prep
    python -I code/null_full.py run 12     # about 95 min on 12 cores
    python -I code/null_full.py summary    # prints the event NCC 0.6705, best control 0.6121, count 0
    python -I code/early_null.py 12 3000   # about 7 min: 1 of 3000 >= 0.6706, EFC_early 0.0120
    python -I code/locate.py               # 39.1635 N 119.0459 W 7.0 km, RMS 0.1787 s, herr 3.446 km

- **Third-party data, not copied in:** the event and calibration waveform windows, the StationXML responses, the ComCat
  CSVs and the Zenodo catalogue are refetched by URL.
  - **URLs:** event.json `waveform_urls_event_window`, `code/mag_check.py fetch`, how-we-built-it/data/fetchlog_*.jsonl
    and mc_histograms.csv.
  - **Integrity:** the sha256 of every file the claimant used is in how-we-built-it/claim_data_manifest.json.
- **Larger than 1 MB, so kept out of git:** data/templates.json (the 385 templates; size and sha256 in
  claim_data_manifest.json). null_full.py and early_null.py need it.
  - **Archive:** doi:10.5281/zenodo.23679540 (Walsh 2026, CC BY 4.0), with a README on the file format. Its sha256 matches
    claim_data_manifest.json.
  - **Also:** the per-control maxima in object/ are the null's full output, and they were independently recomputed
    by the REPRODUCE skeptic (panel/reproduce.md section 6).
