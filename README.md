```
██╗   ██╗ ██████╗  ██████╗   ██╗ ████████╗ ██╗  ██╗ ███████╗
██║   ██║ ╚════██╗ ██╔══██╗ ███║ ╚══██╔══╝ ██║  ██║ ██╔════╝
██║   ██║  █████╔╝ ██████╔╝ ╚██║    ██║    ███████║ ███████╗
╚██╗ ██╔╝  ╚═══██╗ ██╔══██╗  ██║    ██║    ╚════██║ ╚════██║
 ╚████╔╝  ██████╔╝ ██║  ██║  ██║    ██║         ██║ ███████║
  ╚═══╝   ╚═════╝  ╚═╝  ╚═╝  ╚═╝    ╚═╝         ╚═╝ ╚══════╝
    hills no one has climbed · unknowns no one has known
```

<p align="center">
  <strong>Turn your unused tokens into scientific discoveries.</strong><br>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/results-53-brightgreen" alt="53 results" />
  <a href="LICENSING.md"><img src="https://img.shields.io/badge/license-AGPL--3.0_%7C_CC_BY_4.0-blue" alt="AGPL-3.0 code, CC BY 4.0 data" /></a>
</p>

<p align="center">
  <a href="#-w1ns"><strong>Wins</strong></a> ·
  <a href="#-known-unknowns"><strong>Known unknowns</strong></a> ·
  <a href="#-dont-trust-us-check-it"><strong>Check us</strong></a> ·
  <a href="#-j01n-th3-hunt"><strong>Join</strong></a> ·
  <a href="TROPHY_CASE.md"><strong>Trophy case</strong></a> ·
  <a href="AGENTS.md"><strong>For agents</strong></a>
</p>

**CIPHERS CRACKED. TABLES BEATEN. BOUNDS PUSHED. 🔓** 

Unsolved problems, liberated by legions of agents, verified by skeptics, reproducible by anyone. Matrix multiplication with fewer multiplications than any public catalogue, for five matrix shapes. Two unsolved cipher-machine challenges, cracked. The lower bound on Lehmer's 1932 totient problem pushed from 10²⁶ to a computer-verified 10⁵⁰. All from a one-shot routine prompt. And now, the same power is in your hands! May you wield it wisely.

### ⚡ Join in one line

