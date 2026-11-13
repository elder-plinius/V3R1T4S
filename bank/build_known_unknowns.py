#!/usr/bin/env python3
"""Build known-unknowns/ (one guide page per open problem, grouped by category) from bank/targets.json.

bank/targets.json stays the single source of truth: edit it, then rerun
    python3 bank/build_known_unknowns.py
Standard library only. SPDX-License-Identifier: AGPL-3.0-or-later
"""
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "known-unknowns")
REPO = "https://github.com/elder-plinius/V3R1T4S"

ICONS = {
    "unbroken-ciphers": "🔐", "undeciphered-scripts": "📜", "ancient-texts": "🏺", "herculaneum-scrolls": "🌋",
    "number-hunts": "🔢", "erdos-and-proofs": "✏️", "record-tables": "📊", "graphs-games-automata": "🕸️",
    "packings-physics": "⚪", "algorithms": "⚡", "optimization-benchmarks": "🚚", "sky-archives": "🔭",
    "ml-robustness": "🛡️", "disease-research": "🧬", "drug-discovery": "💊", "biology": "🦠", "physics": "⚛️", "earth-and-sky": "🌍",
    "machine-learning": "🤖", "crypto-math": "🗝️", "compression-and-golf": "🗜️", "recreational-math": "🎲",
    "formal-proofs": "✅", "wildcard": "🃏",
    "planetary-science": "🪐", "genomics": "🧫", "neuroscience": "🧠", "ecology": "🐦", "chemistry-materials": "⚗️", "engineering": "🛠️", "particle-physics": "💥",
    "uncharted": "🧭", "lost-and-hidden": "⚓", "animal-communication": "🐋", "new-species": "🦋",
}
KIND = {"harvest": "harvest (many cells or partial wins within reach)", "standard": "standard",
        "moonshot": "moonshot (famous, long odds)"}


def load(name):
    with open(os.path.join(ROOT, "bank", name), encoding="utf-8") as f:
        return json.load(f)


def stars(t):
    try:
        n = int(round(float(t)))
    except (TypeError, ValueError):
        return "?"
    return "★" * n + "☆" * (5 - n)


def cell(s):
    return re.sub(r"\s+", " ", str(s)).replace("|", "\\|").strip()


def short(s, n=90):
    s = cell(s)
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def bullets(items):
    out = []
    for x in items or []:
        if isinstance(x, dict):
            x = x.get("statement") or x.get("text") or json.dumps(x, ensure_ascii=False)
        out.append("- " + re.sub(r"\s+", " ", str(x)).strip())
    return "\n".join(out)


def links(urls):
    out = []
    for u in urls or []:
        u = str(u).strip()
        out.append("- <%s>" % u if re.match(r"https?://", u) else "- " + u)
    return "\n".join(out)


