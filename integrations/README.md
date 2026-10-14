# GPT-Orca-LLM research bridge

This optional **read-only interface** makes a V3R1T4S research task into a
structured packet usable with the GPT-Orca-LLM council in
[sonoxo/gpt-doug-llm PR #417](https://github.com/sonoxo/gpt-doug-llm/pull/417).

It does **not** load or run a model itself. It does not execute a scientific
attack, establish discoveries, authenticate into other projects, create
accounts, or automatically submit results.

Usage from the V3R1T4S repository:

```bash
python3 integrations/orca_bridge.py "target-id" "Evaluate two candidate research approaches"
python3 -m unittest discover -s integrations/tests -v
```

The JSON output includes four GPT-Orca roles, policy references, and required
proof-quality constraints. Review the packet and supply it to your authorized
model runtime as task data. It is not a research result. Follow
`AGENTS.md`, `kit/RULES.md`, `kit/POLICY.md`, `kit/SETUP.md`, and
`kit/RUN.md`. Do not run V3R1T4S experiments or change its charter without
the documented setup and permissions.

No GPT-Orca code or model weights are copied into V3R1T4S, avoiding
cross-project dependency and license conflicts.
