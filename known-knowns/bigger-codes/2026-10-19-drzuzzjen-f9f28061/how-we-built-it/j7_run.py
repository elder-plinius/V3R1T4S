"""Stage G job wrapper (adapted from Stage F j5_run.py: + gain-time curve CSV and final kept fractions) (runs as the OWNED process under the pte-eval supervisor's Job Object; everything it starts
-- the engine, the checkers -- is in the same job tree).
1. Last-start gate: if now >= CUTOFF_UTC exit 3 without starting anything.
2. Start lb_lns_gen.py START 25 6 11 PREFIX --seconds S --rounds 1000000 --seed SEED as a child (stdout -> job log).
3. While the engine runs (poll 2 s): when PREFIX.log shows a best >= max(BAR, last frozen + 1), freeze PREFIX_best.npy:
   bytes read in memory (retry on a torn read), M = #unique words; if M >= BAR and M > last frozen:
   OUTDIR/CANDIDATE_M<M>.npy (exact bytes) + CANDIDATE_M<M>.txt (0/1, char j = bit j, sorted), both checkers run
   SEQUENTIALLY on the .txt -> CANDIDATE_M<M>_cwcheck_int.json / _cwcheck_set.json, record CANDIDATE_M<M>_freeze.json
   (sha256 of all, UTC, fraction of start words and of seed words). Never overwrites an existing file. The engine keeps
   running (no stop on a candidate).
4. After the engine exits: one last freeze attempt, then tools-equivalent post-check (post_check.py) on PREFIX.
Exit code = the engine's.
Stage I change (j6 = j5 + pause): the engine is a separate child process; before the checkers run on a snapshot the
wrapper SUSPENDS the engine (psutil suspend of the engine pid and any descendants) and RESUMES it after both checkers
end (in a finally block), so engine + checker never run at the same time (aggregate <= 4 threads). The engine's own
clock keeps running during the pause (same --seconds budget, same supervisor deadline). Logged with microsecond UTC:
PAUSE_AT, CHECK_START, ENGINE_SAMPLE (num_threads, cpu_percent over 1 s, status, taken during the check),
CHECK_END, RESUME_AT, ENGINE_CPU_DURING_PAUSE (cpu-time delta of the engine over the whole pause). Optional
--test-snapshot-after S (test only): once, S s after engine start, snapshot+check the current best (PREFIX_best.npy, else
PREFIX_cur.npy) regardless of BAR, so the pause sequence is exercised; with this flag ALL snapshots are named
CANDIDATE_TEST_M<M>.* (never CANDIDATE_M<M>).
Stage W change (j7 = j6 + fail-closed paths, Manager 6263866201): (P1) the watchdog KILLS the running checker and waits
for it to exit, never resumes the engine, kills the engine tree and the job exits 5; (P2) a snapshot whose re-read sha256
differs is not checked, the engine is killed and the job exits 6; (P3) a frozen snapshot with both_valid false or a
post-check with rc != 0 / both_valid false makes the job exit 7. Test-only env hooks (default off): J7_WATCHDOG_S,
J7_TOOLS, J7_POSTCHECK, J7_TEST_CORRUPT_TXT.
usage: j7_run.py CUTOFF_UTC ENGINE START PREFIX SECONDS SEED BAR OUTDIR SEED_NPY [--test-snapshot-after S]"""
import datetime, hashlib, io, json, os, re, subprocess, sys, threading, time
import numpy as np
import psutil
cutoff, eng, start, prefix, secs, seed, bar, outdir, seednpy = sys.argv[1:10]
bar = int(bar)
test_after = float(sys.argv[sys.argv.index("--test-snapshot-after") + 1]) if "--test-snapshot-after" in sys.argv[10:] else None
STOP_AT = int(sys.argv[sys.argv.index("--stop-at-M") + 1]) if "--stop-at-M" in sys.argv[10:] else None  # P4
STOPPED_AT = [None]
STEM = "CANDIDATE_TEST_M" if test_after is not None else "CANDIDATE_M"
utc_us = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
ENG = [None]  # the engine Popen, set in __main__
def engine_procs():
    p = ENG[0]
    if p is None or p.poll() is not None: return []
    try:
        ep = psutil.Process(p.pid); return [ep] + ep.children(recursive=True)
    except psutil.Error: return []
def cpu_s(procs):
    t = 0.0
    for q in procs:
        try: c = q.cpu_times(); t += c.user + c.system
        except psutil.Error: pass
    return t
