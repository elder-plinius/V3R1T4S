# Panel copies: redactions

The panel files are copies of the run's panel/ files, made after the gate (2026-11-03T20:41Z). One string in
novelty.md was replaced so the package passes the kit/check_run.py leak scan. Wording, verdicts, the
confirmed_scope line, context lines and pass lines are untouched.

| file | replaced | with | sha256 of the run's original |
|---|---|---|---|
| novelty.md | line 30: an entry of the contributor's never-publish list, inside the sibling package's outbox folder name | `[redacted]` | 4018d671388e086a1f16242f2e0297179001270a12aaacebcfbc87b8f7f93064 |
| reproduce.md | nothing | - | e5eb89b83fd539944a66adc6251db41e6f86fb26391536f0e2e763e5670fb947 |
| criterion.md | nothing | - | 1872203fbbded55809863e4c82858ba5a60bd3ae6bc42b833e8fca1e1e6f4821 |
| gate.md | nothing | - | b76aaaa6f739bd700398faa9998f36789c04e7a3e48c24838aa8b14da5199a55 |
| reproduce_checker.py | nothing | - | 63cfb13abcd404d73b1ab4afd5810a1b1d3e4721eeadb6979cfee0cab24020c2 |

The scratch-folder paths under /workspace/ that the skeptics mention are their own temporary copies, not paths
needed for checking.
