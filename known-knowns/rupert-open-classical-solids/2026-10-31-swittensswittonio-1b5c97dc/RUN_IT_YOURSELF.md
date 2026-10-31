# Run it yourself

From a fresh shell in this folder (Python 3.9+, POSIX shell, .NET SDK 8+, network to github.com):

```sh
sh verify-it-yourself/run_checks.sh
```

It (1) checks the sha256 of every file in `object/` against `verify-it-yourself/object.sha256`, (2) downloads the pinned GitHub archive of Hervay's repository (commit 802a3ded09535c4a99cef1371ce0d0277c433fa8) and extracts only the certificate, the 38 cover files and `paper/appendices/b-zoom-covers.tex`, each checked against `verify-it-yourself/INPUTS.sha256` (search.cert must hash to df1f8dbab68b561f22fa9daeca48153d71bde7b6fba3345d9f6b7b8077df4b5f; clone with `core.autocrlf=false` if you fetch it by git instead, a CRLF checkout changes the hash), (3) builds the C# verifier, (4) runs `RidVerify.dll all`. Exit code 0 and last line `PASS` on success; any failure ends in `FAIL`.

By hand:

```sh
mkdir -p w/attempts/csharp-verifier/code w/attempts/csharp-verifier/result w/data/hervay_inputs
cp -r object/RidVerify w/attempts/csharp-verifier/code/
python verify-it-yourself/fetch_inputs.py w/data/hervay_inputs
cd w/attempts/csharp-verifier/code/RidVerify
dotnet build -c Release -o ../build
dotnet ../build/RidVerify.dll all
```

Sub-commands: `geom`, `domain`, `global`, `localexotic`, `cover <names>`, `cube`, `all --no-controls`. Environment overrides: `RID_CERT`, `RID_COVERS`, `RID_INPUTS`, `RID_RESULT`. `object/verification_log.txt` and `object/summary.json` are the author's own run for comparison.