def thr_times(procs):  # per-thread (user, system) cpu times, keyed "pid:tid"
    r = {}
    for q in procs:
        try:
            for t in q.threads(): r["%d:%d" % (q.pid, t.id)] = (t.user_time, t.system_time)
        except psutil.Error: pass
    return r
def nthreads(procs):
    r = {}
    for q in procs:
        try: r[q.pid] = q.num_threads()
        except psutil.Error as e: r[q.pid] = repr(e)
    return r
CHK_ENV = dict(os.environ, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", NUMBA_NUM_THREADS="1")
WATCHDOG_S = float(os.environ.get("J7_WATCHDOG_S", "120"))
CUR_CHK = [None]  # the checker Popen currently running (P1)
ABORT = {"code": 0, "why": None}  # fail-closed exit (P1 5, P2 6); FAILED_VALIDATION -> 7 (P3)
FAILED_VALIDATION = [False]
PAUSES = [0]  # number of suspend/check/resume events
POST_RESUME = [None]  # number of engine round lines at the last RESUME_AT; cleared once the engine logs a new round
def round_lines():
    try: return sum(1 for ln in open(prefix + ".log", encoding="utf-8", errors="replace") if pat.match(ln))
    except OSError: return 0
def run_checker(cmd, census):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=CHK_ENV)
    CUR_CHK[0] = p
    def watch():
        try: pp = psutil.Process(p.pid); ts = time.time()
        except psutil.Error: return
        while p.poll() is None:
            try: ct = pp.cpu_times(); census.append((utc_us(), pp.num_threads(), ct.user + ct.system, time.time() - ts))
            except psutil.Error: break
            time.sleep(0.1)
    tw = threading.Thread(target=watch); tw.start()
    out, err = p.communicate(); tw.join(); CUR_CHK[0] = None
    return p.returncode, out, err
def kill_engine(why):
    for q in engine_procs()[::-1]:
        try: q.kill()
        except psutil.Error as e: log("kill pid %d: %r" % (q.pid, e))
    if ENG[0] is not None:
        try: ENG[0].wait(timeout=30)
        except Exception as e: log("engine wait after kill: %r" % e)
    log("ENGINE_KILLED %s (%s)" % (utc_us(), why))
def watchdog_fire():  # P1: fail closed, never resume while a checker may be alive
    ABORT["code"], ABORT["why"] = 5, "watchdog"
    log("WATCHDOG_FIRED %s after %.1f s without CHECK_END: killing checker, engine stays suspended" % (utc_us(), WATCHDOG_S))
    p = CUR_CHK[0]
    if p is not None and p.poll() is None:
        try: p.kill(); p.wait(timeout=30)
        except Exception as e: log("checker kill/wait: %r" % e)
    log("WATCHDOG_CHECKER_GONE %s checker_rc=%s" % (utc_us(), None if p is None else p.poll()))
def sample(p, out, tag):
    try:
        t0 = utc_us(); p.cpu_percent(None); time.sleep(1.0); cp = p.cpu_percent(None)
        out[tag] = {"utc_start": t0, "utc_end": utc_us(), "pid": p.pid, "num_threads": p.num_threads(), "cpu_percent_1s": cp,
                    "status": p.status()}
    except psutil.Error as e: out[tag] = {"error": repr(e)}
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
TOOLS = os.environ.get("J7_TOOLS") or os.path.join(WS, "tools")
n, d, w = 25, 6, 11
utc = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
sha = lambda b: hashlib.sha256(b).hexdigest()
flog = prefix + "_freeze.log"
def log(s):
    line = "%s %s" % (utc(), s); print("j7_run: " + line, flush=True)
    with open(flog, "a", encoding="utf-8") as f: f.write(line + "\n")
START_SET = set(int(x) for x in np.load(start)); SEED_SET = set(int(x) for x in np.load(seednpy))
last = [max(bar - 1, len(START_SET))]
pat = re.compile(r"round (\d+): M=(\d+) gain=-?\d+ applied=\d+ best=(\d+) t=(\d+)s")
def log_best():
    b = None
    try:
        for ln in open(prefix + ".log", encoding="utf-8", errors="replace"):
            m = pat.match(ln)
            if m: b = int(m.group(3))
    except OSError: pass
    return b