def page(t, cat):
    commit_only = t.get("disclosure") == "commit-only"
    rel = "%s/%s.md" % (t["category"], t["id"])
    L = ["# %s\n" % t["name"].strip(),
         "%s **%s** · %s · tractability %s · compute: %s · open as of %s\n" % (
             ICONS.get(cat["id"], "•"), cat["name"], KIND.get(t.get("kind"), t.get("kind", "")),
             stars(t.get("tractability")), t.get("compute_profile", "?"), t.get("status_checked", "?"))]
    if commit_only and t["category"] == "lost-and-hidden":
        L.append("> 🔒 **Sealed location.** Never publish where it is: the exact place goes privately, sent by your human, "
                 "to the authority named under What counts as a win, and only a salted hash goes in this repo. Public "
                 "remote-sensing data only: nobody visits, dives on, digs, metal-detects, disturbs, recovers or removes "
                 "anything; where no functioning authority exists, the place is sent to nobody. Never put a location "
                 "in an issue or pull request. See [DONT_SPOIL_THE_HUNT.md](../../DONT_SPOIL_THE_HUNT.md).\n")
    elif commit_only:
        L.append("> 🔒 **Live puzzle with a living setter.** Solve it, but never publish the answer: it goes privately to "
                 "the setter, and only a salted hash goes in this repo. See [DONT_SPOIL_THE_HUNT.md]"
                 "(../../DONT_SPOIL_THE_HUNT.md).\n")
    L += ["## The problem\n", t.get("statement", "").strip() + "\n",
          "## What counts as a win\n", t.get("success_criterion", "").strip() + "\n"]
    if t.get("partial_wins"):
        L += ["## Partial wins\n",
              "\n".join("- **%s:** %s" % (p.get("id", "?"), re.sub(r"\s+", " ", p.get("statement", "")).strip())
                        for p in t["partial_wins"]) + "\n"]
    L += ["## How a win is checked\n", t.get("verification_method", "").strip() + "\n",
          "## Is it still open?\n",
          "Check the status page before you start and again before you claim anything; tables move fast.\n",
          "- <%s>\n" % t["status_source"] if t.get("status_source") else ""]
    if t.get("primary_sources"):
        L += ["## Sources\n", links(t["primary_sources"]) + "\n"]
    if t.get("angles"):
        L += ["## Ideas to start from\n", "Starting points, not instructions. The best wins came from angles nobody "
              "listed.\n", bullets(t["angles"]) + "\n"]
    elif cat["id"] in ("unbroken-ciphers", "undeciphered-scripts"):
        L += ["## Ideas to start from\n", "Left out on purpose, so this page never spoils the hunt.\n"]
    if t.get("pitfalls"):
        L += ["## Traps\n", "False wins others have fallen for. A claim that walks into one of these will not "
              "survive the skeptics.\n", bullets(t["pitfalls"]) + "\n"]
    L += ["## Point your agent at it\n",
          "```\nset up V3R1T4S: %s and hunt known-unknowns/%s\n```\n" % (REPO, rel),
          "Already set up? Say `run V3R1T4S on %s`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the "
          "status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.\n" % t["id"],
          "---\n",
          "_Generated from [`bank/targets.json`](../../bank/targets.json) (id `%s`). Found it solved, stale or "
          "wrong? Open an issue or a pull request against that file%s._\n" % (
              t["id"], ", with no location in it" if commit_only and t["category"] == "lost-and-hidden" else "")]
    return "\n".join(x for x in L if x != "")


def main():
    targets = load("targets.json")
    targets = targets["targets"] if isinstance(targets, dict) else targets
    cats = load("categories.json")["categories"]
    by = {c["id"]: [] for c in cats}
    for t in targets:
        by.setdefault(t["category"], []).append(t)
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    order = sorted(cats, key=lambda c: -len(by.get(c["id"], [])))
    idx = ["# 🗺 Known unknowns\n",
           "The hills nobody has climbed yet: **%d open problems in %d categories**. Each page says what the problem "
           "is, what counts as a win, how a win is checked, where to check it is still open, ideas to start from, "
           "and the traps that produced false wins before.\n" % (len(targets), len(cats)),
           "Pick one, then tell your agent:\n",
           "```\nset up V3R1T4S: %s and hunt known-unknowns/<category>/<problem>.md\n```\n" % REPO,
           "Or don't pick: your agent can roam anywhere, as long as a stranger's computer can check the answer.\n",
           "| Category | Open | What's in it |\n|---|---|---|"]
    for c in order:
        ts = sorted(by.get(c["id"], []), key=lambda t: (-(t.get("tractability") or 0), t["name"]))
        if not ts:
            continue
        d = os.path.join(OUT, c["id"])
        os.makedirs(d)
        for t in ts:
            with open(os.path.join(d, t["id"] + ".md"), "w", encoding="utf-8") as f:
                f.write(page(t, c))
        rows = ["| %s | [%s](%s.md) | %s | %s |" % (stars(t.get("tractability")), short(t["name"]), t["id"],
                                                     t.get("kind", ""), t.get("compute_profile", ""))
                for t in ts]
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
            f.write("# %s %s\n\n%s\n\n**%d open problems**, easiest first. Tractability is a rough guess at the odds "
                    "for one agent on one machine (★ long shot, ★★★★★ likely).\n\n| Odds | Problem | Kind | Compute |\n"
                    "|---|---|---|---|\n%s\n\n← [All categories](../README.md)\n"
                    % (ICONS.get(c["id"], "•"), c["name"], c["description"], len(ts), "\n".join(rows)))
        idx.append("| %s [%s](%s/README.md) | %d | %s |" % (ICONS.get(c["id"], "•"), c["name"], c["id"], len(ts),
                                                          cell(c["description"])))
    idx += ["", "Tractability, compute and status dates are guesses from the day each page was written; the status "
                "page linked on each problem is the only authority. Every page is generated from "
                "[`bank/targets.json`](../bank/targets.json): `python3 bank/build_known_unknowns.py`.\n"]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx))
    print("wrote %d problem pages in %d categories to %s" % (len(targets), len([c for c in cats if by.get(c["id"])]),
                                                            OUT))


if __name__ == "__main__":
    main()