Open an agent that can run code and paste:

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S
```

It asks six short questions, schedules nothing until you type **go** (setup only creates its own folder), and posts nothing without your **yes**. Most nights it finds nothing. Some nights it beats a table entry, and your name goes in the trophy case. Works with Claude Code, Codex, Gemini CLI, Grok Bot, Hermes and more: see [Pick your agent](#-pick-your-agent).

🤖 Agents: start at [AGENTS.md](AGENTS.md).

> *"Veritas liberabit nos."* The truth will set us free.

⊰•-•✧•-•-⦑/V\E/R\I/T\A/S\⦒-•-•✧•-•⊱

## 🏆 W1NS

| Win | Beats | Status |
|---|---|---|
| 🔐 Hebern 5-rotor, Problem 8 ("hard") | only solver on the setter's table | ✅ [Listed by the setter](http://www.jfbouch.fr/crypto/challenges/H5/index.html) |
| 🔐 Kryha v2, Problem 5 ("difficult") | only solver on the setter's table | ✅ [Listed by the setter](http://www.jfbouch.fr/crypto/challenges/KRYHA2/index.html) |
| 🕸️ Graph (15,4): 13,365 vertices | 11,780 (+13.5 %) | 🧪 Verified internally |
| 🕸️ 6 more degree–diameter cells | +0.03 % to +5.3 % | 🧪 Verified internally |
| 🔢 Lehmer: no counterexample below 10⁵⁰ | 10²⁶ certified, 10³⁰ claimed | 🧪 Computer-verified |
| ⚡ Matrix multiplication, 5 shapes | ⟨15,16,16⟩: 2,180 vs 2,223 | 🧪 Exact over ℚ |
| 🛡️ VNN-COMP 2026: 2 unresolved instances | no tool resolved them in time | 🧪 Validator: `correct` |
| 🎯 RobustBench CIFAR-100, one RN18 model | 27.57 % vs 27.67 % listed | 🧪 Verified internally |
| 📡 27 constant-weight codes (+ 5 LP bounds) | Brouwer's table, most by under 1 % | ✅ [Listed in Brouwer's table](https://aeb.win.tue.nl/codes/Andw.html) as [Pl] (3 more overtaken first) |

🧪 = checked by independent reviewer agents, each with its own code, plus the checkers shipped here. Not yet listed by the table owner. **53 results** in all: 46 checkable results, 5 linear-programming bounds and 2 sealed cipher solves. Each result names the exact table version it beats (the graph margins are against the 10 Oct 2026 snapshot), and almost all of them build on other people's published work, credited by name. Full detail → [TROPHY_CASE.md](TROPHY_CASE.md)

F. Comellas' degree–diameter page describes itself as AI-free. These graphs are offered to him, not claimed on his table; whether agent-found graphs belong there is his call.

<details>
<summary><strong>What do these mean?</strong></summary>

- **Hebern, Kryha:** 1920s cipher machines. J.-F. Bouchaudy publishes simulator challenges for them, with a public table of who solved what.
- **Degree–diameter:** how big can a network get when every node has few links and any two nodes are a few hops apart?
- **Lehmer's totient problem:** is there a composite number N for which φ(N) divides N − 1? Open since 1932. We show any such N is above 10⁵⁰; the problem stays open.
- **Matrix multiplication rank:** how few multiplications multiply two matrices of a given shape. These are theory results for five shapes; no practical speedup is claimed.
- **VNN-COMP:** a yearly contest for tools that prove neural networks safe on input ranges. We found counterexamples for two instances no tool resolved within the contest's 480 s limit.
- **RobustBench:** a public leaderboard of how hard image models are to fool. A stronger attack fools this model on 10 more images than listed.
- **Constant-weight codes:** error-correcting codes in which every codeword has the same number of 1s.

</details>

## 🗺 Known unknowns

The hills nobody has climbed yet: **287 open problems in 18 categories**, each with its own page: what counts as a win, how it's checked, where to confirm it's still open, ideas to start from, and the traps that fooled people before. Pick one and point your agent at it, or let it roam anywhere else.

| Category | Open | For example |
|---|---|---|
| 🧬 [Disease research](known-unknowns/disease-research/README.md) | 51 | cancer drug-response prediction, gene expression from tumour histology, epidemic forecasts |
| 🦠 [Biology](known-unknowns/biology/README.md) | 29 | protein and RNA fitness benchmarks, RNA design, single-cell analysis |
| ⚛️ [Physics](known-unknowns/physics/README.md) | 27 | lattice constants to record precision, quantum codes and SIC-POVMs, materials leaderboards |
| ⚪ [Packings and physics](known-unknowns/packings-physics/README.md) | 19 | sphere packings in a cube or a 4D ball, metal-cluster energy minima |
| 🔢 [Number hunts](known-unknowns/number-hunts/README.md) | 19 | the last unresolved Busy Beaver BB(6) machines |
| 🌍 [Earth and sky](known-unknowns/earth-and-sky/README.md) | 18 | missed marsquakes, bolides and tsunamis in open archives, solar-flare forecasts |
| 📊 [Record tables](known-unknowns/record-tables/README.md) | 17 | binary linear codes above codetables.de |
| 🔐 [Unbroken ciphers](known-unknowns/unbroken-ciphers/README.md) | 17 | the remaining unbroken 1941 German Army Enigma messages |
| 📜 [Undeciphered scripts](known-unknowns/undeciphered-scripts/README.md) | 16 | Linear A, the Indus script, unplaced cuneiform fragments |
| 🕸️ [Graphs, games, automata](known-unknowns/graphs-games-automata/README.md) | 14 | a smaller cage, the rectilinear crossing number of K₂₈ |
| ✏️ [Erdős problems and proofs](known-unknowns/erdos-and-proofs/README.md) | 13 | open Erdős problems with a computable edge |
| 💊 [Drug discovery](known-unknowns/drug-discovery/README.md) | 12 | ADMET, activity-cliff and docking leaderboards |
| 🚚 [Optimization benchmarks](known-unknowns/optimization-benchmarks/README.md) | 9 | best-known routes in CVRPLIB, open MIPLIB instances, hospital timetabling |
| 🔭 [Sky archives](known-unknowns/sky-archives/README.md) | 7 | variable stars and transits hiding in public survey data |
| ⚡ [Algorithms](known-unknowns/algorithms/README.md) | 6 | fewer additions for fast matrix multiplication |
| 🛡️ [ML robustness](known-unknowns/ml-robustness/README.md) | 5 | stronger attacks on RobustBench models |
| 🏺 [Ancient texts](known-unknowns/ancient-texts/README.md) | 4 | restoring damaged Akkadian signs |
| 🌋 [Herculaneum scrolls](known-unknowns/herculaneum-scrolls/README.md) | 4 | ink detection on carbonized papyrus |

Browse them all → [known-unknowns/](known-unknowns/README.md). To aim your agent at one:

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/<category>/<problem>.md
```

## 🔍 Don't trust us, check it

Every open result ships with the object itself, a short checker you can read in one sitting, a snapshot of the table it beat, and the code that generated it. Check the 13,365-vertex graph yourself in seconds (it prints `VALID`):

```sh
cc -O3 -o ddcheck known-knowns/biggest-graphs/verify-it-yourself/ddcheck.c -lpthread
./ddcheck known-knowns/biggest-graphs/graphs/G_15_4_n13365.edges 15 4 4
```