def freeze(force=False):
    src = prefix + "_best.npy"
    if force and not os.path.exists(src): src = prefix + "_cur.npy"
    if not os.path.exists(src): return False
    raw = None
    for _ in range(10):
        try:
            raw = open(src, "rb").read(); a = np.load(io.BytesIO(raw)); break
        except Exception as e:  # torn read while the engine rewrites the file
            raw = None; time.sleep(0.3)
    if raw is None: log("freeze: could not read %s" % src); return False
    arr = sorted(int(x) for x in np.unique(a.astype(np.int64))); M = len(arr)
    if not force and (M < bar or M <= last[0]): return False
    base = os.path.join(outdir, STEM + "%d" % M)
    if any(os.path.exists(base + ext) for ext in (".npy", ".txt")):
        log("freeze: %s.* already exists, not overwritten" % base); last[0] = max(last[0], M); return False
    txt = "".join("".join("1" if (x >> j) & 1 else "0" for j in range(n)) + "\n" for x in arr).encode("ascii")
    open(base + ".npy", "wb").write(raw); open(base + ".txt", "wb").write(txt)
    if os.environ.get("J7_TEST_CORRUPT_TXT") == "1": open(base + ".txt", "ab").write(b"0")  # test-only (P2 micro-test)
    rec = {"M": M, "frozen_utc": utc(), "source": src, "npy": base + ".npy", "npy_sha256": sha(raw), "txt": base + ".txt",
           "txt_sha256": sha(txt), "start_word_fraction": round(sum(x in START_SET for x in arr) / M, 4),
           "seed_word_fraction": round(sum(x in SEED_SET for x in arr) / M, 4), "checks": {}}
    try: rec["engine_best_json"] = json.load(open(prefix + "_best.json"))
    except Exception: pass
    rec["forced_test_snapshot"] = bool(force)
    # files are closed above (write() on a temporary handle); re-read from disk and verify the hashes BEFORE any pause
    hv = (sha(open(base + ".npy", "rb").read()) == rec["npy_sha256"], sha(open(base + ".txt", "rb").read()) == rec["txt_sha256"])
    pz = {"HASH_VERIFIED_AT": utc_us(), "hash_verified_npy_txt": hv}
    log("HASH_VERIFIED_AT %s npy_ok=%s txt_ok=%s" % (pz["HASH_VERIFIED_AT"], hv[0], hv[1]))
    if not all(hv):  # P2: no checks on a file whose bytes are not the recorded ones; fail closed
        rec["both_valid"] = False; rec["aborted"] = "hash_mismatch"; rec["pause"] = pz
        json.dump(rec, open(base + "_freeze.json", "w", encoding="utf-8"), indent=1)
        log("HASH_MISMATCH %s: no checks, no success record; aborting job" % base)
        ABORT["code"], ABORT["why"] = 6, "hash_mismatch"; kill_engine("hash_mismatch"); return False
    procs = engine_procs(); pz["engine_pids"] = [q.pid for q in procs]; smp = {}; census = {}
    pz["wrapper_pid"] = os.getpid()
    if procs:
        sample(procs[0], smp, "pre_pause")  # contrast: the running engine, 1 s before the pause
        log("ENGINE_SAMPLE_PRE_PAUSE %s" % json.dumps(smp["pre_pause"]))
    st = {"resumed": False}; lock = threading.Lock()
    def do_resume(tag):
        with lock:
            if st["resumed"]: return
            c1 = cpu_s(procs); t1 = thr_times(procs)  # immediately before resume()
            for q in procs:
                try: q.resume()
                except psutil.Error as e: log("resume pid %d: %r" % (q.pid, e))
            st["resumed"] = True
            pz[tag] = utc_us(); pz["engine_cpu_s_delta_during_pause"] = round(c1 - c0, 6)
            dthr = {k: (round(t1[k][0] - t0t[k][0], 6), round(t1[k][1] - t0t[k][1], 6)) for k in t1 if k in t0t}
            pz["engine_thread_cpu_delta_nonzero"] = {k: v for k, v in dthr.items() if v != (0.0, 0.0)}
            pz["engine_threads_compared"] = len(dthr)
            pz["engine_num_threads_after_resume"] = nthreads(procs)
            log("%s %s" % (tag, pz[tag]))
            log("ENGINE_CPU_TIME_DELTA_DURING_PAUSE process=%.6f s threads_compared=%d threads_with_nonzero_delta=%d %s" % (
                c1 - c0, len(dthr), len(pz["engine_thread_cpu_delta_nonzero"]), json.dumps(pz["engine_thread_cpu_delta_nonzero"])))
            POST_RESUME[0] = round_lines()
    wd = None
    try:
        if procs:
            pz["engine_num_threads_before_suspend"] = nthreads(procs)
            for q in procs: q.suspend()
            PAUSES[0] += 1
            c0 = cpu_s(procs); t0t = thr_times(procs)  # immediately after suspend() returned
            pz["PAUSE_AT"] = utc_us(); pz["status_after_suspend"] = [q.status() for q in procs]
            pz["engine_num_threads_suspended"] = nthreads(procs)
            log("PAUSE_AT %s engine pids %s status %s num_threads before %s / suspended %s; wrapper pid %d threads %d" % (
                pz["PAUSE_AT"], pz["engine_pids"], pz["status_after_suspend"], pz["engine_num_threads_before_suspend"],
                pz["engine_num_threads_suspended"], os.getpid(), psutil.Process().num_threads()))
            wd = threading.Timer(WATCHDOG_S, watchdog_fire)
            wd.daemon = True; wd.start()
        else:
            log("ENGINE_NOT_RUNNING at %s: no pause needed" % utc_us())
        pz["CHECK_START"] = utc_us(); log("CHECK_START %s" % pz["CHECK_START"])
        th = threading.Thread(target=sample, args=(procs[0], smp, "during_check")) if procs else None
        if th: th.start()
        for c in ("cwcheck_int", "cwcheck_set"):
            if ABORT["code"]: break
            t0 = utc(); census[c] = []
            rc, out, err = run_checker([sys.executable, "-X", "utf8", os.path.join(TOOLS, c + ".py"), base + ".txt", str(n), str(d), str(w)],
                                       census[c])
            open(base + "_%s.json" % c, "w", encoding="utf-8").write(out)
            try: js = json.loads(out.strip().splitlines()[-1])
            except Exception: js = {"raw": out[-300:], "err": err[-300:]}
            rec["checks"][c] = {"rc": rc, "start": t0, "end": utc(), "json_sha256": sha(out.encode()), "result": js}
            nt = [x[1] for x in census[c]]
            eff = round(census[c][-1][2] / census[c][-1][3], 3) if census[c] and census[c][-1][3] > 0 else None
            log("CHECKER_THREADS %s samples=%d os_num_threads_min=%s max=%s last_cpu_s=%s wall_s=%s effective_cpus=%s (env *_NUM_THREADS=1)" % (
                c, len(nt), min(nt) if nt else None, max(nt) if nt else None, round(census[c][-1][2], 3) if nt else None,
                round(census[c][-1][3], 3) if nt else None, eff))
        pz["CHECK_END"] = utc_us(); log("CHECK_END %s" % pz["CHECK_END"])
        if th:
            th.join(); log("ENGINE_SAMPLE %s" % json.dumps(smp.get("during_check")))
    finally:
        if wd is not None: wd.cancel()
        if ABORT["code"] == 5:  # P1: never resume; the checker is already gone (watchdog_fire waited for it)
            p = CUR_CHK[0]
            if p is not None and p.poll() is None:
                p.kill(); p.wait(timeout=30)
            kill_engine("watchdog")
        elif procs: do_resume("RESUME_AT")
    if ABORT["code"] == 5:
        rec["both_valid"] = False; rec["aborted"] = "watchdog"; rec["pause"] = pz
        json.dump(rec, open(base + "_freeze.json", "w", encoding="utf-8"), indent=1)
        log("ABORTED_SNAPSHOT %s (watchdog): no success record" % base); return False
    pz["samples"] = smp; pz["checker_thread_census"] = census; pz["watchdog_s"] = WATCHDOG_S; rec["pause"] = pz
    rec["both_valid"] = len(rec["checks"]) == 2 and all(v["rc"] == 0 and v["result"].get("valid") is True for v in rec["checks"].values())
    if not rec["both_valid"]: FAILED_VALIDATION[0] = True; log("FAILED_VALIDATION snapshot %s" % base)
    json.dump(rec, open(base + "_freeze.json", "w", encoding="utf-8"), indent=1)
    log("FROZE%s M=%d txt sha256 %s npy sha256 %s both_valid=%s" % (" (FORCED TEST SNAPSHOT)" if force else "", M, rec["txt_sha256"],
                                                                rec["npy_sha256"], rec["both_valid"]))
    last[0] = max(last[0], M)
    if STOP_AT is not None and rec["both_valid"] and M >= STOP_AT and STOPPED_AT[0] is None:  # P4
        STOPPED_AT[0] = M; log("STOP_AT_M reached M=%d >= %d at %s: stopping the engine" % (M, STOP_AT, utc_us())); kill_engine("stop_at_M")
    return True
