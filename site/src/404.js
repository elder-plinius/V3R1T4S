/* 404 page: copy the setup line, and decode "This page is a known unknown." once (static under reduced motion). */
(function () {
  'use strict';
  var RM = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  function $(s) { return document.querySelector(s); }

  var btn = $('#copy'), live = $('#live'), cmd = $('#cmd'), t = null;
  if (btn && cmd) {
    btn.hidden = false;
    btn.addEventListener('click', function () {
      function done(ok) {
        clearTimeout(t);
        btn.textContent = ok ? '✓ ARMED' : 'Select';
        live.textContent = ok ? 'Setup line copied' : 'Press Ctrl+C to copy';
        if (!ok) { var s = window.getSelection(), r = document.createRange(); r.selectNodeContents(cmd); s.removeAllRanges(); s.addRange(r); }
        t = setTimeout(function () { btn.textContent = 'Copy'; live.textContent = ''; }, 1800);
      }
      var text = cmd.textContent.trim();
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
      else done(false);
    });
  }

  var line = $('#nf-line');
  if (!line || RM.matches) return;
  var text = line.textContent, glyphs = '░▒▓█⦑⦒/\\13470', t0 = performance.now();
  function step(now) {
    var p = Math.min(1, (now - t0) / 1100), out = '';
    for (var i = 0; i < text.length; i++) out += text[i] === ' ' || i < p * text.length ? text[i] : glyphs[(Math.random() * glyphs.length) | 0];
    line.textContent = out;
    if (p < 1) requestAnimationFrame(step); else line.textContent = text;
  }
  requestAnimationFrame(step);
})();
