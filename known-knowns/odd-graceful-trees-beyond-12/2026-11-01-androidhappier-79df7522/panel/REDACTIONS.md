# Panel copies: redactions

The four panel files are copies of the run's panel/ files, made after the gate. The original packaging replaced a machine-local path. The review revision also replaces scratch paths and identifies original-run artifacts as unshipped. Verdicts and pass lines remain unchanged.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| novelty.md | the absolute path of the workspace's kit repository clone (line 22) | `[workspace]/repo` | c8d18c9d5ee4db359a849b37b391ce358018d83910b03ed6b24ea909fd75e376 |
| reproduce.md | nothing | - | e59d6673f0641904b8dfc193f38d2d6f27f9d7648e81c5697cfbdfd047c65701 |
| criterion.md | nothing | - | 63f0e99bac2a9de82ff39b0bcc36959e58a18217b2d566eb20b83ff1e501ca31 |
| gate.md | nothing | - | cf3addb8366266c62e371e2f09709c9261ed15e05565057c59d802adea0aaceb |

The original scratch paths were replaced with [scratch] in the review revision.