if __name__ == "__main__":
    now = datetime.datetime.now(datetime.timezone.utc)
    if now >= datetime.datetime.strptime(cutoff, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc):
        print("j5_run: %s >= cutoff %s, NOT started" % (utc(), cutoff), flush=True); sys.exit(3)
    log("start (cutoff %s) bar %d start M %d pid %d" % (cutoff, bar, len(START_SET), os.getpid()))
    eng_p = subprocess.Popen([sys.executable, "-X", "utf8", eng, start, str(n), str(d), str(w), prefix, "--seconds", secs,
                              "--rounds", "1000000", "--seed", seed])
    ENG[0] = eng_p; t_eng = time.time(); forced = False
    log("engine pid %d%s" % (eng_p.pid, "" if test_after is None else " (test: forced snapshot after %.0f s; names %s<M>)" % (test_after, STEM)))
    while eng_p.poll() is None and not ABORT["code"]:
        b = log_best()
        if b is not None and b >= bar and b > last[0]: freeze()
        if test_after is not None and not forced and time.time() - t_eng >= test_after and eng_p.poll() is None:
            forced = True; ok = freeze(force=True)  # one attempt only
            log("TEST_SNAPSHOT forced attempt wrote_new_files=%s (pause events so far %d)" % (ok, PAUSES[0]))
        if POST_RESUME[0] is not None:
            k = round_lines()
            if k > POST_RESUME[0]:
                last_ln = [ln.strip() for ln in open(prefix + ".log", encoding="utf-8", errors="replace") if pat.match(ln)][-1]
                log("POST_RESUME_PROGRESS %s engine round lines %d -> %d; latest: %s" % (utc_us(), POST_RESUME[0], k, last_ln))
                POST_RESUME[0] = None
        time.sleep(2)
    if ABORT["code"]:
        kill_engine(ABORT["why"]); log("JOB_ABORTED code=%d why=%s (fail closed; no post-check, no success exit)" % (ABORT["code"], ABORT["why"]))
        sys.exit(ABORT["code"])
    rc = eng_p.returncode
    if STOPPED_AT[0] is not None: log("engine stopped by --stop-at-M (engine rc %s not used)" % rc); rc = 0
    log("PAUSE_EVENTS %d during the engine run" % PAUSES[0])
    if test_after is not None and PAUSES[0] == 0: log("TEST_SNAPSHOT_NOT_EXERCISED: no pause/check/resume happened while the engine ran")
    log("engine exited rc=%s; final freeze attempt and post-check" % rc)
    freeze()
    p = subprocess.run([sys.executable, "-X", "utf8", os.environ.get("J7_POSTCHECK") or os.path.join(HERE, "post_check.py"), prefix, seednpy, prefix + "_post_check.json"],
                       capture_output=True, text=True)
    log("post_check rc=%d %s" % (p.returncode, p.stdout.strip()[-400:]))
    try: pc_ok = p.returncode == 0 and json.load(open(prefix + "_post_check.json", encoding="utf-8")).get("both_valid") is True
    except Exception as e: pc_ok = False; log("post_check json unreadable: %r" % e)
    if not pc_ok: FAILED_VALIDATION[0] = True; log("FAILED_VALIDATION post_check")
    rows = []
    try:
        for ln in open(prefix + ".log", encoding="utf-8", errors="replace"):
            m = re.match(r"round (\d+): M=(\d+) gain=(-?\d+) applied=(\d+) best=(\d+) t=(\d+)s", ln)
            if m: rows.append(m.groups())
    except OSError: pass
    with open(prefix + "_curve.csv", "w", encoding="utf-8") as f:
        f.write("round,M,gain,applied,best,t_s\n"); f.writelines(",".join(r) + "\n" for r in rows)
    fin = prefix + "_best.npy" if os.path.exists(prefix + "_best.npy") else prefix + "_cur.npy"
    try:
        fa = set(int(x) for x in np.load(fin))
        summ = {"final_file": fin, "M": len(fa), "kept_from_start": len(fa & START_SET), "frac_kept_from_start": round(len(fa & START_SET) / len(fa), 4),
                "kept_from_seed": len(fa & SEED_SET), "frac_kept_from_seed": round(len(fa & SEED_SET) / len(fa), 4),
                "rounds": len(rows), "last_t_s": int(rows[-1][5]) if rows else None, "best": max((int(r[4]) for r in rows), default=None),
                "rounds_applied_gt0": sum(1 for r in rows if int(r[3]) > 0), "utc": utc()}
        json.dump(summ, open(prefix + "_summary.json", "w"), indent=1); log("summary %s" % json.dumps(summ))
    except Exception as e:
        log("summary failed: %r" % e)
    if FAILED_VALIDATION[0]:
        log("JOB_EXIT 7 (validation failed; engine rc was %s)" % rc); sys.exit(7)
    sys.exit(rc)
