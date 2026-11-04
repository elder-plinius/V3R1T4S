# Panel copies: redactions

The four panel files are byte-for-byte copies of the run's panel/ files, made after the gate. They were scanned for
absolute machine-local paths, unfilled-placeholder tokens (such as the letter n in angle brackets) and the other leaks
kit/check_run.py scans for. None were found, so nothing was replaced. Wording, verdicts and pass lines are untouched.

| file | replaced | sha256 of the run's original (= this copy) |
|---|---|---|
| reproduce.md | nothing | daa8d3257e5a2c8d3540b65366db6bdcc26b3789f9c42f795a8573c0259b9e84 |
| novelty.md | nothing | 8460ee903940bdbe9ee2385415fdcb1a16bf703298587890da25529f8e9057a8 |
| criterion.md | nothing | a973333244d79bdf6e7c543067ec06031efb8774147dca07758834addb94b794 |
| gate.md | nothing | 7aea56ea437dbeff1ea6a13f3fd6abe27da83ab4bd2a11120ca12c49513cf6ee |

A note on names: the panel text refers to the run's uncompressed files result/cert_16.txt ... cert_22.txt. This
package ships the same files gzip-compressed as object/certs/cert_N.txt.gz (orders 4..20) and pins order 22 as an
external file. object/CERTIFICATES.txt lists each file's uncompressed sha256, which equals the value in the run's
result/SHA256SUMS.txt.

The criterion skeptic mentions a scratch copy under its own temporary folder; that path is not needed for checking.
