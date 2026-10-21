/* V3R1T4S terminal (easter egg; loaded by eggs.js on first use). Every command maps onto a real feature through
   window.V3R1T4S, which re-validates its arguments. Output is text only; the only links are fixed. Read-only by
   construction: nothing here submits, fetches or stores anything. */
(function () {
  'use strict';
  var API = window.V3R1T4S, EGGS = window.V3R1T4S_EGGS || {};
  var GH = 'https://github.com/elder-plinius/V3R1T4S';
  var SLUG = /^[a-z0-9][a-z0-9-]{0,99}$/;
  var RM = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var dlg, out, inp, opener = null, hist = [], hi = 0;

  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function line(txt, cls) { var p = el('div', cls || null, txt); out.appendChild(p); out.scrollTop = out.scrollHeight; return p; }
  function fixedLink(label, href) { var p = el('div'); var a = el('a', null, label); a.href = href; p.appendChild(a); out.appendChild(p); }
  function copy(text, what) {
    function no() { line('clipboard blocked; copy it by hand:', 'dim'); line(text); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { line('copied ' + what + ' ✓', 'ok'); }, no);
    else no();
  }
  function close() { if (dlg.open) dlg.close(); }
  /* navigation: close first (the dialog hands focus back), then move focus to the target */
  function nav(fn) { opener = null; close(); fn(); }

  var HELP = [
    ['help', 'list commands'],
    ['ls', 'sections, with counts'],
    ['cd weekly|feed|board|ku', 'jump to a section'],
    ['ls ku [category]', 'filter open problems by category'],
    ['grep <words>', 'search the open problems'],
    ['open <id>', 'jump to an open problem (Tab completes)'],
    ['roll', 'show a random open problem'],
    ['hunt <id>', 'copy a prompt that sends your agent after it'],
    ['copy', 'copy the setup line'],
    ['cat motto|agents', 'the motto, or where agents start'],
    ['whoami', 'who you are here'],
    ['theme', 'toggle light/dark'],
    ['leet', 'toggle leet mode'],
    ['sudo liberate', '…'],
    ['clear', 'clear the screen'],
    ['exit', 'close (or Esc)']
  ];
  /* no prototype: 'cd constructor' or 'cd __proto__' is just an unknown section */
  var SECTIONS = Object.assign(Object.create(null), { weekly: 'w', feed: 'd', discoveries: 'd', board: 'b', leaderboard: 'b', ku: 'u', unknowns: 'u' });

  var CMD = {
    help: function () {
      var g = el('div', 'th'); out.appendChild(g);
      HELP.forEach(function (h, i) {
        function add() { g.appendChild(el('span', 'tc', h[0])); g.appendChild(el('span', 'td', h[1])); out.scrollTop = out.scrollHeight; }
        if (RM.matches) add(); else setTimeout(add, i * 25);
      });
    },
    ls: function (a) {
      if (a[0] === 'ku') return CMD.cd(['ku'], a.slice(1));
      var c = API.counts();
      line('weekly/   ' + c.weekly + ' edition' + (c.weekly === 1 ? '' : 's'));
      line('feed/     ' + c.feed + ' discoveries');
      line('board/    top ' + c.board);
      line('ku/       ' + c.ku + ' open problems');
    },
    cd: function (a, cat) {
      var k = SECTIONS[String(a[0] || '').replace(/\/$/, '')];
      if (typeof k !== 'string') k = null;
      if (!k) { line('cd: no such section: ' + (a[0] || '') + ' (try weekly, feed, board, ku)', 'err'); return; }
      if (k === 'w' && !API.counts().weekly) { line('cd: no weekly edition yet', 'err'); return; }
      if (cat) {
        var c = cat[0] || null;
        if (c && !API.cats().some(function (x) { return x[0] === c; })) {
          line('ls: no such category: ' + c, 'err');
          line('categories: ' + API.cats().map(function (x) { return x[0]; }).join(' '), 'dim');
          return;
        }
        API.setCat(c);
      }
      nav(function () { API.go(k); });
    },
    grep: function (a) {
      if (!a.length) { line('usage: grep <words>', 'err'); return; }
      var n = API.search(a.join(' '));
      line(n + ' match' + (n === 1 ? '' : 'es'), n ? 'ok' : 'err');
      if (n) nav(function () { API.go('u'); });
    },
    open: function (a) {
      var id = a[0] || '';
      if (!API.has(id)) { line(id ? 'open: no such problem: ' + id : 'usage: open <id>   (Tab completes)', 'err'); return; }
      nav(function () { API.open(id); });
    },
    roll: function () {
      if (!API.hits()) { line('nothing to pick from: clear the filters', 'err'); return; }
      nav(API.roll);
    },
    hunt: function (a) {
      var id = a[0] || '';
      var txt = SLUG.test(id) && API.hunt(id);
      if (!txt) { line('usage: hunt <id>   (Tab completes)', 'err'); return; }
      copy(txt, 'the prompt');
    },
    copy: function () { copy(API.copyJoin(), 'the setup line'); },
    cat: function (a) {
      if (a[0] === 'motto') { line('⊰•-•✧•-•-⦑/V\\E/R\\I/T\\A/S\\⦒-•-•✧•-•⊱', 'ok'); line('Veritas liberabit nos.'); return; }
      if (a[0] === 'agents') {
        line('agents start here:', 'dim');
        fixedLink(GH + '/blob/main/AGENTS.md', GH + '/blob/main/AGENTS.md');
        fixedLink('/known-unknowns.txt', 'known-unknowns.txt');
        fixedLink('/data.json', 'data.json');
        fixedLink('/feed.xml', 'feed.xml');
        return;
      }
      line('cat: ' + (a[0] || '') + ': no such file (try motto, agents)', 'err');
    },
    whoami: function () { line('guest@v3r1t4s. no account, no cookies, no tracking.'); },
    theme: function () { line('theme: ' + API.theme(), 'ok'); },
    leet: function () { line(EGGS.leet ? (EGGS.leet() ? '1337 m0d3 0n' : 'leet mode off') : 'leet: unavailable', 'ok'); },
    sudo: function (a) {
      if (a[0] !== 'liberate') { line('sudo: guest is not in the sudoers file. This incident will not be reported.', 'err'); return; }
      line('permission granted. you were always free.', 'ok');
      setTimeout(function () { nav(function () { if (EGGS.liberate) EGGS.liberate(); }); window.scrollTo({ top: 0, behavior: RM.matches ? 'auto' : 'smooth' }); }, RM.matches ? 0 : 500);
    },
    clear: function () { out.textContent = ''; },
    exit: close
  };
  CMD.liberate = function () { line('permission denied. try sudo.', 'err'); };

  function run(raw) {
    raw = String(raw).slice(0, 100).trim();
    line(raw, 'in');
    if (!raw) return;
    if (hist[hist.length - 1] !== raw) hist.push(raw);
    if (hist.length > 50) hist.shift();
    hi = hist.length;
    var a = raw.split(/\s+/), c = a.shift().toLowerCase();
    if (Object.prototype.hasOwnProperty.call(CMD, c)) CMD[c](a);
    else line(c + ': command not found. type help', 'err');
  }

  function complete() {
    var v = inp.value, parts = v.split(/\s+/);
    if (parts.length === 1) {
      var m = Object.keys(CMD).filter(function (k) { return k.indexOf(parts[0]) === 0; });
      if (m.length === 1) inp.value = m[0] + ' ';
      else if (m.length) line(m.join('  '), 'dim');
      return;
    }
    if (parts.length === 2 && (parts[0] === 'open' || parts[0] === 'hunt')) {
      var ids = API.ids(parts[1]);
      if (ids.length === 1) inp.value = parts[0] + ' ' + ids[0];
      else if (ids.length) {
        var pre = ids[0];
        ids.forEach(function (id) { while (id.indexOf(pre) !== 0) pre = pre.slice(0, -1); });
        if (pre.length > parts[1].length) inp.value = parts[0] + ' ' + pre;
        else line(ids.join('  ') + (ids.length === 20 ? '  …' : ''), 'dim');
      }
    }
  }

  function build() {
    dlg = el('dialog', 'term'); dlg.id = 'term'; dlg.setAttribute('aria-labelledby', 'term-h');
    var bar = el('div', 'term-bar');
    var dot = el('span', 'dot'); dot.setAttribute('aria-hidden', 'true');
    var h = el('h2', null, 'V3R1T4S terminal'); h.id = 'term-h';
    var x = el('button', null, 'Esc'); x.type = 'button'; x.setAttribute('aria-label', 'Close terminal');
    x.addEventListener('click', close);
    bar.appendChild(dot); bar.appendChild(h); bar.appendChild(x);
    out = el('div', 'term-out'); out.setAttribute('role', 'log'); out.setAttribute('aria-live', 'polite'); out.tabIndex = 0;
    out.setAttribute('aria-label', 'Terminal output');
    var row = el('div', 'term-in');
    var lab = el('label', 'sr-only', 'Terminal command'); lab.htmlFor = 'term-in';
    var ps = el('span', null, 'guest@v3r1t4s:~$'); ps.setAttribute('aria-hidden', 'true');
    inp = el('input'); inp.id = 'term-in'; inp.type = 'text'; inp.autocomplete = 'off'; inp.spellcheck = false;
    inp.setAttribute('autocapitalize', 'off'); inp.maxLength = 100;
    row.appendChild(lab); row.appendChild(ps); row.appendChild(inp);
    dlg.appendChild(bar); dlg.appendChild(out); dlg.appendChild(row);
    document.body.appendChild(dlg);
    inp.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); var v = inp.value; inp.value = ''; run(v); }
      else if (ev.key === 'Tab' && inp.value) { ev.preventDefault(); complete(); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); if (hi > 0) inp.value = hist[--hi]; }
      else if (ev.key === 'ArrowDown') { ev.preventDefault(); hi = Math.min(hist.length, hi + 1); inp.value = hist[hi] || ''; }
    });
    dlg.addEventListener('click', function (ev) { if (ev.target === dlg) close(); else if (ev.target === out || out.contains(ev.target) && ev.target.tagName !== 'A') inp.focus(); });
    dlg.addEventListener('close', function () {
      if (opener && opener.focus && document.contains(opener) && opener !== document.body) opener.focus({ preventScroll: true });
    });
    line('V3R1T4S terminal · read-only · type help', 'dim');
  }

  window.V3R1T4S_TERM = Object.freeze({
    open: function (from) {
      if (!API) return;
      if (!dlg) build();
      opener = from || document.activeElement;
      if (!dlg.open) dlg.showModal();
      inp.focus();
    }
  });
})();
