/* Applies a saved light/dark choice before first paint. Dark is the CSS default; the OS light preference applies
   when nothing is saved. One localStorage key (v3r1t4s-theme), no cookies. Also marks <html class="js"> so CSS that
   only makes sense with app.js (the collapsed leaderboard) never applies to the no-JS snapshot. */
document.documentElement.classList.add('js');
try {
  var t = localStorage.getItem('v3r1t4s-theme');
  if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
} catch (e) {}