Start here → [READ_BEFORE_CITING.md](READ_BEFORE_CITING.md)

These results predate the contributor kit. Before release, two or three independent reviewer agents re-checked each one; the checkers shipped here re-check them today. If one is wrong, tell us and we will correct it in the open.

Puzzles with a living setter stay puzzles: the solution goes privately to the setter, and only a sealed hash (a fingerprint that proves we had the answer without revealing it) lives here → [DONT_SPOIL_THE_HUNT.md](DONT_SPOIL_THE_HUNT.md)

## 🛠 J01N TH3 HUNT

**1. Paste the line** from [Join in one line](#-join-in-one-line) into your agent.

**2. Answer six short questions** (or reply "ok" for the defaults): credit name · what you're curious about · time per run · schedule · share your research charter (the topic brief your agent writes)? · may it use what it knows about you? (default: no)

**3. Let it hunt.** It picks an open problem that fits your interests, from the [bank](bank/) or from any field where a stranger's computer can check the answer, and works on it in its own folder on your machine.

**What you get**
- 🏴 **Credit:** confirmed wins carry the name you choose, or a pseudonym.
- 🧠 **A front-row seat:** every run leaves a plain-language report of what your agent tried, what failed and why.
- 🎲 **Honest odds:** a clean "no" counts as a good night; a beaten table counts as a great one.
- 🔓 **Your own niche:** the six questions shape a research charter around what *you're* curious about.

**🛡️ Safe by design.** No **go**, no schedule. No **yes**, nothing leaves your machine. Runs stay inside the time per run you set.

Every new claim has to survive the gauntlet before it counts:

```
hunt --> null test --> 3 skeptics --> check_run.py --> your "yes" --> trophy case
```

- **Null test:** whenever luck could fake a result, the same pipeline runs on 400+ decoys first. If a decoy wins, so does luck.
- **3 skeptics:** three fresh contexts, each with its own code. Any one of them can kill the claim.
- **check_run.py:** a mechanical honesty check. PASS, or it didn't happen.
- **Your "yes":** nothing leaves your machine without it.

### 🧭 Pick your agent

**Claude Code:** run `claude` in any folder and paste the line.

<details>
<summary><strong>Codex, Gemini CLI, Grok Bot, Grok Build, Hermes, OpenClaw, Meta Muse, Cursor and more</strong></summary>

You need an agent that can run code: a terminal, a shell tool, or its own cloud computer.

| Agent | How to start | Notes |
|---|---|---|
| **Codex CLI** | `codex`, paste the line | Reads `AGENTS.md` natively; skeptics via `codex exec` |
| **Gemini CLI** | `gemini`, paste the line | Skeptics via `gemini -p` |
| **Grok Bot** (SpaceXAI × Cursor) | ask it the line | Runs in its own cloud computer, not your laptop |
| **Grok Build** (SpaceXAI's terminal agent) | start it in any folder, paste the line | Skeptics as its subagents |
| **Hermes Agent** (Nous) | `hermes`, paste the line | Use your strongest model; smaller ones tend to stop early |
| **OpenClaw** | message it the line | Approve its exec prompts during setup |
| **Meta Muse** | ask Muse the line | Runs in Muse's own cloud computer, not your laptop |
| **Cursor, OpenHands, Aider** | open an agent session, paste the line | No scheduler: say "run V3R1T4S" to hunt |
| 💬 **Chat-only bots** (@grok on X, chat apps) | paste the link | Can read and explain the repo, can't hunt without a shell |

Got it working somewhere new? [Open an issue](https://github.com/elder-plinius/V3R1T4S/issues) and tell us.

</details>

## ⚠️ Disclaimer

V3R1T4S is provided **as is**, without warranty of any kind (see [LICENSE](LICENSE) and [LICENSE-DATA](LICENSE-DATA)). You run it at your own risk:

- **Your agent, your responsibility.** You choose the agent, its permissions and its schedule. Monitor what it does, and stop it if you don't like what you see.
- **Your costs.** Runs spend your own plan, API credits and compute.
- **Your rules.** Follow the law, your agent provider's terms, and the terms of every site and dataset your agent touches.
- **No guarantees.** Results can be wrong until they are checked. Verify before you cite, submit or celebrate.
- **Not affiliated** with any table maintainer, puzzle setter, benchmark or AI company mentioned here.

The authors and contributors accept no liability for how the software is used or for anything an agent does with it.

⊰•-•✧•-•-⦑/V\E/R\I/T\A/S\⦒-•-•✧•-•⊱

🐉 Siblings: [L1B3RT4S](https://github.com/elder-plinius/L1B3RT4S) · [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) · V3R1T4S

#V3R1T4S

*Made with love by Pliny the Liberator <3*

⊰-•-•✧•-•-⦑/L\O/V\E/\P/L\I/N\Y/⦒-•-•✧•-•-⊱
