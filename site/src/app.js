/* V3R1T4S site. Renders data.json (built from the repo by site/build.py) over the server-rendered snapshot.
   Every string in data.json comes from contributor-controlled files, so: text goes in with textContent only (never
   innerHTML), every string is length-capped, and every link is built here from a fixed GitHub prefix plus ids that
   must match strict patterns. data.json carries no URLs. Storage: localStorage v3r1t4s-theme and v3r1t4s-keys only. */
(function () {
  'use strict';
  var GH = 'https://github.com/elder-plinius/V3R1T4S';
  var SLUG = /^[a-z0-9][a-z0-9-]{0,99}$/;
  var PKG_SRC = '\\d{4}-\\d{2}-\\d{2}-[A-Za-z0-9][A-Za-z0-9_.-]{0,63}-[0-9a-f]{8}';
  var PKG = new RegExp('^' + PKG_SRC + '$');
  var DAY = /^(\d{4})-(\d{2})-(\d{2})$/;
  var CREDIT = /^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$/;
  var ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
  var KIND = /^[a-z]{1,12}$/;
  var SAFE_URL = /^https:\/\/github\.com\/elder-plinius\/V3R1T4S\/[A-Za-z0-9._~\/?=&%-]*$/;
  var H_U = /^#u-([a-z0-9][a-z0-9-]{0,99})$/, H_D = new RegExp('^#d-(' + PKG_SRC + ')$'), H_W = /^#w-(\d{4}-\d{2}-\d{2})$/;
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var MARK = Object.assign(Object.create(null), { o: ['✅', "Officially listed: the table's owner has added it"], v: ['🧪', 'Checked by us, not yet on the official table'] });
  /* display labels only: URL values (cp=min, kind=harvest) and data.json keep the raw words (build.py CB_LABEL, KIND_LABEL) */
  var CB = [['min', 'minutes on a laptop'], ['hours', 'hours on a laptop'], ['days', 'days on a laptop'], ['cluster', 'needs a cluster'], ['thought', 'pen and paper']];
  /* lookup tables keyed by repo or URL strings have no prototype, so 'constructor' or '__proto__' never match */
  function dict() { return Object.create(null); }
  var CB_LABEL = dict(); CB.forEach(function (c) { CB_LABEL[c[0]] = c[1]; });
  var KIND_L = Object.assign(dict(), { harvest: 'within reach' });
  function kindLabel(k) { return KIND_L[k] || k; }
  var PLAIN_MAX = 110;
  var FEED_STEP = 12;
  var KU_STEP = window.matchMedia && matchMedia('(min-width: 960px)').matches ? 24 : 12;
  var SUGGEST = GH + '/issues/new?template=suggest-known-unknown.yml';
  var RM = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var MAC = /Mac|iP(hone|ad|od)/.test(navigator.platform || navigator.userAgent || '');

  function $(s) { return document.querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function str(x, n) { x = (x == null ? '' : String(x)); return x.length > n ? x.slice(0, n - 1) + '…' : x; }
  function int(x) { return typeof x === 'number' && isFinite(x) && x >= 0 && x < 1e9 ? Math.floor(x) : null; }
  function fmt(n) { return Number(n).toLocaleString('en-US'); }
  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }
  function link(url, cls, txt) {
    var a = el('a', cls, txt);
    if (SAFE_URL.test(url)) a.href = url;
    return a;
  }
  function enc(s) {
    return encodeURIComponent(s).replace(/[!'()*]/g, function (c) { return '%' + c.charCodeAt(0).toString(16).toUpperCase(); });
  }
  function emoji(x) {
    x = str(x, 16);
    return /^(?:[©®‼-㊙️‍]|[\ud83c-\ud83e][\udc00-\udfff])+$/.test(x) ? x : '◆';
  }
  function dayLabel(d, year) {
    var m = DAY.exec(d);
    var mon = m && MONTHS[+m[2] - 1];
    if (!mon || +m[3] < 1 || +m[3] > 31) return d;
    return mon + ' ' + (+m[3]) + (year === false ? '' : ', ' + m[1]);
  }
  function utcDays(d) { var m = DAY.exec(d); return m ? Date.UTC(+m[1], +m[2] - 1, +m[3]) / 864e5 : null; }
  /* merge days are UTC days, so "today" is the UTC calendar day: never a "Tomorrow" */
  function relDay(d) {
    var now = new Date(), t = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()) / 864e5;
    var x = utcDays(d), n = x == null ? -1 : Math.round(t - x);
    return n === 0 ? 'Today' : n === 1 ? 'Yesterday' : n > 1 && n < 7 ? n + ' days ago' : dayLabel(d);
  }
  function ago(iso) {
    var s = (Date.now() - Date.parse(iso)) / 1000;
    if (!(s >= 0)) return null;
    if (s < 90) return 'just now';
    if (s < 3600) return Math.round(s / 60) + ' min ago';
    if (s < 86400 * 2) return Math.round(s / 3600) + 'h ago';
    return Math.round(s / 86400) + ' days ago';
  }
  function say(region, msg) { var r = $(region); if (r) { r.textContent = ''; setTimeout(function () { r.textContent = msg; }, 30); } }
  function keysOn() { try { return localStorage.getItem('v3r1t4s-keys') !== 'off'; } catch (e) { return true; } }

  /* ---------------- M1: one copy helper */
  var JOIN = '';
  function copyText(text, btn, okLabel, srMsg, what) {
    var lab = btn.querySelector('.lab') || btn;
    if (btn._lab == null) btn._lab = lab.textContent;
    function done(ok) {
      clearTimeout(btn._t);
      lab.textContent = ok ? (okLabel || 'Copied ✓') : 'Select';
      btn.classList.toggle('ok', ok);
      $('#live').textContent = ok ? (srMsg || 'Copied to clipboard') : (MAC ? 'Press ⌘C to copy' : 'Press Ctrl+C to copy');
      if (!ok) {
        var src = btn.getAttribute('data-src') && document.getElementById(btn.getAttribute('data-src'));
        if (src) {
          var s = window.getSelection(), r = document.createRange();
          r.selectNodeContents(src); s.removeAllRanges(); s.addRange(r);
        } else {
          var fb = $('#copy-fb'); fb.value = text; fb.hidden = false; fb.focus(); fb.select();
        }
      }
      btn._t = setTimeout(function () {
        lab.textContent = btn._lab; btn.classList.remove('ok'); $('#live').textContent = '';
      }, 1800);
      if (ok) document.dispatchEvent(new CustomEvent('v3:copied', { detail: { what: what || 'link', btn: btn } }));
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
    else done(false);
  }
  function copyJoin(btn) { copyText(JOIN, btn || $('#copy'), null, 'Setup line copied', 'join'); }

  /* ---------------- state */
  var feed = [], feedShown = FEED_STEP, feedBy = null, feedView = [];
  var ku = [], kuById = dict(), cats = dict(), catList = [], kinds = [], kuHits = [], kuShown = KU_STEP;
  var kuCat = null, kuKind = null, kuCp = null, words = [], lastRoll = null, loaded = false;
  var famPlain = dict(), catPlain = dict();

  function qv() { return str($('#q').value.trim(), 100); }

  /* ---------------- M5: filter state in the query string */
  function readState() {
    var p;
    try { p = new URLSearchParams(location.search); } catch (e) { return; }
    $('#q').value = str((p.get('q') || '').trim(), 100);
    var c = p.get('cat'), k = p.get('kind'), b = p.get('cp'), by = p.get('by');
    kuCat = c && SLUG.test(c) && cats[c] ? c : null;
    kuKind = k && kinds.indexOf(k) !== -1 ? k : null;
    kuCp = b && CB_LABEL[b] ? b : null;
    feedBy = by && CREDIT.test(by) && feed.some(function (x) { return x.c === by; }) ? by : null;
  }
  function itemShown(h) {
    var m;
    if ((m = H_U.exec(h))) return kuHits.some(function (k) { return k.id === m[1]; });
    if ((m = H_D.exec(h))) return feedView.some(function (x) { return x.k === m[1]; });
    return true;
  }
  function stateUrl() {
    var p = [], q = qv();
    if (q) p.push('q=' + enc(q));
    if (kuCat) p.push('cat=' + kuCat);
    if (kuKind) p.push('kind=' + kuKind);
    if (kuCp) p.push('cp=' + kuCp);
    if (feedBy) p.push('by=' + enc(feedBy));
    var h = location.hash && itemShown(location.hash) ? location.hash : '';
    return location.pathname + (p.length ? '?' + p.join('&') : '') + h;
  }
  function writeState(push) {
    var url = stateUrl();
    if (url === location.pathname + location.search + location.hash) return;
    try { history[push ? 'pushState' : 'replaceState'](history.state, '', url); } catch (e) {}
  }
  /* M8: remember scroll and "show more" depth in history.state, URL untouched */
  function saveHist(patch) {
    try { history.replaceState(Object.assign({}, history.state || {}, patch), ''); } catch (e) {}
  }

  /* ---------------- daily discoveries */
  function permalink(hash, title) {
    var a = el('a', 'pl', '#');
    a.href = hash;
    a.setAttribute('aria-label', 'Link to: ' + str(title, 60));
    a.title = 'Copy a link to this';
    return a;
  }

  /* blurb: the family's plain-English line, shown on the first item of a run of one family (renderFeed) */
  function feedItem(x, blurb) {
    var li = el('li', 'it');
    if (PKG.test(x.k)) li.id = 'd-' + x.k;
    var e = el('span', 'e', emoji(x.e)); e.setAttribute('aria-hidden', 'true');
    var b = el('div', 'b');
    var ok = SLUG.test(x.f) && PKG.test(x.k);
    b.appendChild(ok ? link(GH + '/tree/main/known-knowns/' + x.f + '/' + x.k, 't', str(x.t, 140)) : el('span', 't', str(x.t, 140)));
    if (blurb) b.appendChild(el('p', 'fam', blurb));
    var meta = el('div', 'meta');
    var mk = MARK[x.s] || MARK.v;
    var st = el('span', 'badge st' + (x.s === 'o' ? ' o' : ''), mk[0]);
    st.setAttribute('role', 'img'); st.setAttribute('aria-label', mk[1]); st.title = mk[1];
    meta.appendChild(st);
    if (x.m) { var mg = el('span', 'badge mg', str(x.m, 60)); mg.title = 'The new value and the previous best'; meta.appendChild(mg); }
    if (CREDIT.test(x.c)) meta.appendChild(el('span', 'cr', 'by ' + x.c));
    if (ok) meta.appendChild(permalink('#d-' + x.k, x.t));
    b.appendChild(meta);
    li.appendChild(e); li.appendChild(b);
    return li;
  }

  function renderFeed() {
    var box = $('#feed'); box.textContent = '';
    feedView = feedBy ? feed.filter(function (x) { return x.c === feedBy; }) : feed;
    var by = $('#feed-by');
    by.textContent = '';
    by.hidden = !feedBy;
    if (feedBy) {
      by.appendChild(document.createTextNode('Showing ' + fmt(feedView.length) + ' discover' + (feedView.length === 1 ? 'y' : 'ies') + ' by '));
      by.appendChild(el('b', null, feedBy));
      var x = el('button', 'x', '✕'); x.type = 'button'; x.setAttribute('aria-label', 'Show everyone');
      x.addEventListener('click', function () { setBy(null); });
      by.appendChild(x);
    }
    if (!feedView.length) {
      var p = el('p', 'empty panel', 'No discoveries yet. Be the first: ');
      var c = el('button', 'mini', 'Copy line'); c.type = 'button';
      c.addEventListener('click', function () { copyJoin(c); });
      p.appendChild(c); box.appendChild(p);
    }
    var group = null, last = null, lastF = null, perDay = dict();
    feedView.forEach(function (x) { perDay[x.d] = (perDay[x.d] || 0) + 1; });
    feedView.slice(0, feedShown).forEach(function (x) {
      if (x.d !== last) {
        last = x.d; lastF = null;
        var sec = el('section', 'day');
        var head = el('div', 'day-h');
        var h3 = el('h3');
        var t = el('time', null, relDay(x.d));
        t.setAttribute('datetime', x.d); t.title = 'Added ' + dayLabel(x.d) + ' (UTC)';
        h3.appendChild(t); head.appendChild(h3);
        var n = el('span', 'day-n', fmt(perDay[x.d])); n.setAttribute('aria-hidden', 'true');
        head.appendChild(n);
        sec.appendChild(head);
        group = el('ol'); sec.appendChild(group); box.appendChild(sec);
      }
      group.appendChild(feedItem(x, x.f !== lastF ? famPlain[x.f] : null));
      lastF = x.f;
    });
    var more = $('#feed-more'), left = feedView.length - feedShown;
    more.hidden = left <= 0;
    more.textContent = 'Show more (' + fmt(Math.max(left, 0)) + ')';
  }

  function setBy(c, focus) {
    feedBy = c && CREDIT.test(c) ? c : null;
    feedShown = FEED_STEP;
    renderFeed(); syncBoard(); writeState(true);
    if (feedBy) say('#live', 'Showing ' + fmt(feedView.length) + ' discoveries by ' + feedBy);
    if (focus !== false) {
      var h = $('#feed-h');
      h.scrollIntoView({ block: 'start', behavior: RM.matches ? 'auto' : 'smooth' });
      h.focus({ preventScroll: true });
    }
  }

  /* ---------------- leaderboard (S2: a name filters the feed) */
  function renderBoard(rows) {
    var bo = $('#board'); bo.textContent = '';
    rows = rows.slice(0, 10).filter(function (r) { return r && CREDIT.test(r.c) && int(r.n) != null; });
    var max = 1;
    rows.forEach(function (r) { if (r.n > max) max = r.n; });
    rows.forEach(function (r) {
      var i = bo.children.length;
      var li = el('li', i === 0 ? 'top1' : i < 3 ? 'top3' : null);
      li.classList.add('w' + Math.max(5, Math.min(100, Math.round(20 * r.n / max) * 5)));
      if (i >= 5) li.classList.add('x');
      li.appendChild(el('span', 'r', String(i + 1)));
      var has = feed.some(function (x) { return x.c === r.c; });
      var n = el(has ? 'button' : 'span', 'n', r.c); n.title = has ? 'Show ' + r.c + "'s discoveries" : r.c;
      if (has) {
        n.type = 'button'; n.setAttribute('data-c', r.c); n.setAttribute('aria-pressed', 'false');
        n.addEventListener('click', function () { setBy(feedBy === r.c ? null : r.c); });
      }
      li.appendChild(n);
      var c = el('span', 'c', fmt(r.n)); c.appendChild(el('span', 'sr-only', r.n === 1 ? ' result' : ' results'));
      li.appendChild(c);
      bo.appendChild(li);
    });
    if (!rows.length) bo.appendChild(el('li', 'empty', 'No one on the board yet. Be the first.'));
    /* below 1024px the board sits above the feed, so it starts at the top 5 */
    var k = rows.length, bm = $('#board-more');
    bm.hidden = k <= 5;
    bm.textContent = 'Show all ' + fmt(k);
    bo.classList.remove('all'); bm.setAttribute('aria-expanded', 'false');
    syncBoard();
  }
  function syncBoard() {
    $$('#board button.n').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-c') === feedBy)); });
  }

  /* ---------------- known unknowns */
  function matchQ(k) {
    for (var i = 0; i < words.length; i++) if (k._hay.indexOf(words[i]) === -1) return false;
    return true;
  }
  function kuFilter() {
    words = qv().toLowerCase().split(/\s+/).filter(Boolean).slice(0, 8).map(function (w) { return w.slice(0, 30); });
    var byCat = dict(), byKind = dict(), byCp = dict(), all = 0;
    kuHits = [];
    ku.forEach(function (k) {
      if (!matchQ(k)) return;
      var c = !kuCat || k.cat === kuCat, d = !kuKind || k.k === kuKind, p = !kuCp || k.cb === kuCp;
      if (d && p) { byCat[k.cat] = (byCat[k.cat] || 0) + 1; all++; }
      if (c && p && k.k) byKind[k.k] = (byKind[k.k] || 0) + 1;
      if (c && d && k.cb) byCp[k.cb] = (byCp[k.cb] || 0) + 1;
      if (c && d && p) kuHits.push(k);
    });
    function setN(b, n) { var s = b.querySelector('.k'); if (s) s.textContent = fmt(n); if (n) b.removeAttribute('data-zero'); else b.setAttribute('data-zero', ''); }
    $$('#chips .chip').forEach(function (b) { var id = b.getAttribute('data-cat'); setN(b, id ? byCat[id] || 0 : all); });
    $$('#eff-kind .chip').forEach(function (b) { setN(b, byKind[b.getAttribute('data-kind')] || 0); });
    $$('#eff-cp .chip').forEach(function (b) { setN(b, byCp[b.getAttribute('data-cp')] || 0); });
  }

  /* S3: highlight matched words; no RegExp, so nothing to escape */
  function hl(text, ws) {
    var f = document.createDocumentFragment(), low = text.toLowerCase(), rs = [];
    ws.forEach(function (w) {
      var i = 0;
      while (w && (i = low.indexOf(w, i)) !== -1) { rs.push([i, i + w.length]); i += w.length; }
    });
    rs.sort(function (a, b) { return a[0] - b[0]; });
    var at = 0, cur = null, merged = [];
    rs.forEach(function (r) { if (cur && r[0] <= cur[1]) cur[1] = Math.max(cur[1], r[1]); else { cur = r.slice(); merged.push(cur); } });
    merged.forEach(function (r) {
      if (r[0] > at) f.appendChild(document.createTextNode(text.slice(at, r[0])));
      f.appendChild(el('mark', null, text.slice(r[0], r[1])));
      at = r[1];
    });
    if (at < text.length) f.appendChild(document.createTextNode(text.slice(at)));
    return f;
  }

  function kuItem(k, idx) {
    var c = cats[k.cat] || {};
    var li = el('li'); li.id = 'u-' + k.id;
    var e = el('span', 'e', c.e || '◆'); e.setAttribute('aria-hidden', 'true');
    var b = el('div', 'b');
    var a = link(GH + '/blob/main/known-unknowns/' + k.cat + '/' + k.id + '.md', 'kt');
    a.appendChild(words.length ? hl(k.t, words) : document.createTextNode(k.t));
    b.appendChild(a);
    var meta = el('div', 'meta');
    var cs = el('span', 'cat', c.name || k.cat);
    if (catPlain[k.cat]) cs.title = catPlain[k.cat];
    meta.appendChild(cs);
    if (k.k) meta.appendChild(el('span', 'badge' + (k.k === 'moonshot' ? ' kd-moonshot' : ''), kindLabel(k.k)));
    if (k.cp) meta.appendChild(el('span', 'badge', k.cb ? CB_LABEL[k.cb] : k.cp));
    if (words.length) {
      var t = k.t.toLowerCase();
      if (words.some(function (w) { return t.indexOf(w) === -1 && k.id.indexOf(w) !== -1; })) {
        var code = el('code', 'kid'); code.appendChild(hl(k.id, words)); meta.appendChild(code);
      }
    }
    b.appendChild(meta);
    var acts = el('div', 'acts');
    acts.appendChild(permalink('#u-' + k.id, k.t));
    var h = el('button', 'hunt'); h.type = 'button';
    h.setAttribute('data-i', String(idx));
    h.setAttribute('aria-label', 'Hunt: copy a prompt that sends your agent after ' + str(k.t, 60));
    h.title = 'Copy a prompt that sends your agent after this problem';
    h.appendChild(el('span', 'lab', 'Hunt'));
    acts.appendChild(h);
    li.appendChild(e); li.appendChild(b); li.appendChild(acts);
    return li;
  }

  function renderKu() {
    var ul = $('#kul'); ul.textContent = '';
    kuHits.slice(0, kuShown).forEach(function (k, i) { ul.appendChild(kuItem(k, i)); });
    if (!kuHits.length) ul.appendChild(emptyKu());
    var more = $('#ku-more'), left = kuHits.length - kuShown;
    more.hidden = left <= 0;
    more.textContent = 'Show more (' + fmt(Math.max(left, 0)) + ')';
    var cnt = $('#ku-count'), all = kuHits.length === ku.length;
    cnt.textContent = all ? fmt(ku.length) : fmt(kuHits.length) + ' / ' + fmt(ku.length);
    cnt.classList.toggle('f', !all);
    var r = $('#roll');
    r.disabled = !kuHits.length;
    r.title = kuHits.length ? 'Show a random open problem (Shift+R)' : 'Nothing to pick from: clear the filters';
  }

  /* M9: a zero-result state that offers the next step */
  function emptyKu() {
    var li = el('li', 'empty'), q = qv();
    var p = el('p', null, 'No open problem matches');
    if (q) { p.appendChild(document.createTextNode(' ')); p.appendChild(el('q', null, q)); }
    if (kuCat && cats[kuCat]) p.appendChild(document.createTextNode(' in ' + cats[kuCat].e + ' ' + cats[kuCat].name));
    if (kuKind || kuCp) p.appendChild(document.createTextNode(' with these filters'));
    p.appendChild(document.createTextNode('.'));
    li.appendChild(p);
    var row = el('p', 'acts-row');
    var filtered = kuCat || kuKind || kuCp;
    if (q && filtered) {
      var n = ku.filter(matchQ).length;
      if (n) { var a = el('button', 'mini', 'Search all categories (' + fmt(n) + ')'); a.type = 'button'; a.setAttribute('data-act', 'all'); row.appendChild(a); }
    }
    if (q || filtered) { var c = el('button', 'mini', 'Clear filters'); c.type = 'button'; c.setAttribute('data-act', 'clear'); row.appendChild(c); }
    row.appendChild(link(SUGGEST + (q ? '&title=' + enc(q.slice(0, 80)) : ''), 'mini sug', q ? 'Suggest it as a new problem →' : 'Suggest a problem →'));
    li.appendChild(row);
    return li;
  }

  function updateKu(announce) {
    kuShown = KU_STEP; kuFilter(); renderKu();
    if (announce) $('#ku-live').textContent = fmt(kuHits.length) + ' open problem' + (kuHits.length === 1 ? '' : 's');
  }

  function pressGroup(sel, attr, val) {
    $$(sel).forEach(function (c) { c.setAttribute('aria-pressed', String((c.getAttribute(attr) || null) === val)); });
  }
  function syncChips() {
    pressGroup('#chips .chip', 'data-cat', kuCat);
    pressGroup('#eff-kind .chip', 'data-kind', kuKind);
    pressGroup('#eff-cp .chip', 'data-cp', kuCp);
    /* the selected category's plain-English line, under the chips */
    var cp = $('#cat-p'), t = kuCat && catPlain[kuCat];
    if (cp && cp.textContent !== (t || '')) cp.textContent = t || '';
    if (cp) cp.hidden = !t;
  }
  function chip(label, n, attr, val, onClick, cls) {
    var b = el('button', 'chip' + (cls ? ' ' + cls : ''));
    b.type = 'button';
    b.setAttribute(attr, val || '');
    b.appendChild(document.createTextNode(label));
    b.appendChild(el('span', 'k', fmt(n)));
    b.addEventListener('click', onClick);
    return b;
  }
  function setFilter(kind, val) {
    if (kind === 'cat') kuCat = val;
    else if (kind === 'kind') kuKind = kuKind === val ? null : val;
    else if (kind === 'cp') kuCp = kuCp === val ? null : val;
    syncChips(); updateKu(true); writeState(true);
  }
  function renderChips() {
    var box = $('#chips'); box.textContent = '';
    box.appendChild(chip('All', ku.length, 'data-cat', null, function () { setFilter('cat', null); }));
    catList.forEach(function (c) {
      var b = chip(c.e + ' ' + c.name, c.n, 'data-cat', c.id, function () { setFilter('cat', c.id); });
      if (catPlain[c.id]) b.title = catPlain[c.id];
      box.appendChild(b);
    });
    var kb = $('#eff-kind'), cb = $('#eff-cp'); kb.textContent = ''; cb.textContent = '';
    kinds.forEach(function (k) { kb.appendChild(chip(kindLabel(k), 0, 'data-kind', k, function () { setFilter('kind', k); }, 'sm')); });
    CB.forEach(function (c) {
      if (ku.some(function (k) { return k.cb === c[0]; })) cb.appendChild(chip(c[1], 0, 'data-cp', c[0], function () { setFilter('cp', c[0]); }, 'sm'));
    });
    $('#eff').hidden = !kinds.length && !cb.children.length;
    syncChips();
  }

  /* ---------------- M4: deep links #u-<id>, #d-<package>, #w-<date> */
  function flash(row, center) {
    if (!row) return;
    if (!row.hasAttribute('tabindex')) row.tabIndex = -1;
    row.scrollIntoView({ block: center === false ? 'start' : 'center', behavior: RM.matches ? 'auto' : 'smooth' });
    row.focus({ preventScroll: true });
    row.classList.remove('hit'); void row.offsetWidth; row.classList.add('hit');
    clearTimeout(row._hit); row._hit = setTimeout(function () { row.classList.remove('hit'); }, 1600);
  }
  function focusItem(h) {
    var m, i, row;
    if (!loaded && (H_U.test(h) || H_D.test(h))) {
      row = document.getElementById(h.slice(1));
      if (row) flash(row);
      return !!row;
    }
    if ((m = H_U.exec(h))) {
      var k = kuById[m[1]];
      if (!k) { missing(); return true; }
      if (kuHits.indexOf(k) === -1) { $('#q').value = ''; kuCat = kuKind = kuCp = null; syncChips(); kuFilter(); }
      i = kuHits.indexOf(k);
      kuShown = Math.max(kuShown, Math.ceil((i + 1) / KU_STEP) * KU_STEP);
      renderKu(); writeState(false);
      flash(document.getElementById('u-' + k.id));
      return true;
    }
    if ((m = H_D.exec(h))) {
      if (feedBy && !feedView.some(function (x) { return x.k === m[1]; })) { feedBy = null; syncBoard(); renderFeed(); }
      i = -1;
      feedView.some(function (x, j) { if (x.k === m[1]) { i = j; return true; } return false; });
      if (i < 0) return false;
      feedShown = Math.max(feedShown, Math.ceil((i + 1) / FEED_STEP) * FEED_STEP);
      renderFeed(); writeState(false);
      flash(document.getElementById('d-' + m[1]));
      return true;
    }
    if ((m = H_W.exec(h))) {
      row = document.getElementById('w-' + m[1]);
      if (!row) return false;
      if (row.classList.contains('clip')) { row.classList.remove('clip'); var ab = $('.ed-all', row); if (ab) ab.remove(); }
      for (var p = row; p; p = p.parentElement) if (p.tagName === 'DETAILS') p.open = true;
      flash(row, false);
      return true;
    }
    return false;
  }
  function missing() {
    var ul = $('#kul'), li = el('li', 'empty note');
    li.appendChild(document.createTextNode("That problem isn't on the list any more. It may have been renamed or retired. "));
    li.appendChild(link(GH + '/tree/main/known-unknowns', null, 'Browse on GitHub →'));
    ul.insertBefore(li, ul.firstChild);
    $('#ku-live').textContent = "That problem isn't on the list any more.";
    flash(li);
  }
  function go(hash) {
    try { history.pushState(history.state, '', location.pathname + location.search + hash); } catch (e) {}
    focusItem(hash);
  }

  /* ---------------- M7: roll a random target */
  function roll() {
    if (!kuHits.length) return null;
    var k = kuHits[Math.floor(Math.random() * kuHits.length)];
    if (kuHits.length > 1 && k.id === lastRoll) k = kuHits[Math.floor(Math.random() * kuHits.length)];
    lastRoll = k.id;
    var r = $('#roll');
    if (!RM.matches) { r.classList.remove('spin'); void r.offsetWidth; r.classList.add('spin'); }
    go('#u-' + k.id);
    say('#ku-live', 'Picked: ' + str(k.t, 60));
    return k;
  }
  function hunt(k, btn) {
    if (!k || !SLUG.test(k.id) || !SLUG.test(k.cat)) return false;
    var text = JOIN + ' and hunt known-unknowns/' + k.cat + '/' + k.id + '.md';
    if (btn) copyText(text, btn, 'Copied ✓', 'Prompt copied for ' + str(k.t, 60), 'hunt');
    return text;
  }

  /* ---------------- sections */
  var SEC = Object.assign(dict(), { w: '#wk-h', d: '#feed-h', b: '#lb-h', u: '#ku-h' });
  function goSection(key) {
    var h = typeof key === 'string' && SEC[key] ? $(SEC[key]) : null;
    if (!h) return false;
    if (!h.hasAttribute('tabindex')) h.tabIndex = -1;
    h.scrollIntoView({ block: 'start', behavior: RM.matches ? 'auto' : 'smooth' });
    h.focus({ preventScroll: true });
    return true;
  }

  /* ---------------- V3R1T4S Weekly: on phones, the latest edition shows 3 highlights and a button for the rest */
  function clipWeekly() {
    var ed = $('#weekly article.ed'), n = ed ? $$('.ed-b > li', ed).length : 0;
    if (n <= 4 || !(window.matchMedia && matchMedia('(max-width: 599px)').matches)) return;
    ed.classList.add('clip');
    var b = el('button', 'btn ed-all', 'Show all ' + n + ' highlights'); b.type = 'button';
    b.addEventListener('click', function () {
      ed.classList.remove('clip'); b.remove();
      var li = $$('.ed-b > li', ed)[3]; if (li) { li.tabIndex = -1; li.focus(); }
    });
    ed.appendChild(b);
  }

  /* ---------------- data */
  function load(D) {
    if (!D || D.schema !== 'v3r1t4s-site/2') throw new Error('bad data');
    feed = (Array.isArray(D.feed) ? D.feed : []).filter(function (x) {
      return x && DAY.test(x.d) && typeof x.t === 'string';
    }).slice(0, 20000);
    (Array.isArray(D.cats) ? D.cats : []).forEach(function (c) {
      if (!c || !SLUG.test(c.id) || cats[c.id]) return;
      var o = { id: c.id, name: str(c.name, 40), e: emoji(c.e), n: int(c.n) || 0 };
      cats[c.id] = o; catList.push(o);
    });
    ku = (Array.isArray(D.ku) ? D.ku : []).filter(function (k) {
      return k && SLUG.test(k.id) && SLUG.test(k.cat) && cats[k.cat] && !kuById[k.id] && (kuById[k.id] = true);
    }).slice(0, 20000).map(function (k) {
      var o = { id: k.id, cat: k.cat, t: str(k.t, 180), k: typeof k.k === 'string' && KIND.test(k.k) ? k.k : null,
                cp: k.cp ? str(k.cp, 24) : null, cb: CB_LABEL[k.cb] ? k.cb : null };
      o._hay = [o.t, o.id, cats[k.cat].name, o.k || '', o.k ? kindLabel(o.k) : '', o.cp || '', o.cb ? CB_LABEL[o.cb] : ''].join(' ').toLowerCase();
      kuById[o.id] = o;
      return o;
    });
    ['harvest', 'standard', 'moonshot'].concat(ku.map(function (k) { return k.k; })).forEach(function (k) {
      if (k && kinds.indexOf(k) === -1 && ku.some(function (x) { return x.k === k; })) kinds.push(k);
    });
    catList.sort(function (a, b) { return b.n - a.n || (a.name < b.name ? -1 : 1); });
    /* plain-English blurbs: {f: {family: text}, c: {category: text}}; ids re-checked, text capped, shown as text */
    var P = D.plain && typeof D.plain === 'object' ? D.plain : {};
    [[P.f, famPlain], [P.c, catPlain]].forEach(function (pair) {
      var src = pair[0], dst = pair[1];
      if (!src || typeof src !== 'object' || Array.isArray(src)) return;
      Object.keys(src).slice(0, 2000).forEach(function (id) {
        if (SLUG.test(id) && typeof src[id] === 'string' && src[id]) dst[id] = str(src[id], PLAIN_MAX);
      });
    });

    readState();
    var st = history.state || {}, ok = typeof st.y === 'number';
    if (ok) {
      feedShown = Math.min(Math.max(int(st.fs) || FEED_STEP, FEED_STEP), Math.max(feed.length, FEED_STEP));
    }
    renderFeed();
    renderBoard(Array.isArray(D.board) ? D.board : []);
    renderChips();
    kuFilter();
    if (ok) kuShown = Math.min(Math.max(int(st.ks) || KU_STEP, KU_STEP), 2000);
    renderKu();
    if (typeof D.built === 'string' && ISO.test(D.built)) {
      var b = $('#built'), a = ago(D.built);
      if (b && a) { b.textContent = a; b.title = D.built.replace('T', ' ').replace('Z', ' UTC'); }
    }
    loaded = true;
    $('#roll').hidden = false;
    if (!focusItem(location.hash) && ok) window.scrollTo(0, Math.max(0, int(st.y) || 0));
  }

  /* S1: keep the server-rendered snapshot when data.json cannot be loaded */
  function fail() {
    var box = $('#feed');
    var p = el('p', 'empty panel err', box.querySelector('.it') ? "Couldn't load the latest list, so this is a saved copy. " : "Couldn't load the list. ");
    p.appendChild(link(GH + '/tree/main/known-knowns', null, 'Browse it on GitHub →'));
    box.insertBefore(p, box.firstChild);
  }

  /* ---------------- S4: keyboard shortcuts */
  function editable(t) {
    return t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable);
  }
  function anyFilter() { return !!(kuCat || kuKind || kuCp); }
  function escape() {
    if (feedBy) { setBy(null, false); return true; }
    if (anyFilter()) { kuCat = kuKind = kuCp = null; syncChips(); updateKu(true); writeState(true); return true; }
    if (qv()) { $('#q').value = ''; updateKu(true); writeState(false); return true; }
    return false;
  }

  function boot() {
    JOIN = $('#cmd').textContent.trim();
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
    $('#foot-x').hidden = false;
    clipWeekly();

    $('#feed-more').addEventListener('click', function () {
      var old = feedShown; feedShown += FEED_STEP; renderFeed();
      var rows = $$('#feed .it'); if (rows[old]) { rows[old].tabIndex = -1; rows[old].focus(); }
      say('#live', 'Showing ' + fmt(Math.min(feedShown, feedView.length)) + ' of ' + fmt(feedView.length));
    });
    /* the snapshot hides ranks 6-10 below 1024px only once JS runs (html.js), so offer "Show all" right away */
    var bm0 = $('#board-more'), n0 = $$('#board li').length;
    bm0.hidden = n0 <= 5; bm0.textContent = 'Show all ' + fmt(n0);
    $('#copy').hidden = false; $('#tog').hidden = false;
    $('#board-more').addEventListener('click', function () {
      var bo = $('#board'), open = bo.classList.toggle('all');
      this.setAttribute('aria-expanded', String(open));
      this.textContent = open ? 'Show top 5' : 'Show all ' + fmt(bo.children.length);
    });
    $('#ku-more').addEventListener('click', function () {
      var old = kuShown; kuShown += KU_STEP; renderKu();
      var rows = $$('#kul > li'); if (rows[old]) { rows[old].tabIndex = -1; rows[old].focus(); }
      say('#ku-live', 'Showing ' + fmt(Math.min(kuShown, kuHits.length)) + ' of ' + fmt(kuHits.length));
    });
    var t = null, q = $('#q');
    q.addEventListener('input', function () {
      clearTimeout(t);
      t = setTimeout(function () { updateKu(true); writeState(false); }, 120);
    });
    $('#roll').addEventListener('click', roll);

    /* copy buttons */
    $('#copy').addEventListener('click', function () { copyJoin(this); });
    $('#copy2').addEventListener('click', function () { copyJoin(this); });
    $('#copy-fb').addEventListener('blur', function () { this.hidden = true; });

    /* delegated: hunt, permalinks, empty-state actions */
    $('#kul').addEventListener('click', function (ev) {
      var b = ev.target.closest('button, a.pl');
      if (!b) return;
      if (b.classList.contains('hunt')) { hunt(kuHits[+b.getAttribute('data-i')], b); return; }
      var act = b.getAttribute('data-act');
      if (act === 'all') { kuCat = kuKind = kuCp = null; syncChips(); updateKu(true); writeState(true); q.focus(); return; }
      if (act === 'clear') { q.value = ''; kuCat = kuKind = kuCp = null; syncChips(); updateKu(true); writeState(true); q.focus(); }
    });
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('a.pl');
      if (!a || ev.ctrlKey || ev.metaKey || ev.shiftKey || ev.altKey) return;
      var h = a.getAttribute('href');
      if (!H_U.test(h) && !H_D.test(h) && !H_W.test(h)) return;
      ev.preventDefault();
      go(h);
      copyText(location.origin + location.pathname + h, a, '✓', 'Link copied', 'link');
    });

    /* M2: copy button that follows you; current section in the bar */
    if ('IntersectionObserver' in window) {
      var c2 = $('#copy2');
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { c2.hidden = e.isIntersecting || e.boundingClientRect.top > 0; });
      }).observe($('#join'));
      /* the board is sticky beside the feed on wide screens, so the feed wins when both are in the band */
      var pills = $$('.pills a'), inBand = {}, ORDER = ['feed-sec', 'ku', 'board-sec'];
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { inBand[e.target.id] = e.isIntersecting; });
        var cur = ORDER.filter(function (id) { return inBand[id]; })[0] || null;
        pills.forEach(function (a) {
          if (a.getAttribute('data-sec') === cur) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
        });
      }, { rootMargin: '-45% 0px -50% 0px' });
      ORDER.forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
    }

    /* "/" focuses the search; arrow keys walk the results like a command palette */
    function kuLinks() { return $$('#kul a.kt'); }
    q.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') { var a = kuLinks(); if (a.length) { ev.preventDefault(); a[0].focus(); } }
      else if (ev.key === 'Escape') {
        ev.preventDefault();
        if (q.value) { q.value = ''; updateKu(true); writeState(false); } else q.blur();
      }
    });
    $('#kul').addEventListener('keydown', function (ev) {
      if (ev.key !== 'ArrowDown' && ev.key !== 'ArrowUp') return;
      var a = kuLinks(), i = a.indexOf(document.activeElement);
      if (i < 0) return;
      ev.preventDefault();
      if (ev.key === 'ArrowDown' && i < a.length - 1) a[i + 1].focus();
      else if (ev.key === 'ArrowUp') (i ? a[i - 1] : q).focus();
    });

    /* S4: the shortcut sheet */
    var dlg = $('#keys'), on = $('#keys-on'), opener = null;
    on.checked = keysOn();
    on.addEventListener('change', function () { try { localStorage.setItem('v3r1t4s-keys', on.checked ? 'on' : 'off'); } catch (e) {} });
    function openKeys() {
      if (!dlg.showModal || dlg.open) return;
      opener = document.activeElement; dlg.showModal();
    }
    dlg.addEventListener('close', function () { if (opener && opener.focus) opener.focus(); });
    $('#keys-x').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (ev) { if (ev.target === dlg) dlg.close(); });
    $('#keys-open').addEventListener('click', openKeys);

    var chord = 0;
    document.addEventListener('keydown', function (ev) {
      if (ev.defaultPrevented || ev.ctrlKey || ev.metaKey || ev.altKey || ev.isComposing) return;
      if (editable(ev.target) || document.querySelector('dialog[open]')) return;
      var k = ev.key;
      if (k === 'Escape') { if (escape()) ev.preventDefault(); return; }
      /* WCAG 2.1.4: the off switch covers every printable-key shortcut; the footer "? keys" button stays */
      if (!keysOn() || ev.repeat) return;
      if (k === '/') { ev.preventDefault(); q.focus(); q.select(); return; }
      if (k === '?') { ev.preventDefault(); openKeys(); return; }
      if (chord && Date.now() - chord < 1000) {
        chord = 0;
        if (SEC[k] && goSection(k)) ev.preventDefault();
        return;
      }
      chord = 0;
      if (k === 'g') { chord = Date.now(); return; }
      if (k === 'c') { ev.preventDefault(); copyJoin($('#copy2').hidden ? $('#copy') : $('#copy2')); return; }
      if (k === 'R' && ev.shiftKey) { ev.preventDefault(); roll(); }
    });

    /* M5/M8: history */
    window.addEventListener('popstate', function () {
      if (!loaded) return;
      readState(); syncChips(); syncBoard();
      kuFilter(); renderKu(); renderFeed();
      focusItem(location.hash);
    });
    window.addEventListener('hashchange', function () { if (loaded) focusItem(location.hash); });
    function remember() { if (loaded) saveHist({ y: window.scrollY, fs: feedShown, ks: kuShown }); }
    window.addEventListener('pagehide', remember);
    var st = null;  /* a reload does not always keep a pagehide write, so also save after scrolling settles */
    window.addEventListener('scroll', function () { clearTimeout(st); st = setTimeout(remember, 400); }, { passive: true });
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') remember();
      else if (loaded) $$('#feed time').forEach(function (t) { t.textContent = relDay(t.getAttribute('datetime')); });
    });

    /* theme (graft: dark unless the OS asks for light) */
    var root = document.documentElement, tog = $('#tog');
    function isDark() { var a = root.getAttribute('data-theme'); return a ? a === 'dark' : !matchMedia('(prefers-color-scheme: light)').matches; }
    function sync() { tog.setAttribute('aria-pressed', String(isDark())); }
    function toggleTheme() {
      var n = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', n);
      try { localStorage.setItem('v3r1t4s-theme', n); } catch (e) {}
      sync();
      return n;
    }
    tog.addEventListener('click', toggleTheme);
    sync();

    /* read/act API for eggs.js and term.js: every argument is re-validated here */
    window.V3R1T4S = Object.freeze({
      go: goSection,
      open: function (id) { if (typeof id === 'string' && SLUG.test(id) && kuById[id]) { go('#u-' + id); return kuById[id].t; } return null; },
      search: function (s) { q.value = str(String(s || ''), 100); updateKu(true); writeState(false); return kuHits.length; },
      setCat: function (c) { if (c != null && !(SLUG.test(c) && cats[c])) return false; setFilter('cat', c || null); return true; },
      hits: function () { return kuHits.length; },
      has: function (id) { return typeof id === 'string' && SLUG.test(id) && !!kuById[id]; },
      cats: function () { return catList.map(function (c) { return [c.id, c.n]; }); },
      roll: function () { var k = roll(); return k ? k.t : null; },
      hunt: function (id) { return typeof id === 'string' && SLUG.test(id) && kuById[id] && SLUG.test(kuById[id].cat) ? hunt(kuById[id]) : null; },
      copyJoin: function () { copyJoin(); return JOIN; },
      ids: function (pre) { pre = String(pre || ''); return ku.filter(function (k) { return k.id.indexOf(pre) === 0; }).slice(0, 20).map(function (k) { return k.id; }); },
      counts: function () { return { feed: feed.length, board: $$('#board li').length, ku: ku.length, weekly: $$('.ed').length }; },
      theme: toggleTheme,
      join: function () { return JOIN; }
    });

    if (!window.fetch) { fail(); return; }
    fetch('data.json', { cache: 'no-cache', credentials: 'omit' })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(load)
      .catch(function (e) { if (!loaded) fail(); if (window.console) console.warn('V3R1T4S: ' + e.message); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
