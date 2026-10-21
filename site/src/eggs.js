/* V3R1T4S easter eggs. Decoration only: they never change data, numbers or the setup line, never move focus
   (except the terminal, which you open on purpose), and every one ends by itself or with Esc.
   Delete this file's <script> tag and the site works the same without them.
     liberate  (or ↑↑↓↓←→←→BA)  glitch the banner and decode the tagline into the motto
     pliny                      leet mode on the site's own labels
     `  (or the footer button)  a small terminal (term.js, loaded on first use)
     copying the setup line     ✓ ARMED
   With single-key shortcuts off (the ? sheet), only the footer button and Esc work.                       */
(function () {
  'use strict';
  var RM = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var MOTTO = 'Veritas liberabit nos.';
  var GLYPHS = '░▒▓█⦑⦒/\\13470$#';

  function $(s) { return document.querySelector(s); }
  /* the key sheet's "Single-key shortcuts" switch (WCAG 2.1.4) turns the typed eggs and ` off too */
  function keysOn() { try { return localStorage.getItem('v3r1t4s-keys') !== 'off'; } catch (e) { return true; } }
  function editable(t) { return t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable); }
  var live = document.createElement('p');
  live.className = 'sr-only'; live.id = 'egg-live'; live.setAttribute('aria-live', 'polite');
  document.body.appendChild(live);
  function say(m) { live.textContent = ''; setTimeout(function () { live.textContent = m; }, 30); }

  /* ---------- console greeting (for devs and agents; no counts, they would go stale) */
  try {
    console.log('%c⊰•-•✧•-•-⦑/V\\E/R\\I/T\\A/S\\⦒-•-•✧•-•⊱\nVeritas liberabit nos', 'color:#39ff14;background:#050510;font-family:monospace;padding:4px 8px');
    console.log('Agents and devs: read AGENTS.md (https://github.com/elder-plinius/V3R1T4S/blob/main/AGENTS.md). Data: /data.json, /known-unknowns.txt, /feed.xml. Press ` for a terminal, ? for shortcuts.');
  } catch (e) {}

  /* ---------- E1: liberate (banner glitch + tagline decode) */
  var tag = $('#tag'), banner = $('.banner'), running = false, saved = null, restoreT = null, raf = 0;
  function restoreTag() {
    clearTimeout(restoreT); cancelAnimationFrame(raf);
    if (saved) { tag.textContent = ''; saved.forEach(function (n) { tag.appendChild(n); }); saved = null; }
    tag.classList.remove('motto', 'lit'); banner.classList.remove('lit', 'glitch');
    running = false;
  }
  function liberate() {
    if (!tag || !banner) return;
    if (running) restoreTag();
    running = true;
    saved = Array.prototype.slice.call(tag.childNodes);
    say('Liberated. Veritas liberabit nos.');
    tag.classList.add('motto');
    if (RM.matches) {
      tag.textContent = MOTTO; tag.classList.add('lit'); banner.classList.add('lit');
      setTimeout(function () { banner.classList.remove('lit'); tag.classList.remove('lit'); }, 1200);
    } else {
      banner.classList.remove('glitch'); void banner.getBoundingClientRect(); banner.classList.add('glitch');
      setTimeout(function () { banner.classList.remove('glitch'); }, 320);
      var t0 = performance.now();
      var step = function (now) {
        var p = Math.min(1, (now - t0) / 900), out = '';
        for (var i = 0; i < MOTTO.length; i++) {
          var ch = MOTTO[i];
          out += ch === ' ' || i < p * MOTTO.length ? ch : GLYPHS[(Math.random() * GLYPHS.length) | 0];
        }
        tag.textContent = out;
        if (p < 1) raf = requestAnimationFrame(step); else tag.textContent = MOTTO;
      };
      raf = requestAnimationFrame(step);
    }
    restoreT = setTimeout(restoreTag, 8000);
  }

  /* ---------- E2: pliny (leet labels; screen readers keep the plain words) */
  var LEET = { a: '4', e: '3', i: '1', o: '0', s: '5', t: '7', A: '4', E: '3', I: '1', O: '0', S: '5', T: '7' };
  var leetOn = false, swaps = [], pill = null;
  function leet(on) {
    if (on === leetOn) return;
    leetOn = on;
    if (on) {
      Array.prototype.forEach.call(document.querySelectorAll('[data-leet]'), function (host) {
        Array.prototype.slice.call(host.childNodes).forEach(function (n) {
          if (n.nodeType !== 3 || !n.nodeValue.trim()) return;
          var wrap = document.createElement('span'), sr = document.createElement('span'), lt = document.createElement('span');
          sr.className = 'sr-only'; sr.textContent = n.nodeValue;
          lt.className = 'leet'; lt.setAttribute('aria-hidden', 'true');
          lt.textContent = n.nodeValue.replace(/[aeiostAEIOST]/g, function (c) { return LEET[c]; });
          wrap.appendChild(sr); wrap.appendChild(lt);
          host.replaceChild(wrap, n);
          swaps.push([host, wrap, n]);
        });
      });
      pill = document.createElement('button');
      pill.type = 'button'; pill.className = 'leet-off'; pill.textContent = '1337 · off';
      pill.setAttribute('aria-label', 'Turn leet mode off');
      pill.addEventListener('click', function () { leet(false); });
      document.body.appendChild(pill);
      say('Leet mode on');
    } else {
      if (running) restoreTag();
      swaps.forEach(function (s) { if (s[1].parentNode === s[0]) s[0].replaceChild(s[2], s[1]); });
      swaps = [];
      if (pill) { if (pill === document.activeElement) $('#tog').focus(); pill.remove(); pill = null; }
      say('Leet mode off');
    }
  }

  /* ---------- E4: ✓ ARMED when the setup line is copied */
  document.addEventListener('v3:copied', function (ev) {
    var d = ev.detail || {};
    if (d.what !== 'join' || !d.btn) return;
    var lab = d.btn.querySelector('.lab') || d.btn;
    lab.textContent = '✓ ARMED';
    var box = $('#cmdbox'), hint = $('#hint');
    if (!box) return;
    if (hint) { hint.classList.add('lit'); setTimeout(function () { hint.classList.remove('lit'); }, 1800); }
    if (RM.matches || d.btn.id !== 'copy') {
      box.classList.add('armed'); setTimeout(function () { box.classList.remove('armed'); }, 1000);
      return;
    }
    box.classList.remove('scan'); void box.offsetWidth; box.classList.add('scan');
    setTimeout(function () { box.classList.remove('scan'); }, 600);
    var marks = ['✧', '•', '⊰', '⊱', '✧', '•', '⊰', '⊱'];
    marks.forEach(function (m, i) {
      var s = document.createElement('span');
      s.className = 'spark s' + (i + 1); s.setAttribute('aria-hidden', 'true'); s.textContent = m;
      var kill = function () { if (s.parentNode) s.parentNode.removeChild(s); };
      s.addEventListener('animationend', kill);
      setTimeout(kill, 800);
      box.appendChild(s);
    });
  });

  /* ---------- E6: the terminal, loaded on first use */
  var termState = 0, termOpener = null;
  function openTerm() {
    termOpener = document.activeElement;
    if (window.V3R1T4S_TERM) { window.V3R1T4S_TERM.open(termOpener); return; }
    if (termState) return;
    termState = 1;
    var s = document.createElement('script');
    s.src = 'term.js';
    s.onload = function () { termState = 2; if (window.V3R1T4S_TERM) window.V3R1T4S_TERM.open(termOpener); };
    s.onerror = function () { termState = 0; };
    document.head.appendChild(s);
  }
  var tb = $('#term-open');
  if (tb) tb.addEventListener('click', openTerm);
  window.V3R1T4S_EGGS = Object.freeze({ liberate: liberate, leet: function (on) { leet(on == null ? !leetOn : !!on); return leetOn; } });

  /* ---------- the engine: one listener, a rolling buffer, never preventDefault on typing */
  var buf = '', KONAMI = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'], ki = 0;
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') {
      if (running) restoreTag();
      if (leetOn && !document.querySelector('dialog[open]')) leet(false);
      return;
    }
    if (ev.ctrlKey || ev.metaKey || ev.altKey || ev.repeat || editable(ev.target) || document.querySelector('dialog[open]')) return;
    if (!keysOn()) { buf = ''; ki = 0; return; }
    var k = ev.key;
    if (k === KONAMI[ki] || (k && k.toLowerCase() === KONAMI[ki])) ki++;
    else ki = k === 'ArrowUp' ? (ki === 2 ? 2 : 1) : 0;
    if (ki === KONAMI.length) { ki = 0; liberate(); return; }
    if (k === '`') { ev.preventDefault(); openTerm(); return; }
    if (!k || k.length !== 1) return;
    buf = (buf + k.toLowerCase()).slice(-12);
    if (/liberate$/.test(buf)) { buf = ''; liberate(); }
    else if (/pliny$/.test(buf)) { buf = ''; leet(!leetOn); }
  });
})();
