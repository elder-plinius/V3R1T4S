/* V3R1T4S problem thumbnails, drawn in the browser. V3Thumb.make({id, cat, t}) returns a new <svg> (viewBox
   0 0 320 200): one motif family per category, laid out by a seeded generator keyed on the problem id, so the same
   problem gets the same picture on every load and no two problems get the same one. Line art only: colours come
   from CSS classes (style.css, .thumb), so the picture follows the light and dark theme. No images, no network, no
   filters, about 25 elements at most. The only text drawn is a short signature token (an OEIS number, a parameter
   tuple, "n = 37", a contest year such as "ISIC 2018") pulled out of the title with strict patterns; it goes in with textContent. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var SLUG = /^[a-z0-9][a-z0-9-]{0,99}$/;
  var TAU = Math.PI * 2;

  /* ---------------- seeded randomness */
  function hash(s, salt) {
    var h = (2166136261 ^ (salt || 0)) >>> 0;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    h ^= h >>> 16; h = Math.imul(h, 2246822507) >>> 0; h ^= h >>> 13; h = Math.imul(h, 3266489909) >>> 0; h ^= h >>> 16;
    return h >>> 0;
  }
  function mulberry(a) {
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* ---------------- path helpers */
  function f(x) { return String(Math.round(x * 10) / 10); }
  function M(x, y) { return 'M' + f(x) + ' ' + f(y); }
  function L(x, y) { return 'L' + f(x) + ' ' + f(y); }
  function dot(x, y) { return M(x, y) + 'h0'; }                       /* a round-capped zero-length dash */
  function seg(a, b, c, d) { return M(a, b) + L(c, d); }
  function ring(x, y, r) {
    var R = f(r), D = f(2 * r);
    return M(x - r, y) + 'a' + R + ' ' + R + ' 0 1 0 ' + D + ' 0a' + R + ' ' + R + ' 0 1 0 -' + D + ' 0';
  }
  function poly(p, close) {
    var d = '';
    for (var i = 0; i < p.length; i++) d += (i ? L : M)(p[i][0], p[i][1]);
    return d + (close && p.length ? 'Z' : '');
  }
  function smooth(p, close) {                                          /* Catmull-Rom through the points */
    if (p.length < 3) return poly(p, close);
    var n = p.length, d = M(p[0][0], p[0][1]), last = close ? n : n - 1;
    function at(i) { return close ? p[(i + n) % n] : p[Math.max(0, Math.min(n - 1, i))]; }
    for (var i = 0; i < last; i++) {
      var p0 = at(i - 1), p1 = at(i), p2 = at(i + 1), p3 = at(i + 2);
      d += 'C' + f(p1[0] + (p2[0] - p0[0]) / 6) + ' ' + f(p1[1] + (p2[1] - p0[1]) / 6) + ' ' +
        f(p2[0] - (p3[0] - p1[0]) / 6) + ' ' + f(p2[1] - (p3[1] - p1[1]) / 6) + ' ' + f(p2[0]) + ' ' + f(p2[1]);
    }
    return d + (close ? 'Z' : '');
  }
  function sq(x, y, s) { return M(x, y) + 'h' + f(s) + 'v' + f(s) + 'h' + f(-s) + 'z'; }
  function dist(a, b) { return Math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])); }
  function isPrime(n) {
    if (n < 2) return false;
    if (n % 2 === 0) return n === 2;
    for (var d = 3; d * d <= n; d += 2) if (n % d === 0) return false;
    return true;
  }

  /* ---------------- the pen: element factory plus the seeded generator */
  function Pen(svg, r) { this.svg = svg; this.r = r; this.at = svg; }
  var P = Pen.prototype;
  P.u = function (a, b) { return a + (b - a) * this.r(); };
  P.i = function (a, b) { return a + Math.floor((b - a + 1) * this.r()); };
  P.ch = function (p) { return this.r() < p; };
  P.pick = function (a) { return a[Math.floor(this.r() * a.length)]; };
  P.el = function (tag, at, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in at) if (Object.prototype.hasOwnProperty.call(at, k) && at[k] != null) e.setAttribute(k, String(at[k]));
    (parent || this.at).appendChild(e);
    return e;
  };
  P.p = function (d, cls, at) {
    if (!d) return null;
    at = at || {}; at.d = d; at['class'] = at['class'] || cls;
    return this.el('path', at);
  };
  P.c = function (x, y, r, cls, at) {
    at = at || {}; at.cx = f(x); at.cy = f(y); at.r = f(r); at['class'] = cls;
    return this.el('circle', at);
  };
  P.rect = function (x, y, w, h, cls, at, parent) {
    at = at || {}; at.x = f(x); at.y = f(y); at.width = f(w); at.height = f(h); at['class'] = cls;
    return this.el('rect', at, parent);
  };
  P.group = function (tr) { this.at = this.el('g', { transform: tr }); return this.at; };
  P.end = function () { this.at = this.svg; };
  P.scatter = function (n, x0, x1, y0, y1, md) {
    var pts = [], tries = 0;
    while (pts.length < n && tries++ < 800) {
      var p = [this.u(x0, x1), this.u(y0, y1)], ok = true;
      for (var j = 0; j < pts.length && ok; j++) ok = dist(p, pts[j]) >= md;
      if (ok) pts.push(p);
    }
    return pts;
  };
  /* greedy circle packing: bound(x, y) is the largest radius the container allows at (x, y) */
  P.pack = function (bound, rmin, rmax, tries, maxN) {
    var cs = [];
    for (var t = 0; t < tries && cs.length < maxN; t++) {
      var x = this.u(0, 320), y = this.u(0, 200), r = Math.min(rmax, bound(x, y));
      for (var j = 0; j < cs.length && r >= rmin; j++) r = Math.min(r, dist([x, y], cs[j]) - cs[j][2] - 1.5);
      if (r >= rmin) cs.push([x, y, r]);
    }
    return cs;
  };

  function sw(w, o, extra) {
    var a = { 'stroke-width': w };
    if (o != null) a.opacity = o;
    if (extra) for (var k in extra) a[k] = extra[k];
    return a;
  }
  function arrow(x1, y1, x2, y2, h) {
    var a = Math.atan2(y2 - y1, x2 - x1);
    return seg(x1, y1, x2, y2) + M(x2 - h * Math.cos(a - 0.45), y2 - h * Math.sin(a - 0.45)) + L(x2, y2) +
      L(x2 - h * Math.cos(a + 0.45), y2 - h * Math.sin(a + 0.45));
  }
  function axes(B) { B.p('M34 26V172H292', 't-dm', sw(1, 0.8)); B.p(ticks(34, 292, 172, 32, 3), 't-dm', sw(1, 0.6)); }
  function ticks(x0, x1, y, step, h) { var d = ''; for (var x = x0 + step; x <= x1; x += step) d += M(x, y) + 'v' + h; return d; }

  /* scalar field on a grid, and its iso-lines by marching squares */
  function field(B, nb) {
    var bumps = [];
    for (var k = 0; k < nb; k++) bumps.push([B.u(20, 300), B.u(15, 185), B.u(28, 70), B.u(0.5, 1) * (B.ch(0.8) ? 1 : -0.7)]);
    var fx = B.u(0.01, 0.03), fy = B.u(0.01, 0.03), ph = B.u(0, TAU), F = [], lo = 1e9, hi = -1e9, peak = null;
    for (var j = 0; j <= 25; j++) {
      var row = [];
      for (var i = 0; i <= 40; i++) {
        var x = i * 8, y = j * 8, v = 0.18 * Math.sin(x * fx + ph) * Math.cos(y * fy - ph);
        for (k = 0; k < nb; k++) {
          var b = bumps[k], dx = x - b[0], dy = y - b[1];
          v += b[3] * Math.exp(-(dx * dx + dy * dy) / (2 * b[2] * b[2]));
        }
        row.push(v);
        if (v < lo) lo = v;
        if (v > hi) { hi = v; peak = [x, y]; }
      }
      F.push(row);
    }
    return { F: F, lo: lo, hi: hi, peak: peak };
  }
  function iso(F, lev, skip) {
    var d = '';
    for (var j = 0; j < 25; j++) for (var i = 0; i < 40; i++) {
      if (skip && skip(i * 8 + 4, j * 8 + 4)) continue;
      var a = F[j][i], b = F[j][i + 1], c = F[j + 1][i + 1], e = F[j + 1][i];
      var idx = (a > lev ? 8 : 0) | (b > lev ? 4 : 0) | (c > lev ? 2 : 0) | (e > lev ? 1 : 0);
      if (idx === 0 || idx === 15) continue;
      var x = i * 8, y = j * 8;
      var T = [x + 8 * (lev - a) / (b - a), y], R = [x + 8, y + 8 * (lev - b) / (c - b)];
      var Bo = [x + 8 * (lev - e) / (c - e), y + 8], Le = [x, y + 8 * (lev - a) / (e - a)];
      var S = { 1: [Le, Bo], 2: [Bo, R], 3: [Le, R], 4: [T, R], 6: [T, Bo], 7: [Le, T], 8: [Le, T], 9: [T, Bo],
                11: [T, R], 12: [Le, R], 13: [Bo, R], 14: [Le, Bo] }[idx];
      if (idx === 5) d += seg(Le[0], Le[1], T[0], T[1]) + seg(Bo[0], Bo[1], R[0], R[1]);
      else if (idx === 10) d += seg(T[0], T[1], R[0], R[1]) + seg(Le[0], Le[1], Bo[0], Bo[1]);
      else d += seg(S[0][0], S[0][1], S[1][0], S[1][1]);
    }
    return d;
  }

  /* invented glyphs: two or three short strokes on a 3x3 lattice, always with one diagonal and a terminal mark,
     so they read as an unknown script and never as Latin letters or real signs */
  var LAT = [];
  (function () {
    for (var y = 0; y < 3; y++) for (var x = 0; x < 3; x++) {
      if (x < 2) LAT.push([x, y, x + 1, y, 0]);
      if (y < 2) LAT.push([x, y, x, y + 1, 0]);
      if (x < 2 && y < 2) { LAT.push([x, y, x + 1, y + 1, 1]); LAT.push([x + 1, y, x, y + 1, 1]); }
    }
  })();
  /* two diagonals that cross in one cell read as an X, and two that meet at a point as a V or a caret; two parallel
     diagonals joined by a straight stroke read as a lightning zigzag; a diagonal with parallel straight strokes at
     both ends reads as an N or a Z, and one with a horizontal at its top end, over its foot, as a 7 */
  function touch(a, b) {
    return (a[0] === b[0] && a[1] === b[1]) || (a[0] === b[2] && a[1] === b[3]) ||
      (a[2] === b[0] && a[3] === b[1]) || (a[2] === b[2] && a[3] === b[3]);
  }
  function atPt(s, x, y) { return (s[0] === x && s[1] === y) || (s[2] === x && s[3] === y); }
  function latinish(segs) {
    var dg = segs.filter(function (s) { return s[4]; }), st = segs.filter(function (s) { return !s[4]; });
    for (var a = 0; a < dg.length; a++) {
      var p0 = dg[a], top = p0[1] < p0[3] ? [p0[0], p0[1], p0[2]] : [p0[2], p0[3], p0[0]];
      var e0 = st.filter(function (s) { return atPt(s, p0[0], p0[1]); }), e1 = st.filter(function (s) { return atPt(s, p0[2], p0[3]); });
      for (var u = 0; u < e0.length; u++) for (var v = 0; v < e1.length; v++) if ((e0[u][1] === e0[u][3]) === (e1[v][1] === e1[v][3])) return true;
      for (u = 0; u < st.length; u++) {
        var h = st[u];
        if (h[1] === h[3] && h[1] === top[1] && atPt(h, top[0], top[1]) && Math.min(h[0], h[2]) < top[0] === top[2] < top[0]) return true;
      }
      for (var b = a + 1; b < dg.length; b++) {
        var q0 = dg[b];
        if ((p0[2] - p0[0]) * (p0[3] - p0[1]) === (q0[2] - q0[0]) * (q0[3] - q0[1]) &&
            st.some(function (s) { return touch(s, p0) && touch(s, q0); })) return true;
      }
    }
    for (var i = 0; i < dg.length; i++) for (var j = i + 1; j < dg.length; j++) {
      var p = dg[i], q = dg[j];
      if (Math.min(p[0], p[2]) === Math.min(q[0], q[2]) && Math.min(p[1], p[3]) === Math.min(q[1], q[3])) return true;
      var ends = [[p[0], p[1], q[0], q[1]], [p[0], p[1], q[2], q[3]], [p[2], p[3], q[0], q[1]], [p[2], p[3], q[2], q[3]]];
      for (var k = 0; k < 4; k++) if (ends[k][0] === ends[k][2] && ends[k][1] === ends[k][3]) {
        var dp = (p[2] - p[0]) * (p[3] - p[1]), dq = (q[2] - q[0]) * (q[3] - q[1]);
        if (dp !== dq) return true;
      }
    }
    return false;
  }
  function glyph(B, x, y, w, h, curvy) {
    var diag = LAT.filter(function (s) { return s[4]; }), segs, tries = 0;
    do {
      var n = B.i(2, 3), used = {};
      segs = [];
      for (var i = 0; i < n; i++) {
        var s = i ? B.pick(LAT) : B.pick(diag), k = s.join(',');
        if (!used[k]) { used[k] = 1; segs.push(s); }
      }
    } while (latinish(segs) && ++tries < 20);
    /* never keep a shape just rejected: walk the diagonal + stroke pairs from a seeded start to the first clean one */
    if (latinish(segs)) {
      var o = B.i(0, diag.length * LAT.length - 1);
      for (var j = 0; j < diag.length * LAT.length; j++) {
        var c = (o + j) % (diag.length * LAT.length), s1 = diag[Math.floor(c / LAT.length)], s2 = LAT[c % LAT.length];
        if (s1 !== s2 && !latinish([s1, s2])) { segs = [s1, s2]; break; }
      }
    }
    var d = '';
    segs.forEach(function (s) { d += seg(x + s[0] * w / 2, y + s[1] * h / 2, x + s[2] * w / 2, y + s[3] * h / 2); });
    /* half the glyphs end in a short hook, which no Latin capital has */
    if (B.ch(0.5)) {
      var e = segs[segs.length - 1], ex = x + e[2] * w / 2, ey = y + e[3] * h / 2, sx = ex > x + w / 2 ? -1 : 1, sy = ey > y + h / 2 ? -1 : 1;
      d += smooth([[ex, ey], [ex + sx * w * 0.32, ey + sy * h * 0.08], [ex + sx * w * 0.22, ey + sy * h * 0.3]]);
    }
    if (curvy && B.ch(0.6)) {
      var cx = x + B.i(0, 2) * w / 2, cy = y + B.i(0, 2) * h / 2, r = w / 2;
      d += M(cx, cy) + 'a' + f(r) + ' ' + f(r) + ' 0 0 ' + (B.ch(0.5) ? 1 : 0) + ' ' + f(B.ch(0.5) ? r : -r) + ' ' + f(r);
    }
    var tx = x + B.i(0, 2) * w / 2, ty = y + B.pick([0, 2]) * h / 2 + (B.ch(0.5) ? -2.5 : 2.5);
    d += M(tx - 1, ty) + 'h2';
    return d;
  }

  /* ================================================================== motifs */

  /* graphs: a node-link graph (scattered, or a circulant ring) */
  function mGraph(B) {
    var pts, E = [], seen = {}, i;
    function edge(a, b) { var k = a < b ? a + ',' + b : b + ',' + a; if (a !== b && !seen[k]) { seen[k] = 1; E.push([a, b]); } }
    if (B.ch(0.4)) {
      var n = B.i(7, 12), cx = B.u(130, 190), R = B.u(56, 70), ph = B.u(0, TAU), s2 = B.i(2, Math.floor(n / 2));
      pts = [];
      for (i = 0; i < n; i++) pts.push([cx + R * Math.cos(ph + i * TAU / n), 100 + R * Math.sin(ph + i * TAU / n)]);
      for (i = 0; i < n; i++) { edge(i, (i + 1) % n); edge(i, (i + s2) % n); }
    } else {
      pts = B.scatter(B.i(8, 12), 34, 286, 28, 168, 36);
      pts.forEach(function (p, i) {
        var o = pts.map(function (q, j) { return [dist(p, q), j]; }).sort(function (a, b) { return a[0] - b[0]; });
        edge(i, o[1][1]);
        if (B.ch(0.7) && o[2]) edge(i, o[2][1]);
      });
      edge(B.i(0, pts.length - 1), B.i(0, pts.length - 1));
    }
    var d = '', hd = '', hot = B.i(0, pts.length - 1);
    E.forEach(function (e) {
      var s = seg(pts[e[0]][0], pts[e[0]][1], pts[e[1]][0], pts[e[1]][1]);
      if (e[0] === hot || e[1] === hot) hd += s; else d += s;
    });
    B.p(d, 't-ln', sw(1.1, 0.55));
    B.p(hd, 't-gn', sw(1.3, 0.9));
    pts.forEach(function (p, i) { if (i !== hot) B.c(p[0], p[1], 3.6, 't-ho', sw(1.4)); });
    B.c(pts[hot][0], pts[hot][1], 4.6, 't-gf');
    B.c(pts[hot][0], pts[hot][1], 10, 't-gn', sw(1, null, { 'stroke-dasharray': '2 3' }));
  }

  /* automata: an elementary cellular automaton, the next row still unknown */
  function mCA(B) {
    var rule = B.pick([30, 90, 110, 54, 150, 18, 22, 126, 60, 102, 45, 105, 129, 182]);
    var cols = 36, rows = 19, s = 6.5, x0 = 160 - cols * s / 2, y0 = 24, row = [], i, r, d = '';
    for (i = 0; i < cols; i++) row.push(0);
    if (B.ch(0.6)) row[B.i(12, 24)] = 1; else for (i = B.i(2, 4); i > 0; i--) row[B.i(4, cols - 5)] = 1;
    for (r = 0; r < rows; r++) {
      for (i = 0; i < cols; i++) if (row[i]) d += sq(x0 + i * s + 0.6, y0 + r * s + 0.6, s - 1.2);
      var nx = [];
      for (i = 0; i < cols; i++) nx.push((rule >> ((row[(i + cols - 1) % cols] << 2) | (row[i] << 1) | row[(i + 1) % cols])) & 1);
      row = nx;
    }
    B.p(d, 't-lf', { opacity: 0.8 });
    var y = y0 + rows * s + 3;
    B.rect(x0, y, cols * s, s, 't-gh', sw(1, null, { 'stroke-dasharray': '3 2' }));
    B.p(M(x0 - 8, y0) + 'V' + f(y + s) + M(x0 - 11, y + s - 3) + L(x0 - 8, y + s) + L(x0 - 5, y + s - 3), 't-dm', sw(1, 0.7));
  }

  /* number hunts: an Ulam spiral of primes from a seeded start, or a sieve */
  function mSpiral(B) {
    var s0 = B.i(1, 60000), cell = 12, cx = 160 + B.i(-2, 2) * cell, cy = 100, x = 0, y = 0, dx = 1, dy = 0;
    var len = 1, k = 0, turns = 0, pd = '', cd = '', trail = [], last = null;
    for (var n = 0; n < 420; n++) {
      var px = cx + x * cell, py = cy + y * cell;
      if (px > 22 && px < 298 && py > 18 && py < 182) {
        if (isPrime(s0 + n)) { pd += dot(px, py); last = [px, py]; } else cd += dot(px, py);
      }
      if (n < 170) trail.push([px, py]);
      x += dx; y += dy;
      if (++k === len) { k = 0; var t = dx; dx = -dy; dy = t; if (++turns % 2 === 0) len++; }
    }
    B.p(poly(trail), 't-dm', sw(0.8, 0.4));
    B.p(cd, 't-dm', sw(1.8, 0.55));
    B.p(pd, 't-ln', sw(4.2));
    B.c(cx, cy, 6.5, 't-ln', sw(1, 0.8));
    if (last) B.c(last[0], last[1], 7, 't-gn', sw(1.4));
  }

  /* Erdős problems and proofs: a point set with a measured distance, a Moser spindle, or a bound being squeezed */
  function mPoints(B) {
    var pts = B.scatter(B.i(7, 10), 44, 276, 32, 168, 30), d = '', i;
    for (i = 0; i < 6; i++) { var a = B.pick(pts), b = B.pick(pts); if (a !== b) d += seg(a[0], a[1], b[0], b[1]); }
    B.p(d, 't-dm', sw(0.9, 0.7));
    var P0 = pts[0], cr = Math.min(dist(P0, pts[1]), 70, P0[0] - 20, 300 - P0[0], P0[1] - 16, 184 - P0[1]);
    B.c(P0[0], P0[1], cr, 't-dm', sw(0.8, 0.7, { 'stroke-dasharray': '2 4' }));
    var A = pts[2], C = pts[3], an = Math.atan2(C[1] - A[1], C[0] - A[0]), nx = -Math.sin(an) * 6, ny = Math.cos(an) * 6;
    B.p(seg(A[0], A[1], C[0], C[1]) + seg(A[0] - nx, A[1] - ny, A[0] + nx, A[1] + ny) + seg(C[0] - nx, C[1] - ny, C[0] + nx, C[1] + ny), 't-gn', sw(1.3));
    B.p(pts.map(function (p) { return dot(p[0], p[1]); }).join(''), 't-ln', sw(5));
  }
  function mMoser(B) {
    var s = B.u(56, 66), th = B.u(0, TAU), sp = 2 * Math.asin(1 / (2 * Math.sqrt(3)));
    function pt(r, a) { return [r * Math.cos(a), r * Math.sin(a)]; }
    var V = [[0, 0]], E = [], i;
    [th, th + sp].forEach(function (a) {
      var b = V.length;
      V.push(pt(1, a - Math.PI / 6), pt(1, a + Math.PI / 6), pt(Math.sqrt(3), a));
      E.push([0, b], [0, b + 1], [b, b + 1], [b, b + 2], [b + 1, b + 2]);
    });
    var cx = 0, cy = 0;
    V.forEach(function (v) { cx += v[0] / V.length; cy += v[1] / V.length; });
    V = V.map(function (v) { return [160 + (v[0] - cx) * s, 100 + (v[1] - cy) * s]; });
    var d = '';
    E.forEach(function (e) { d += seg(V[e[0]][0], V[e[0]][1], V[e[1]][0], V[e[1]][1]); });
    B.p(d, 't-ln', sw(1.3, 0.8));
    B.p(seg(V[3][0], V[3][1], V[6][0], V[6][1]), 't-gn', sw(1.8));
    V.forEach(function (v, i) { B.c(v[0], v[1], 4, i === 3 || i === 6 ? 't-gf' : 't-ho', sw(1.4)); });
    B.c(V[0][0], V[0][1], Math.min(s, V[0][0] - 20, 300 - V[0][0], V[0][1] - 16, 184 - V[0][1]), 't-dm', sw(0.7, 0.45, { 'stroke-dasharray': '1 4' }));
  }
  function mBounds(B) {
    var y = 128, x0 = 30, x1 = 290, d = '', i;
    for (var x = x0; x <= x1; x += 13) d += M(x, y) + 'v' + ((x - x0) % 52 === 0 ? 7 : 3.5);
    B.p(M(x0, y) + 'H' + x1, 't-dm', sw(1, 0.8));
    B.p(d, 't-dm', sw(0.9, 0.7));
    var lo = B.u(60, 120), hi = B.u(190, 260), hist = '';
    for (i = 0; i < 5; i++) {
      var yy = 40 + i * 14, a = lo - (4 - i) * B.u(5, 12), b = hi + (4 - i) * B.u(5, 12);
      hist += M(a, yy) + 'H' + f(b) + M(a, yy - 3) + 'v6' + M(b, yy - 3) + 'v6';
    }
    B.p(hist, 't-ln', sw(1.1, 0.4));
    B.rect(lo, y - 10, hi - lo, 10, 't-lf', { opacity: 0.14 });
    B.p(M(lo + 6, y - 14) + 'H' + f(lo) + 'V' + f(y + 4) + 'H' + f(lo + 6) + M(hi - 6, y - 14) + 'H' + f(hi) + 'V' + f(y + 4) + 'H' + f(hi - 6), 't-ln', sw(1.8));
    var m = B.u(lo + 30, hi - 30);
    B.p(arrow(lo + 4, y + 18, m - 10, y + 18, 4) + arrow(hi - 4, y + 18, m + 10, y + 18, 4), 't-gn', sw(1.3));
    B.p(M(m, y - 4) + 'v-8', 't-gn', sw(1.2, null, { 'stroke-dasharray': '2 2' }));
  }

  /* physics: percolation clusters, field lines, or wave interference */
  function mPerc(B) {
    var C = 30, R = 17, s = 7.5, x0 = 160 - C * s / 2, y0 = 100 - R * s / 2 - 6, p = B.u(0.54, 0.62), g = [], lab = [], i, j;
    for (i = 0; i < R; i++) { g.push([]); lab.push([]); for (j = 0; j < C; j++) { g[i].push(B.ch(p)); lab[i].push(-1); } }
    var sizes = [], best = -1, bestN = 0;
    for (i = 0; i < R; i++) for (j = 0; j < C; j++) {
      if (!g[i][j] || lab[i][j] >= 0) continue;
      var id = sizes.length, st = [[i, j]], n = 0;
      lab[i][j] = id;
      while (st.length) {
        var c = st.pop(); n++;
        [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(function (o) {
          var a = c[0] + o[0], b = c[1] + o[1];
          if (a >= 0 && a < R && b >= 0 && b < C && g[a][b] && lab[a][b] < 0) { lab[a][b] = id; st.push([a, b]); }
        });
      }
      sizes.push(n);
      if (n > bestN) { bestN = n; best = id; }
    }
    var dl = '', dd = '', lo = C, hi = -1;
    for (i = 0; i < R; i++) for (j = 0; j < C; j++) {
      if (!g[i][j]) continue;
      var q = sq(x0 + j * s + 0.8, y0 + i * s + 0.8, s - 1.6);
      if (lab[i][j] === best) { dl += q; lo = Math.min(lo, j); hi = Math.max(hi, j); } else dd += q;
    }
    B.p(dd, 't-df', { opacity: 0.35 });
    B.p(dl, 't-lf', { opacity: 0.85 });
    var yb = y0 + R * s + 8;
    B.p(M(x0 + lo * s, yb - 4) + 'v8' + M(x0 + lo * s, yb) + 'H' + f(x0 + (hi + 1) * s) + M(x0 + (hi + 1) * s, yb - 4) + 'v8', 't-gn', sw(1.3));
  }
  function mField(B) {
    var q = B.scatter(B.i(2, 3), 80, 240, 50, 150, 70).map(function (p, i) { return [p[0], p[1], i === 1 ? -1 : (i === 0 || B.ch(0.5) ? 1 : -1)]; });
    function E(x, y) {
      var ex = 0, ey = 0;
      q.forEach(function (c) { var dx = x - c[0], dy = y - c[1], r2 = dx * dx + dy * dy + 1, r = Math.sqrt(r2); ex += c[2] * dx / (r2 * r); ey += c[2] * dy / (r2 * r); });
      return [ex, ey];
    }
    var d = '', ph = B.u(0, 1);
    q.forEach(function (c) {
      if (c[2] < 0) return;
      for (var k = 0; k < 14; k++) {
        var a = (k + ph) * TAU / 14, x = c[0] + 8 * Math.cos(a), y = c[1] + 8 * Math.sin(a), pts = [[x, y]];
        for (var st = 0; st < 140; st++) {
          var e = E(x, y), l = Math.sqrt(e[0] * e[0] + e[1] * e[1]);
          if (!l) break;
          x += 3 * e[0] / l; y += 3 * e[1] / l;
          if (st % 2) pts.push([x, y]);
          if (x < -10 || x > 330 || y < -10 || y > 210) break;
          if (q.some(function (o) { return o[2] < 0 && Math.abs(x - o[0]) + Math.abs(y - o[1]) < 8; })) { pts.push([x, y]); break; }
        }
        d += poly(pts);
      }
    });
    B.p(d, 't-ln', sw(0.9, 0.55));
    q.forEach(function (c, i) {
      B.c(c[0], c[1], 7, i === 0 ? 't-gh' : 't-ho', sw(1.4));
      B.p(M(c[0] - 3.5, c[1]) + 'h7' + (c[2] > 0 ? M(c[0], c[1] - 3.5) + 'v7' : ''), i === 0 ? 't-gn' : 't-ln', sw(1.3));
    });
  }

  /* optimization: a convergence curve with the best so far, a schedule, or a tour */
  function mConverge(B) {
    axes(B);
    var N = 64, tau = B.u(8, 20), amp = B.u(95, 115), xs = 248 / N, raw = [], best = [], bv = -1, d = 'M38 36';
    for (var i = 0; i < N; i++) {
      var base = 36 + amp * (1 - Math.exp(-i / tau)), y = base - B.u(0, 26) * Math.exp(-i / (N * 0.6));
      raw.push([38 + i * xs, y]);
      if (y > bv) { bv = y; if (i) d += 'H' + f(38 + i * xs) + 'V' + f(y); }
      best.push(bv);
    }
    d += 'H' + f(38 + N * xs);
    B.p(poly(raw), 't-ln', sw(0.9, 0.35));
    B.p(raw.map(function (p) { return dot(p[0], p[1]); }).join(''), 't-ln', sw(2.2, 0.4));
    B.p(d, 't-ln', sw(1.7));
    var ty = Math.min(166, bv + B.u(6, 12));
    B.p(M(34, ty) + 'H292', 't-gn', sw(1.1, 0.9, { 'stroke-dasharray': '4 3' }));
    B.p(arrow(280, bv + 1, 280, ty - 1, 3), 't-gn', sw(1.3));
  }
  function mGantt(B) {
    var rows = B.i(5, 7), rh = 18, y0 = 100 - rows * rh / 2, bars = '', ends = [], crit = null, r;
    for (r = 0; r < rows; r++) {
      var x = 44 + B.u(0, 14), y = y0 + r * rh + 4;
      while (x < 250) {
        var w = Math.min(B.u(14, 46), 268 - x);
        bars += M(x, y) + 'h' + f(w) + 'v10h' + f(-w) + 'z';
        if (!crit || x + w > crit[0] + crit[2]) crit = [x, y, w];
        x += w + B.u(2, 12);
      }
      ends.push(x);
    }
    B.p(M(36, y0) + 'V' + f(y0 + rows * rh) + 'H292', 't-dm', sw(1, 0.8));
    B.p(bars, 't-lf', { opacity: 0.22 });
    B.p(bars, 't-ln', sw(0.9, 0.8));
    B.rect(crit[0], crit[1], crit[2], 10, 't-gf', { opacity: 0.85 });
    var mk = crit[0] + crit[2];
    B.p(M(mk, y0 - 10) + 'V' + f(y0 + rows * rh + 8), 't-gn', sw(1.1, null, { 'stroke-dasharray': '3 3' }));
  }
  function mTour(B) {
    var pts = B.scatter(B.i(16, 24), 34, 286, 30, 170, 20), used = [0], cur = 0, i, t = [pts[0]];
    while (used.length < pts.length) {
      var bj = -1, bd = 1e9;
      for (i = 0; i < pts.length; i++) if (used.indexOf(i) < 0 && dist(pts[cur], pts[i]) < bd) { bd = dist(pts[cur], pts[i]); bj = i; }
      used.push(bj); cur = bj; t.push(pts[bj]);
    }
    B.p(poly(t, true), 't-ln', sw(1.2, 0.75));
    B.p(pts.map(function (p) { return dot(p[0], p[1]); }).join(''), 't-ln', sw(4.5));
    B.c(pts[0][0], pts[0][1], 6.5, 't-gn', sw(1.5));
    B.c(pts[0][0], pts[0][1], 2.6, 't-gf');
  }

  /* disease research: survival curves, or a cluster of cells */
  function mKM(B) {
    axes(B);
    var n = B.i(2, 3), cross = [];
    B.p(M(34, 104) + 'H292', 't-dm', sw(0.8, 0.6, { 'stroke-dasharray': '2 4' }));
    for (var c = 0; c < n; c++) {
      var y = 36, x = 34, d = M(x, y), cens = '', rate = B.u(0.55, 1.2) * (1 + c * 0.35);
      while (x < 286) {
        x += B.u(4, 18);
        if (x > 286) break;
        if (B.ch(0.25)) { cens += M(x, y - 3) + 'v6'; continue; }
        var ny = Math.min(166, y + B.u(1, 7) * rate);
        d += 'H' + f(x) + 'V' + f(ny);
        if (cross[c] == null && y < 104 && ny >= 104) cross[c] = x;
        y = ny;
      }
      d += 'H286';
      B.p(d, c ? 't-dm' : 't-ln', sw(c ? 1.1 : 1.6, c ? 0.75 : 1, c > 1 ? { 'stroke-dasharray': '4 2' } : null));
      B.p(cens, c ? 't-dm' : 't-ln', sw(1, 0.8));
    }
    /* the green target: the gap between the median survival times of the first two curves */
    var a = cross[0] == null ? 286 : cross[0], b = cross[1] == null ? 286 : cross[1], lo = Math.min(a, b), hi = Math.max(a, b);
    if (hi - lo < 8) { lo = Math.max(40, lo - 6); hi = lo + 12; }
    B.p(M(lo, 98) + 'v12' + M(lo, 104) + 'H' + f(hi) + M(hi, 98) + 'v12', 't-gn', sw(1.6));
    B.c(a, 104, 3.2, 't-gf');
  }
  function mCells(B) {
    var cx = B.u(130, 190), cy = 100, rx = B.u(96, 120), ry = B.u(62, 74);
    var cs = B.pack(function (x, y) { var u = (x - cx) / rx, v = (y - cy) / ry, q = 1 - Math.sqrt(u * u + v * v); return q * ry; }, 6, B.u(14, 19), 500, 30);
    var d = '', nu = '';
    cs.forEach(function (c, i) {
      if (!i) return;
      var pts = [];
      for (var k = 0; k < 7; k++) { var a = k * TAU / 7, rr = c[2] * B.u(0.86, 1); pts.push([c[0] + rr * Math.cos(a), c[1] + rr * Math.sin(a)]); }
      d += smooth(pts, true);
      nu += dot(c[0] + B.u(-2, 2), c[1] + B.u(-2, 2));
    });
    B.p(d, 't-ln', sw(1.1, 0.75));
    B.p(nu, 't-ln', sw(4.2, 0.55));
    if (cs.length) { var h = cs[0]; B.c(h[0], h[1], h[2] * 0.95, 't-gh', sw(1.5)); B.c(h[0], h[1], 2.4, 't-gf'); }
  }

  /* recreational math: a polyomino tiling, or a Sudoku-style grid with one open cell */
  function mPolyomino(B) {
    var C = 13, R = 8, s = 15, x0 = 160 - C * s / 2, y0 = 100 - R * s / 2, own = [], i, j, k;
    for (i = 0; i < R * C; i++) own.push(-1);
    var nP = B.i(13, 18), cells = [];
    for (k = 0; k < nP; k++) { var c = B.i(0, R * C - 1); if (own[c] < 0) { own[c] = cells.length; cells.push([c]); } }
    for (var grew = true; grew;) {
      grew = false;
      for (k = 0; k < cells.length; k++) {
        var fr = [];
        cells[k].forEach(function (c) {
          var r = Math.floor(c / C), q = c % C;
          [[r - 1, q], [r + 1, q], [r, q - 1], [r, q + 1]].forEach(function (o) { if (o[0] >= 0 && o[0] < R && o[1] >= 0 && o[1] < C && own[o[0] * C + o[1]] < 0) fr.push(o[0] * C + o[1]); });
        });
        if (fr.length) { var t = B.pick(fr); own[t] = k; cells[k].push(t); grew = true; }
      }
    }
    var d = '', hot = B.i(0, cells.length - 1), hd = '', fill = '', faint = '';
    function O(r, q) { return r < 0 || r >= R || q < 0 || q >= C ? -2 : own[r * C + q]; }
    for (i = 0; i < R; i++) for (j = 0; j < C; j++) {
      var o = O(i, j), x = x0 + j * s, y = y0 + i * s;
      if (O(i - 1, j) !== o) { d += M(x, y) + 'h' + s; if (o === hot || O(i - 1, j) === hot) hd += M(x, y) + 'h' + s; }
      if (O(i, j - 1) !== o) { d += M(x, y) + 'v' + s; if (o === hot || O(i, j - 1) === hot) hd += M(x, y) + 'v' + s; }
      if (i === R - 1) { d += M(x, y + s) + 'h' + s; if (o === hot) hd += M(x, y + s) + 'h' + s; }
      if (j === C - 1) { d += M(x + s, y) + 'v' + s; if (o === hot) hd += M(x + s, y) + 'v' + s; }
      if (o === hot) fill += sq(x, y, s); else if (o % 5 === 1) faint += sq(x, y, s);
    }
    B.p(faint, 't-lf', { opacity: 0.12 });
    B.p(fill, 't-gf', { opacity: 0.16 });
    B.p(d, 't-ln', sw(1.5, 0.85));
    B.p(hd, 't-gn', sw(2));
  }
  function mSudoku(B) {
    var box = B.pick([[3, 3], [2, 3], [2, 4], [3, 4]]), n = box[0] * box[1], s = Math.min(15, 140 / n), w = n * s;
    var x0 = 160 - w / 2 + B.u(-50, 50), y0 = 100 - w / 2, thin = '', thick = '', giv = '', open = [];
    for (var i = 0; i <= n; i++) {
      var p = M(x0, y0 + i * s) + 'h' + f(w), q = M(x0 + i * s, y0) + 'v' + f(w);
      if (i % box[0] === 0) thick += p; else thin += p;
      if (i % box[1] === 0) thick += q; else thin += q;
    }
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) {
      if (B.ch(0.3)) giv += dot(x0 + c * s + s / 2, y0 + r * s + s / 2); else open.push([r, c]);
    }
    B.p(thin, 't-dm', sw(0.6, 0.6));
    B.p(thick, 't-ln', sw(1.4, 0.9));
    B.p(giv, 't-ln', sw(Math.max(3, s * 0.32), 0.8));
    var h = B.pick(open);
    B.rect(x0 + h[1] * s + 1.5, y0 + h[0] * s + 1.5, s - 3, s - 3, 't-gh', sw(1.3));
  }

  /* biology: a double helix, or a contact map */
  function mHelix(B) {
    var A = B.u(26, 34), k = TAU / B.u(70, 95), ph = B.u(0, TAU), cy = 100, s1 = [], s2 = [], rungs = '', hot = null;
    B.group('rotate(' + f(B.u(-14, 14)) + ' 160 100)');
    for (var x = 4; x <= 316; x += 4) {
      var y1 = cy + A * Math.sin(k * x + ph), y2 = cy + A * Math.sin(k * x + ph + 2.4);
      s1.push([x, y1]); s2.push([x, y2]);
      if (x % 12 === 4) { rungs += seg(x, y1, x, y2); if (!hot && x > 140) hot = [x, y1, y2]; }
    }
    B.p(rungs, 't-dm', sw(1, 0.55));
    B.p(poly(s2), 't-ln', sw(1.1, 0.5));
    B.p(poly(s1), 't-ln', sw(1.8, 0.95));
    if (hot) B.p(seg(hot[0], hot[1], hot[0], hot[2]), 't-gn', sw(2.4));
    B.end();
  }

  /* wildcard (and the fallback): a constellation */
  function mStars(B) {
    var dust = '', i;
    for (i = 0; i < 46; i++) dust += dot(B.u(16, 304), B.u(14, 186));
    B.p(dust, 't-dm', sw(1.2, 0.45));
    var st = B.scatter(B.i(7, 10), 40, 280, 30, 170, 30), inT = [0], d = '';
    while (inT.length < st.length) {
      var bi = -1, bj = -1, bd = 1e9;
      inT.forEach(function (a) { st.forEach(function (p, j) { if (inT.indexOf(j) < 0 && dist(st[a], p) < bd) { bd = dist(st[a], p); bi = a; bj = j; } }); });
      d += seg(st[bi][0], st[bi][1], st[bj][0], st[bj][1]);
      inT.push(bj);
    }
    B.p(d, 't-ln', sw(0.9, 0.55));
    var big = '', small = '', hot = B.i(0, st.length - 1);
    st.forEach(function (p, i) { if (i !== hot) { if (B.ch(0.4)) big += dot(p[0], p[1]); else small += dot(p[0], p[1]); } });
    B.p(small, 't-ln', sw(3.6));
    B.p(big, 't-ln', sw(5.6));
    var h = st[hot];
    B.p(M(h[0] - 11, h[1]) + 'h6' + M(h[0] + 5, h[1]) + 'h6' + M(h[0], h[1] - 11) + 'v6' + M(h[0], h[1] + 5) + 'v6', 't-gn', sw(1.3));
    B.c(h[0], h[1], 3, 't-gf');
  }

  /* packings: circles in a container, equal circles with room for one more, or points on a sphere */
  function mPack(B) {
    var circ = B.ch(0.5), cx = 160, cy = 100, R = 78, d = '';
    var bound = circ ? function (x, y) { return R - Math.sqrt((x - cx) * (x - cx) + (y - cy) * (y - cy)); }
                     : function (x, y) { return Math.min(x - 82, 238 - x, y - 22, 178 - y); };
    var cs = B.pack(bound, 4, B.u(18, 30), 1200, 44);
    cs.slice(1).forEach(function (c) { d += ring(c[0], c[1], c[2]); });
    B.p(circ ? ring(cx, cy, R) : 'M82 22H238V178H82Z', 't-dm', sw(1.3, 0.85));
    B.p(d, 't-ln', sw(1, 0.8));
    if (cs.length) B.c(cs[0][0], cs[0][1], cs[0][2], 't-gh', sw(1.4));
  }
  function mEqual(B) {
    var r = B.u(9, 13), cx = 160, cy = 100, R = 76, d = '', pts = [], ph = B.u(0, 1);
    for (var j = -8; j <= 8; j++) for (var i = -10; i <= 10; i++) {
      var x = cx + (i + (j % 2 ? 0.5 : 0) + ph) * 2 * r, y = cy + j * r * Math.sqrt(3);
      if (Math.sqrt((x - cx) * (x - cx) + (y - cy) * (y - cy)) <= R - r) pts.push([x + B.u(-1, 1), y + B.u(-1, 1)]);
    }
    var gap = pts.length ? B.i(0, pts.length - 1) : -1;
    pts.forEach(function (p, i) { if (i !== gap) d += ring(p[0], p[1], r - 0.8); });
    B.p(ring(cx, cy, R), 't-dm', sw(1.3, 0.85));
    B.p(d, 't-ln', sw(1, 0.8));
    if (gap >= 0) B.c(pts[gap][0], pts[gap][1], r - 0.8, 't-gh', sw(1.3, null, { 'stroke-dasharray': '3 2' }));
  }
  function mSphere(B) {
    var cx = 160 + B.u(-24, 24), cy = 100, R = 72, lat = '', front = '', back = '', hot = null;
    B.p(ring(cx, cy, R), 't-ln', sw(1.3, 0.9));
    [-0.6, -0.3, 0, 0.3, 0.6].forEach(function (s) {
      var rx = R * Math.sqrt(1 - s * s), y = cy + R * s;
      lat += M(cx - rx, y) + 'a' + f(rx) + ' ' + f(rx * 0.26) + ' 0 0 0 ' + f(2 * rx) + ' 0';
    });
    B.p(lat, 't-dm', sw(0.8, 0.55));
    B.p(M(cx, cy - R) + 'a' + f(R * 0.35) + ' ' + f(R) + ' 0 0 0 0 ' + f(2 * R), 't-dm', sw(0.8, 0.55));
    for (var i = 0; i < 34; i++) {
      var z = B.u(-1, 1), a = B.u(0, TAU), q = Math.sqrt(1 - z * z), x = cx + R * q * Math.cos(a), y = cy + R * z * 0.98, depth = q * Math.sin(a);
      if (depth > 0) { front += dot(x, y); if (!hot && depth > 0.5) hot = [x, y]; } else back += dot(x, y);
    }
    B.p(back, 't-dm', sw(2.6, 0.5));
    B.p(front, 't-ln', sw(4.6));
    if (hot) B.c(hot[0], hot[1], 7, 't-gn', sw(1.4));
  }

  /* earth and sky: a contour map with its summit */
  function mContour(B) {
    var F = field(B, B.i(3, 5)), n = 7;
    for (var l = 1; l <= n; l++) {
      var lev = F.lo + (F.hi - F.lo) * l / (n + 1), main = l % 3 === 0;
      B.p(iso(F.F, lev), main ? 't-ln' : 't-dm', sw(main ? 1.3 : 0.8, main ? 0.9 : 0.6));
    }
    var p = F.peak;
    B.p(M(p[0], p[1] - 6) + L(p[0] + 5.5, p[1] + 4) + L(p[0] - 5.5, p[1] + 4) + 'Z', 't-gn', sw(1.4));
  }

  /* algorithms: a sorting network, a search tree, or matrices to multiply */
  function mSortNet(B) {
    var n = B.i(6, 9), sp = Math.min(18, 128 / (n - 1)), y0 = 100 - (n - 1) * sp / 2, wires = '', comps = '', ends = '';
    for (var i = 0; i < n; i++) wires += M(34, y0 + i * sp) + 'H286';
    var layers = B.i(7, 10), dx = 226 / layers, all = [];
    for (var l = 0; l < layers; l++) {
      var used = [], x = 47 + l * dx;
      for (var t = 0; t < 4; t++) {
        var a = B.i(0, n - 2), b = B.i(a + 1, Math.min(n - 1, a + 4)), free = true;
        for (var k = a; k <= b; k++) if (used[k]) free = false;
        if (!free) continue;
        for (k = a; k <= b; k++) used[k] = 1;
        var xx = x + (t % 2) * dx * 0.4;
        all.push([xx, y0 + a * sp, y0 + b * sp]);
      }
    }
    var hot = all.length ? B.i(0, all.length - 1) : -1;
    all.forEach(function (c, i) { if (i !== hot) { comps += M(c[0], c[1]) + 'V' + f(c[2]); ends += dot(c[0], c[1]) + dot(c[0], c[2]); } });
    B.p(wires, 't-dm', sw(0.9, 0.7));
    B.p(comps, 't-ln', sw(1.3, 0.9));
    B.p(ends, 't-ln', sw(4.6));
    if (hot >= 0) { var h = all[hot]; B.p(M(h[0], h[1]) + 'V' + f(h[2]), 't-gn', sw(1.8)); B.p(dot(h[0], h[1]) + dot(h[0], h[2]), 't-gn', sw(5.4)); }
  }
  function mTree(B) {
    var nodes = [], d = '', leaves = [];
    (function grow(i, l, x0, x1) {
      var x = (x0 + x1) / 2, y = 34 + l * 38;
      nodes.push([x, y]);
      var idx = nodes.length - 1;
      if (l === 3) { leaves.push(idx); return; }
      for (var s = 0; s < 2; s++) {
        if (l >= 1 && B.ch(0.25)) continue;
        var cx0 = s ? x : x0, cx1 = s ? x1 : x, cx = (cx0 + cx1) / 2;
        d += seg(x, y, cx, y + 38);
        grow(0, l + 1, cx0, cx1);
      }
    })(0, 0, 34 + B.u(0, 20), 286 - B.u(0, 20));
    B.p(d, 't-dm', sw(1.1, 0.8));
    var hot = leaves.length ? B.pick(leaves) : nodes.length - 1;
    nodes.forEach(function (n, i) { if (i !== hot) B.c(n[0], n[1], 4.4, 't-ho', sw(1.4)); });
    B.c(nodes[hot][0], nodes[hot][1], 5, 't-gf');
    B.c(nodes[hot][0], nodes[hot][1], 10, 't-gn', sw(1, null, { 'stroke-dasharray': '2 3' }));
  }
  function mMatrix(B) {
    var n = B.i(3, 5), m = B.i(3, 5), p = B.i(3, 5), s = 14, gap = 26, w = (m + p + p) * s + 2 * gap;
    var x0 = 160 - w / 2, y0 = 100 - Math.max(n, m) * s / 2, grid = '', fill = '', ops = '';
    function mat(x, y, r, c, density) {
      for (var i = 0; i <= r; i++) grid += M(x, y + i * s) + 'h' + c * s;
      for (var j = 0; j <= c; j++) grid += M(x + j * s, y) + 'v' + r * s;
      for (i = 0; i < r; i++) for (j = 0; j < c; j++) if (B.ch(density)) fill += sq(x + j * s + 2, y + i * s + 2, s - 4);
    }
    mat(x0, y0, n, m, 0.5);
    var xb = x0 + m * s + gap;
    mat(xb, y0, m, p, 0.5);
    var xc = xb + p * s + gap;
    mat(xc, y0, n, p, 0.85);
    ops += M(x0 + m * s + gap / 2 - 3.5, y0 + n * s / 2 - 3.5) + 'l7 7m0 -7l-7 7';
    ops += M(xb + p * s + gap / 2 - 4, y0 + n * s / 2 - 2.5) + 'h8m-8 5h8';
    B.p(grid, 't-dm', sw(0.8, 0.7));
    B.p(fill, 't-lf', { opacity: 0.55 });
    B.p(ops, 't-ln', sw(1.4));
    B.rect(xc + B.i(0, p - 1) * s, y0 + B.i(0, n - 1) * s, s, s, 't-gh', sw(1.4));
    var rk = '';
    for (var k = 0; k < B.i(3, 6); k++) rk += M(x0 + k * 9, y0 + Math.max(n, m) * s + 26) + 'v-' + f(B.u(4, 12));
    B.p(rk, 't-dm', sw(3, 0.6, { 'class': 't-dm bt' }));
  }

  /* machine learning: a small neural network, loss curves, or a forecast */
  function mNet(B) {
    var sizes = [B.i(3, 4), B.i(4, 5), B.i(4, 5), B.i(2, 3)], L = [], d = '', hd = '';
    sizes.forEach(function (n, l) {
      var x = 56 + l * 69, col = [];
      for (var i = 0; i < n; i++) col.push([x, 100 + (i - (n - 1) / 2) * 30]);
      L.push(col);
    });
    for (var l = 0; l < 3; l++) L[l].forEach(function (a) { L[l + 1].forEach(function (b) { if (B.ch(0.22)) hd += seg(a[0], a[1], b[0], b[1]); else d += seg(a[0], a[1], b[0], b[1]); }); });
    B.p(d, 't-dm', sw(0.7, 0.45));
    B.p(hd, 't-ln', sw(1.1, 0.75));
    var out = B.i(0, sizes[3] - 1);
    L.forEach(function (col, l) { col.forEach(function (p, i) { if (!(l === 3 && i === out)) B.c(p[0], p[1], 5, 't-ho', sw(1.4)); }); });
    B.c(L[3][out][0], L[3][out][1], 6, 't-gf');
  }
  function mLoss(B) {
    axes(B);
    var tau = B.u(10, 22), tr = [], va = [], best = null, bv = 1e9;
    for (var x = 38; x <= 290; x += 4) {
      var t = (x - 38) / 252, a = 40 + 110 * (1 - Math.exp(-t * 252 / (tau * 4)));
      tr.push([x, a + B.u(-3, 3)]);
      var v = a - 14 - 70 * t * t + B.u(-3, 3) + 60 * Math.max(0, t - 0.6);
      va.push([x, Math.min(168, 175 - (175 - v) * 0.9)]);
    }
    va.forEach(function (p) { if (p[1] > (best ? best[1] : -1)) best = p; });
    B.p(poly(tr), 't-ln', sw(1.4, 0.9));
    B.p(poly(va), 't-dm', sw(1.2, 0.85, { 'stroke-dasharray': '4 2' }));
    if (best) { B.c(best[0], best[1], 3.6, 't-gf'); B.p(M(best[0], 26) + 'V' + f(best[1] - 6), 't-gn', sw(1, 0.8, { 'stroke-dasharray': '2 3' })); }
  }
  function mForecast(B) {
    axes(B);
    var y = 100, past = [], fut = [], up = [], lo = [], k = B.u(0.1, 0.2), ph = B.u(0, TAU);
    for (var x = 38; x <= 200; x += 3) { y += B.u(-4, 4) + (100 - y) * 0.05; past.push([x, y + 16 * Math.sin(k * x + ph)]); }
    var y0 = past[past.length - 1][1] - 16 * Math.sin(k * 200 + ph);
    for (x = 200; x <= 290; x += 3) {
      var c = y0 + 16 * Math.sin(k * x + ph), w = 4 + (x - 200) * 0.28;
      fut.push([x, c]); up.push([x, c - w]); lo.push([x, c + w]);
    }
    B.p(poly(up.concat(lo.reverse()), true), 't-lf', { opacity: 0.12 });
    B.p(M(200, 26) + 'V172', 't-dm', sw(0.8, 0.6, { 'stroke-dasharray': '2 3' }));
    B.p(poly(past), 't-ln', sw(1.4, 0.9));
    B.p(poly(fut), 't-gn', sw(1.5, null, { 'stroke-dasharray': '4 3' }));
  }

  /* unbroken ciphers: invented glyphs in five-groups, or cipher wheels with pins */
  function mCipher(B) {
    var rows = 5, groups = 3, per = 5, gw = 8, gh = 12, gap = 5.5, ggap = 15, rh = 24;
    var w = groups * (per * gw + (per - 1) * gap) + (groups - 1) * ggap, x0 = 160 - w / 2, y0 = 100 - rows * rh / 2 + 6;
    var d = '', hot = [B.i(0, rows - 1), B.i(0, groups * per - 1)], hd = '', hx = 0, hy = 0;
    for (var r = 0; r < rows; r++) for (var g = 0; g < groups * per; g++) {
      var x = x0 + Math.floor(g / per) * (per * gw + (per - 1) * gap + ggap) + (g % per) * (gw + gap), y = y0 + r * rh;
      var s = glyph(B, x, y, gw, gh, false);
      if (r === hot[0] && g === hot[1]) { hd = s; hx = x; hy = y; } else d += s;
    }
    B.p(d, 't-ln', sw(1.3, 0.8));
    B.p(hd, 't-gn', sw(1.5));
    B.rect(hx - 4, hy - 5, gw + 8, gh + 10, 't-gn', sw(1, 0.85, { 'stroke-dasharray': '2 2' }));
  }
  function mRotor(B) {
    [[B.u(96, 112), 100, B.u(60, 68), 26], [B.u(220, 236), 100, B.u(40, 48), B.i(17, 25)]].forEach(function (w, wi) {
      var cx = w[0], cy = w[1], R = w[2], n = w[3], rot = B.u(0, TAU), tk = '', pins = '', off = '';
      B.p(ring(cx, cy, R) + ring(cx, cy, R * 0.62) + ring(cx, cy, 5), 't-dm', sw(1, 0.8));
      for (var i = 0; i < n; i++) {
        var a = rot + i * TAU / n, c = Math.cos(a), s = Math.sin(a);
        tk += seg(cx + R * c, cy + R * s, cx + (R - 6) * c, cy + (R - 6) * s);
        if (B.ch(0.5)) pins += dot(cx + R * 0.8 * c, cy + R * 0.8 * s); else off += dot(cx + R * 0.8 * c, cy + R * 0.8 * s);
      }
      B.p(tk, 't-ln', sw(1, 0.75));
      B.p(off, 't-dm', sw(2, 0.6));
      B.p(pins, 't-ln', sw(4.2));
      if (!wi) B.p(M(cx - 5, cy - R - 12) + L(cx + 5, cy - R - 12) + L(cx, cy - R - 3) + 'Z' + M(cx, cy - R * 0.62) + 'V' + f(cy - R + 8), 't-gn', sw(1.4));
    });
  }

  /* undeciphered scripts: a ruled tablet of invented glyphs, wedge impressions, or a khipu */
  function mTablet(B) {
    var rows = 4, n = B.i(9, 12), gw = 11, gh = 15, gap = 8, w = n * gw + (n - 1) * gap, x0 = 160 - w / 2, y0 = 44, rh = 32;
    B.p('M42 26H278Q290 26 290 38V162Q290 174 278 174H42Q30 174 30 162V38Q30 26 42 26Z', 't-dm', sw(1.2, 0.85));
    var rules = '', d = '', hot = [B.i(0, rows - 2), B.i(0, n - 1)], hd = '', hp = null;
    for (var r = 0; r < rows; r++) {
      rules += M(38, y0 + r * rh + gh + 7) + 'H282';
      var lineN = r === rows - 1 ? B.i(3, n - 2) : n;
      for (var i = 0; i < lineN; i++) {
        var x = x0 + i * (gw + gap), y = y0 + r * rh, s = glyph(B, x, y, gw, gh, true);
        if (r === hot[0] && i === hot[1]) { hd = s; hp = [x, y]; } else d += s;
      }
    }
    B.p(rules, 't-dm', sw(0.6, 0.45));
    B.p(d, 't-ln', sw(1.4, 0.8));
    if (hp) { B.p(hd, 't-gn', sw(1.6)); B.rect(hp[0] - 4, hp[1] - 5, gw + 8, gh + 10, 't-gn', sw(1, 0.85, { 'stroke-dasharray': '2 2' })); }
  }
  function mWedges(B) {
    B.p('M40 30Q160 20 280 30Q292 100 280 170Q160 180 40 170Q28 100 40 30Z', 't-dm', sw(1.2, 0.85));
    var heads = '', tails = '', rules = '', signs = [];
    for (var r = 0; r < 4; r++) {
      var y = 48 + r * 34, x = 52;
      rules += M(44, y + 18) + 'H276';
      while (x < 262) {
        var sg = '', hs = '', k = B.i(1, 4);
        for (var i = 0; i < k; i++) {
          var dir = B.pick([0, 0, Math.PI / 2, Math.PI / 4, -Math.PI / 4]), len = B.u(7, 12), px = x + B.u(0, 8), py = y + B.u(-3, 5);
          var c = Math.cos(dir), s = Math.sin(dir);
          hs += M(px - 3 * s, py + 3 * c) + L(px + 3 * s, py - 3 * c) + L(px + 5 * c, py + 5 * s) + 'Z';
          sg += seg(px + 5 * c, py + 5 * s, px + len * c, py + len * s);
        }
        signs.push([x, y, hs, sg]);
        x += B.u(18, 26);
      }
    }
    var hot = B.i(0, signs.length - 1);
    signs.forEach(function (s, i) { if (i !== hot) { heads += s[2]; tails += s[3]; } });
    B.p(rules, 't-dm', sw(0.6, 0.4));
    B.p(heads, 't-lf', { opacity: 0.8 });
    B.p(tails, 't-ln', sw(1.2, 0.8));
    var h = signs[hot];
    B.p(h[2], 't-gf');
    B.p(h[3], 't-gn', sw(1.2));
    B.rect(h[0] - 6, h[1] - 10, 26, 24, 't-gn', sw(1, 0.85, { 'stroke-dasharray': '2 2' }));
  }
  function mKhipu(B) {
    var sag = B.u(4, 12), n = B.i(10, 15), cord = [], cords = '', knots = '', hot = B.i(1, n - 2), hc = '', hk = '';
    for (var x = 26; x <= 294; x += 12) cord.push([x, 36 + sag * Math.sin(Math.PI * (x - 26) / 268)]);
    B.p(smooth(cord), 't-ln', sw(2.4, 0.9));
    for (var i = 0; i < n; i++) {
      var cx = 40 + i * (240 / (n - 1)), cy = 36 + sag * Math.sin(Math.PI * (cx - 26) / 268), end = B.u(130, 178), sway = B.u(-8, 8);
      var path = M(cx, cy) + 'Q' + f(cx + sway) + ' ' + f((cy + end) / 2) + ' ' + f(cx + sway * 0.4) + ' ' + f(end), kn = '';
      [70, 102, 134].forEach(function (yy) {
        var digit = B.i(0, 4);
        for (var k = 0; k < digit; k++) { var ky = yy + k * 5; if (ky < end - 4) kn += dot(cx + sway * 0.75 * Math.sin(Math.PI * (ky - cy) / (end - cy)), ky); }
      });
      if (i === hot) { hc = path; hk = kn; } else { cords += path; knots += kn; }
    }
    B.p(cords, 't-dm', sw(1.2, 0.8));
    B.p(knots, 't-ln', sw(4.2, 0.9));
    B.p(hc, 't-gn', sw(1.4, null, { 'stroke-dasharray': '3 2' }));
    B.p(hk, 't-gn', sw(4.2));
  }

  /* ancient texts: a fragment with a lacuna, or two fragments that join */
  function jag(B, x0, y0, x1, y1, amp, n) {
    var p = [];
    for (var i = 0; i <= n; i++) { var t = i / n; p.push([x0 + (x1 - x0) * t + (i && i < n ? B.u(-amp, amp) : 0), y0 + (y1 - y0) * t + (i && i < n ? B.u(-amp, amp) : 0)]); }
    return p;
  }
  function textLines(B, x0, x1, y0, rows, skip) {
    var d = '', gaps = [];
    for (var r = 0; r < rows; r++) {
      var y = y0 + r * 15, x = x0 + B.u(0, 6), end = x1 - B.u(0, 14);
      while (x < end) {
        var w = Math.min(B.u(7, 28), end - x);
        if (w > 3) { if (skip && skip(x + w / 2, y)) gaps.push([x, y, w]); else d += M(x, y) + 'h' + f(w); }
        x += w + 5;
      }
    }
    return { d: d, gaps: gaps };
  }
  function mFragment(B) {
    var top = jag(B, 46, 28, 274, 30, 4, 9), right = jag(B, 274, 30, 270, 172, 6, 8), bot = jag(B, 270, 172, 50, 170, 5, 9), left = jag(B, 50, 170, 46, 28, 6, 8);
    B.p(poly(top.concat(right, bot, left), true), 't-dm', sw(1.2, 0.85));
    var lx = B.u(110, 210), ly = B.u(70, 130), rx = B.u(26, 40), ry = B.u(16, 26);
    var T = textLines(B, 60, 260, 46, 9, function (x, y) { var u = (x - lx) / rx, v = (y - ly) / ry; return u * u + v * v < 1; });
    var hole = [];
    for (var k = 0; k < 9; k++) { var a = k * TAU / 9; hole.push([lx + rx * B.u(0.9, 1.15) * Math.cos(a), ly + ry * B.u(0.9, 1.2) * Math.sin(a)]); }
    B.p(T.d, 't-ln', sw(2.4, 0.6));
    B.p(smooth(hole, true), 't-dm', sw(0.9, 0.7, { 'stroke-dasharray': '2 3' }));
    var g = T.gaps.length ? B.pick(T.gaps) : [lx - 10, ly, 20];
    B.rect(g[0] - 2, g[1] - 4, g[2] + 4, 8, 't-gh', sw(1.1, null, { 'stroke-dasharray': '3 2' }));
  }
  function mJoin(B) {
    var seam = jag(B, 160, 34, 162, 166, 9, 7), L = [[46, 36]].concat(seam.map(function (p) { return [p[0] - 9, p[1]]; }), [[44, 168]]);
    var R = [[276, 34]].concat(seam.map(function (p) { return [p[0] + 9, p[1]]; }), [[278, 166]]);
    B.p(poly(L, true) + poly(R, true), 't-dm', sw(1.2, 0.85));
    var A = textLines(B, 58, 140, 52, 8), C = textLines(B, 182, 266, 52, 8);
    B.p(A.d + C.d, 't-ln', sw(2.4, 0.6));
    var d = '';
    seam.forEach(function (p, i) { if (i && i < seam.length - 1 && i % 2) d += M(p[0] - 6, p[1]) + 'h12'; });
    B.p(d, 't-gn', sw(1.3, null, { 'stroke-dasharray': '2 2' }));
  }

  /* Herculaneum scrolls: a rolled scroll in cross-section with one traced wrap, or CT layers with ink */
  function mScroll(B) {
    var cx = 160 + B.u(-30, 30), cy = 100, turns = B.i(5, 8), rmax = 72, b = (rmax - 5) / (turns * TAU), ph = B.u(0, TAU), sq_ = B.u(0.72, 0.85);
    var a = [], c = [], hot = [], h0 = B.u(turns * TAU * 0.55, turns * TAU * 0.85);
    for (var t = 0; t <= turns * TAU; t += 0.14) {
      var r = 5 + b * t + 1.4 * Math.sin(t * 3 + ph), x = cx + r * Math.cos(t + ph), y = cy + r * Math.sin(t + ph) * sq_;
      a.push([x, y]);
      c.push([cx + (r + 2.2) * Math.cos(t + ph), cy + (r + 2.2) * Math.sin(t + ph) * sq_]);
      if (t >= h0 && t <= h0 + 1.7) hot.push([x, y]);
    }
    B.p(M(cx - 92, cy) + 'H' + f(cx + 92) + M(cx, cy - 72) + 'V' + f(cy + 72), 't-dm', sw(0.7, 0.5, { 'stroke-dasharray': '2 4' }));
    B.p(poly(c), 't-dm', sw(0.8, 0.45));
    B.p(poly(a), 't-ln', sw(1.2, 0.8));
    B.p(poly(hot), 't-gn', sw(2.6));
  }
  function mLayers(B) {
    var n = B.i(7, 9), d = '', ink = '', hot = B.i(1, n - 2), hb = null;
    for (var i = 0; i < n; i++) {
      var y0 = 34 + i * (132 / (n - 1)), pts = [], ph = B.u(0, TAU), amp = B.u(2, 6);
      for (var x = 20; x <= 300; x += 10) pts.push([x, y0 + amp * Math.sin(x * 0.03 + ph) + B.u(-1, 1)]);
      d += smooth(pts);
      if (B.ch(0.6) || i === hot) {
        var k = B.i(2, 4), xs = B.u(40, 220);
        for (var j = 0; j < k; j++) {
          var xx = xs + j * B.u(8, 14), yy = y0 + amp * Math.sin(xx * 0.03 + ph);
          ink += M(xx, yy) + 'h' + f(B.u(3, 7));
          if (i === hot && !hb) hb = [xs - 6, yy];
        }
      }
    }
    B.p(d, 't-dm', sw(1, 0.75));
    B.p(ink, 't-ln', sw(3, 0.9));
    if (hb) B.rect(hb[0], hb[1] - 9, 52, 18, 't-gn', sw(1.2, null, { 'stroke-dasharray': '3 2' }));
  }

  /* drug discovery and chemistry: a ring-and-bond molecule skeleton */
  function mMolecule(B) {
    var Rr = 17, rings = [[0, 0]], i, k, bonds = {}, d = '', dbl = '', end = [], keyOf = function (p) { return Math.round(p[0]) + ',' + Math.round(p[1]); };
    function vtx(c, k) { var a = Math.PI / 6 + k * Math.PI / 3; return [c[0] + Rr * Math.cos(a), c[1] + Rr * Math.sin(a)]; }
    function bond(a, b, dbl_) {
      var k = keyOf(a) < keyOf(b) ? keyOf(a) + '|' + keyOf(b) : keyOf(b) + '|' + keyOf(a);
      if (bonds[k]) return;
      bonds[k] = 1;
      d += seg(a[0], a[1], b[0], b[1]);
      if (dbl_) {
        var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, ox = dbl_[0] - mx, oy = dbl_[1] - my, l = Math.sqrt(ox * ox + oy * oy) || 1;
        ox = ox / l * 4; oy = oy / l * 4;
        dbl += seg(a[0] + ox + (b[0] - a[0]) * 0.18, a[1] + oy + (b[1] - a[1]) * 0.18, b[0] + ox - (b[0] - a[0]) * 0.18, b[1] + oy - (b[1] - a[1]) * 0.18);
      }
    }
    for (var n = B.i(1, 3) - 1; n > 0; n--) {
      for (var tries = 0; tries < 12; tries++) {
        var base = B.pick(rings), a = B.i(0, 5) * Math.PI / 3, c = [base[0] + Rr * Math.sqrt(3) * Math.cos(a), base[1] + Rr * Math.sqrt(3) * Math.sin(a)];
        if (rings.every(function (r) { return dist(r, c) > Rr * 1.6; })) { rings.push(c); break; }
      }
    }
    var arom = B.ch(0.5), deg = {};
    rings.forEach(function (c, ri) {
      for (k = 0; k < 6; k++) {
        var p = vtx(c, k), q = vtx(c, (k + 1) % 6);
        bond(p, q, !(ri === 0 && arom) && k % 2 === 0 ? c : null);
        deg[keyOf(p)] = (deg[keyOf(p)] || 0) + 1;
      }
    });
    var outer = [];
    rings.forEach(function (c) { for (k = 0; k < 6; k++) { var p = vtx(c, k); if (deg[keyOf(p)] === 1) outer.push([p, c]); } });
    for (var s = B.i(2, 3); s > 0 && outer.length; s--) {
      var o = outer.splice(B.i(0, outer.length - 1), 1)[0], p0 = o[0], dir = Math.atan2(p0[1] - o[1][1], p0[0] - o[1][0]), len = B.i(1, 3), side = 1;
      for (i = 0; i < len; i++) {
        var aa = dir + side * Math.PI / 6, p1 = [p0[0] + 16 * Math.cos(aa), p0[1] + 16 * Math.sin(aa)];
        bond(p0, p1, i === len - 1 && B.ch(0.35) ? [p0[0] + 30 * Math.cos(aa + side * 2), p0[1] + 30 * Math.sin(aa + side * 2)] : null);
        p0 = p1; side = -side;
      }
      end.push(p0);
    }
    var xs = [], ys = [];
    Object.keys(bonds).forEach(function (k) { k.split('|').forEach(function (q) { var v = q.split(','); xs.push(+v[0]); ys.push(+v[1]); }); });
    var ox = 160 - (Math.min.apply(null, xs) + Math.max.apply(null, xs)) / 2, oy = 100 - (Math.min.apply(null, ys) + Math.max.apply(null, ys)) / 2;
    var sc = Math.min(1.6, 230 / (Math.max.apply(null, xs) - Math.min.apply(null, xs) + 1), 130 / (Math.max.apply(null, ys) - Math.min.apply(null, ys) + 1));
    B.group('translate(160 100) scale(' + f(sc) + ') rotate(' + f(B.u(-20, 20)) + ') translate(' + f(ox - 160) + ' ' + f(oy - 100) + ')');
    B.p(d, 't-ln', sw(1.6 / sc, 0.9));
    B.p(dbl, 't-ln', sw(1.3 / sc, 0.75));
    if (arom) B.c(rings[0][0], rings[0][1], Rr * 0.55, 't-dm', sw(1.1 / sc, 0.8));
    end.forEach(function (p, i) { B.c(p[0], p[1], 4.4 / sc, i ? 't-ho' : 't-gf', sw(1.4 / sc)); });
    B.end();
  }

  /* uncharted: a contour map with a blank, hatched region; or before/after images with a new crater */
  function mMap(B) {
    var F = field(B, B.i(3, 5)), hx = B.u(90, 230), hy = B.u(60, 140), hr = B.u(30, 42);
    function skip(x, y) { return (x - hx) * (x - hx) + (y - hy) * (y - hy) < (hr - 2) * (hr - 2); }
    for (var l = 1; l <= 5; l++) {
      var lev = F.lo + (F.hi - F.lo) * l / 6, coast = l === 2;
      B.p(iso(F.F, lev, skip), coast ? 't-ln' : 't-dm', sw(coast ? 1.5 : 0.8, coast ? 0.95 : 0.55));
    }
    var h = '';
    for (var t = -hr + 4; t < hr; t += 6) {
      var half = Math.sqrt(hr * hr - t * t) - 2, nx = t / Math.SQRT2, ny = -t / Math.SQRT2;
      h += seg(hx + nx - half / Math.SQRT2, hy + ny - half / Math.SQRT2, hx + nx + half / Math.SQRT2, hy + ny + half / Math.SQRT2);
    }
    B.p(h, 't-dm', sw(0.8, 0.4));
    B.c(hx, hy, hr, 't-gn', sw(1.4, null, { 'stroke-dasharray': '4 3' }));
    B.p('M284 24l4 12h-8z' + ring(284, 36, 10), 't-dm', sw(1, 0.75));
  }
  function mCraters(B) {
    var cs = B.pack(function (x, y) { return Math.min(x - 30, 146 - x, y - 44, 156 - y); }, 5, 20, 400, 7), fresh = null;
    for (var t = 0; t < 60 && !fresh; t++) {
      var x = B.u(44, 132), y = B.u(58, 142), r = B.u(5, 8);
      if (cs.every(function (c) { return dist([x, y], c) > c[2] + r + 4; })) fresh = [x, y, r];
    }
    [0, 138].forEach(function (dx, side) {
      var rim = '', sh = '';
      cs.forEach(function (c) {
        rim += ring(c[0] + dx, c[1], c[2]);
        var r = c[2] * 0.78;
        sh += M(c[0] + dx - r * 0.94, c[1] - r * 0.34) + 'A' + f(r) + ' ' + f(r) + ' 0 0 1 ' + f(c[0] + dx + r * 0.94) + ' ' + f(c[1] - r * 0.34);
      });
      B.rect(28 + dx, 40, 120, 120, 't-dm', sw(1, 0.85));
      B.p(rim, 't-ln', sw(1, 0.75));
      B.p(sh, 't-ln', sw(1.8, 0.45));
      if (side && fresh) { B.c(fresh[0] + dx, fresh[1], fresh[2], 't-gh', sw(1.4)); B.c(fresh[0] + dx, fresh[1], fresh[2] + 7, 't-gn', sw(0.9, 0.8, { 'stroke-dasharray': '2 3' })); }
    });
    B.p(arrow(150, 100, 164, 100, 4), 't-dm', sw(1.2, 0.8));
  }

  /* lost and hidden: a sonar sweep with a hull, or a survey grid with buried structures */
  function mSonar(B) {
    var ox = 160, oy = 188, a0 = Math.PI * 1.13, a1 = Math.PI * 1.87, d = '';
    function P(r, a) { return [ox + r * Math.cos(a), oy + r * Math.sin(a)]; }
    for (var r = 32; r <= 160; r += 32) { var p = P(r, a0), q = P(r, a1); d += M(p[0], p[1]) + 'A' + r + ' ' + r + ' 0 0 1 ' + f(q[0]) + ' ' + f(q[1]); }
    for (var k = 0; k <= 4; k++) { var e = P(160, a0 + (a1 - a0) * k / 4); d += seg(ox, oy, e[0], e[1]); }
    B.p(d, 't-dm', sw(0.8, 0.5));
    var sa = B.u(a0 + 0.3, a1 - 0.3), s1 = P(160, sa), s2 = P(160, sa - 0.28);
    B.p(M(ox, oy) + L(s1[0], s1[1]) + 'A160 160 0 0 0 ' + f(s2[0]) + ' ' + f(s2[1]) + 'Z', 't-lf', { opacity: 0.1 });
    B.p(seg(ox, oy, s1[0], s1[1]), 't-ln', sw(1.4));
    var sp = '', br = '';
    for (k = 0; k < 40; k++) { var q2 = P(B.u(20, 156), B.u(a0, a1)); if (B.ch(0.85)) sp += dot(q2[0], q2[1]); else br += dot(q2[0], q2[1]); }
    B.p(sp, 't-dm', sw(1.6, 0.5));
    B.p(br, 't-ln', sw(3.4, 0.8));
    var w = P(B.u(80, 120), sa - 0.12), ha = B.u(0, Math.PI), L1 = B.u(16, 22), W1_ = B.u(5, 7), c = Math.cos(ha), s = Math.sin(ha);
    B.p(M(w[0] - L1 * c, w[1] - L1 * s) + 'Q' + f(w[0] - W1_ * s * 2) + ' ' + f(w[1] + W1_ * c * 2) + ' ' + f(w[0] + L1 * c) + ' ' + f(w[1] + L1 * s) +
        'Q' + f(w[0] + W1_ * s * 2) + ' ' + f(w[1] - W1_ * c * 2) + ' ' + f(w[0] - L1 * c) + ' ' + f(w[1] - L1 * s) + 'Z' + seg(w[0] - L1 * 0.7 * c, w[1] - L1 * 0.7 * s, w[0] + L1 * 0.7 * c, w[1] + L1 * 0.7 * s), 't-gn', sw(1.4));
  }
  function mSurvey(B) {
    var F = field(B, B.i(4, 6));
    for (var l = 1; l <= 6; l++) B.p(iso(F.F, F.lo + (F.hi - F.lo) * l / 7), 't-dm', sw(0.7, 0.45));
    var d = '', rs = [];
    for (var k = B.i(4, 7); k > 0; k--) {
      var x = B.u(40, 260), y = B.u(34, 150), w = B.u(16, 34), h = B.u(12, 26);
      if (rs.some(function (r) { return x < r[0] + r[2] + 8 && r[0] < x + w + 8 && y < r[1] + r[3] + 8 && r[1] < y + h + 8; })) continue;
      rs.push([x, y, w, h]);
    }
    var hot = B.i(0, rs.length - 1);
    rs.forEach(function (r, i) { if (i !== hot) d += M(r[0], r[1]) + 'h' + f(r[2]) + 'v' + f(r[3]) + 'h' + f(-r[2]) + 'z' + M(r[0] + 4, r[1] + 4) + 'h' + f(r[2] - 8) + 'v' + f(r[3] - 8) + 'h' + f(8 - r[2]) + 'z'; });
    B.p(d, 't-ln', sw(1.2, 0.85));
    if (rs.length) { var r = rs[hot]; B.rect(r[0], r[1], r[2], r[3], 't-gh', sw(1.5)); }
    B.p('M20 20h20M20 20v20' + 'M300 180h-20M300 180v-20', 't-dm', sw(1, 0.6, { 'stroke-dasharray': '2 2' }));
  }

  /* ML robustness: two classes, a decision boundary, a perturbation that crosses it */
  function mBoundary(B) {
    var A = B.u(14, 26), k = TAU / B.u(180, 260), ph = B.u(0, TAU), sl = B.u(-0.25, 0.25), pts = [], pb = [];
    function by(x) { return 100 + A * Math.sin(k * x + ph) + sl * (x - 160); }
    var bx = B.u(100, 220);
    for (var x = 20; x <= 300; x += 8) {
      pts.push([x, by(x)]);
      pb.push([x, by(x) + 9 * Math.exp(-Math.pow((x - bx) / 26, 2))]);
    }
    var o = '', c = '', near = null, nd = 1e9;
    for (var i = 0; i < 30; i++) {
      var px = B.u(28, 292), py = B.u(22, 178), dy = py - by(px);
      if (Math.abs(dy) < 8) continue;
      if (dy < 0) { o += ring(px, py, 3.4); if (Math.abs(px - bx) < 60 && -dy < nd) { nd = -dy; near = [px, py]; } }
      else c += M(px - 3, py - 3) + 'l6 6m0 -6l-6 6';
    }
    B.p(smooth(pts), 't-ln', sw(1.5, 0.9));
    B.p(smooth(pb), 't-gn', sw(1.1, 0.85, { 'stroke-dasharray': '4 3' }));
    B.p(o, 't-ln', sw(1.2, 0.85));
    B.p(c, 't-dm', sw(1.2, 0.85));
    if (near) {
      var tx = near[0] + B.u(-4, 4), ty = by(tx) + 12;
      B.p(arrow(near[0], near[1] + 4, tx, ty - 3, 4), 't-gn', sw(1.3));
      B.c(tx, ty, 3, 't-gf');
    }
  }

  /* planets and moons: a banded planet with orbits and moons */
  function mPlanet(B) {
    var cx = B.u(120, 160), cy = 100, R = B.u(28, 38), bands = '', i;
    B.p(ring(cx, cy, R), 't-ln', sw(1.5));
    for (i = -2; i <= 2; i++) {
      var dy = i * R * 0.32, w = Math.sqrt(R * R - dy * dy);
      bands += M(cx - w, cy + dy) + 'Q' + f(cx) + ' ' + f(cy + dy + 5) + ' ' + f(cx + w) + ' ' + f(cy + dy);
    }
    B.p(bands, 't-dm', sw(0.8, 0.7));
    var tilt = B.u(-16, -4), n = B.i(2, 3), hot = B.i(0, n - 1), moons = '';
    B.group('rotate(' + f(tilt) + ' ' + f(cx) + ' ' + f(cy) + ')');
    for (i = 0; i < n; i++) {
      var rx = R + 26 + i * B.u(24, 34), ry = rx * B.u(0.28, 0.36), a = B.u(0, TAU), mx = cx + rx * Math.cos(a), my = cy + ry * Math.sin(a);
      B.el('ellipse', { cx: f(cx), cy: f(cy), rx: f(rx), ry: f(ry), 'class': 't-dm', 'stroke-width': 0.9, opacity: 0.65, 'stroke-dasharray': '3 3' });
      if (i === hot) { B.c(mx, my, 3.4, 't-gf'); B.c(mx, my, 8, 't-gn', sw(1)); } else moons += dot(mx, my);
    }
    B.p(moons, 't-ln', sw(5));
    B.end();
  }

  /* ecology: a food web in trophic levels */
  function mWeb(B) {
    var lv = B.pick([[5, 4, 2, 1], [4, 3, 2, 1], [5, 3, 3, 1]]), L = [], d = '', ad = '';
    lv.forEach(function (n, l) {
      var col = [], y = 164 - l * 42;
      for (var i = 0; i < n; i++) col.push([160 + (i - (n - 1) / 2) * (220 / Math.max(n, 2)) + B.u(-8, 8), y + B.u(-4, 4)]);
      L.push(col);
    });
    for (var l = 1; l < lv.length; l++) L[l].forEach(function (p) {
      var prey = L[l - 1].slice(), k = Math.min(prey.length, B.i(1, 3));
      for (var j = 0; j < k; j++) {
        var q = prey.splice(B.i(0, prey.length - 1), 1)[0], s = M(q[0], q[1]) + 'Q' + f((p[0] + q[0]) / 2 + B.u(-14, 14)) + ' ' + f((p[1] + q[1]) / 2) + ' ' + f(p[0]) + ' ' + f(p[1]);
        if (l === lv.length - 1) ad += s; else d += s;
      }
    });
    B.p(d, 't-dm', sw(0.9, 0.65));
    B.p(ad, 't-ln', sw(1.1, 0.8));
    var prod = '';
    L[0].forEach(function (p) { prod += M(p[0] - 4, p[1] - 4) + 'h8v8h-8z'; });
    B.p(prod, 't-ln', sw(1.3));
    for (l = 1; l < lv.length - 1; l++) L[l].forEach(function (p) { B.c(p[0], p[1], 4.4, 't-ho', sw(1.4)); });
    var top = L[lv.length - 1][0];
    B.c(top[0], top[1], 5.2, 't-gf');
    B.c(top[0], top[1], 10, 't-gn', sw(1, null, { 'stroke-dasharray': '2 3' }));
  }

  /* chemistry and materials: a crystal lattice with its unit cell, or a honeycomb with a defect */
  function mCrystal(B) {
    var a = B.u(34, 40), nx = 4, ny = 3, nz = 2, ox = 160 - (3 * a + a * 0.5) / 2, oy = 100 + a - 6, d = '', back = '', front = '', bc = B.ch(0.5);
    function P(i, j, k) { return [ox + i * a + k * a * 0.5, oy - j * a * 0.86 - k * a * 0.36]; }
    for (var i = 0; i < nx; i++) for (var j = 0; j < ny; j++) for (var k = 0; k < nz; k++) {
      var p = P(i, j, k);
      if (i < nx - 1) { var q = P(i + 1, j, k); d += seg(p[0], p[1], q[0], q[1]); }
      if (j < ny - 1) { q = P(i, j + 1, k); d += seg(p[0], p[1], q[0], q[1]); }
      if (k < nz - 1) { q = P(i, j, k + 1); d += seg(p[0], p[1], q[0], q[1]); }
      if (k) back += dot(p[0], p[1]); else front += dot(p[0], p[1]);
      if (bc && i < nx - 1 && j < ny - 1 && k < nz - 1) { var c = P(i + 0.5, j + 0.5, k + 0.5); back += dot(c[0], c[1]); }
    }
    B.p(d, 't-dm', sw(0.9, 0.65));
    B.p(back, 't-ln', sw(4, 0.55));
    B.p(front, 't-ln', sw(6.4));
    var ui = B.i(0, nx - 2), uj = B.i(0, ny - 2), e = '';
    [[0, 0, 0, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1],
     [0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 1], [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 1, 1]].forEach(function (s) {
      var p = P(ui + s[0], uj + s[1], s[2]), q = P(ui + s[3], uj + s[4], s[5]); e += seg(p[0], p[1], q[0], q[1]);
    });
    B.p(e, 't-gn', sw(1.6));
  }

  /* engineering and chips: a truss, a chip floorplan, or a wind farm */
  function mTruss(B) {
    var n = B.i(5, 8), x0 = 40, x1 = 280, w = (x1 - x0) / n, yb = 126, yt = 126 - B.u(34, 46), pratt = B.ch(0.4), d = '', jt = '', mem = [];
    function add(a, b, c, e) { mem.push([a, b, c, e]); }
    for (var i = 0; i < n; i++) add(x0 + i * w, yb, x0 + (i + 1) * w, yb);
    if (pratt) {
      for (i = 1; i < n - 1; i++) add(x0 + i * w, yt, x0 + (i + 1) * w, yt);
      for (i = 1; i < n; i++) add(x0 + i * w, yb, x0 + i * w, yt);
      add(x0, yb, x0 + w, yt); add(x1, yb, x1 - w, yt);
      for (i = 1; i < n - 1; i++) if (i < n / 2) add(x0 + i * w, yt, x0 + (i + 1) * w, yb); else add(x0 + i * w, yb, x0 + (i + 1) * w, yt);
    } else {
      for (i = 0; i < n - 1; i++) add(x0 + (i + 0.5) * w, yt, x0 + (i + 1.5) * w, yt);
      for (i = 0; i < n; i++) { add(x0 + i * w, yb, x0 + (i + 0.5) * w, yt); add(x0 + (i + 0.5) * w, yt, x0 + (i + 1) * w, yb); }
    }
    var hot = B.i(n, mem.length - 1);
    mem.forEach(function (m, i) { if (i !== hot) d += seg(m[0], m[1], m[2], m[3]); jt += dot(m[0], m[1]) + dot(m[2], m[3]); });
    B.p(d, 't-ln', sw(1.4, 0.85));
    B.p(seg(mem[hot][0], mem[hot][1], mem[hot][2], mem[hot][3]), 't-gn', sw(2.4));
    B.p(jt, 't-ln', sw(4.4));
    var sup = M(x0, yb + 3) + L(x0 - 7, yb + 14) + L(x0 + 7, yb + 14) + 'Z' + M(x1, yb + 3) + L(x1 - 7, yb + 12) + L(x1 + 7, yb + 12) + 'Z' + ring(x1 - 4, yb + 15, 2.4) + ring(x1 + 4, yb + 15, 2.4);
    for (var g = -10; g <= 10; g += 5) sup += seg(x0 + g, yb + 18, x0 + g - 4, yb + 22) + seg(x1 + g, yb + 20, x1 + g - 4, yb + 24);
    B.p(sup, 't-dm', sw(1, 0.85));
    var ld = '';
    for (i = 0; i < 3; i++) { var lx = x0 + B.u(0.2, 0.8) * (x1 - x0); ld += arrow(lx, yt - 30, lx, yt - 5, 4); }
    B.p(ld, 't-dm', sw(1.1, 0.8));
    B.p(M(x0, 166) + 'H' + x1 + M(x0, 162) + 'v8' + M(x1, 162) + 'v8', 't-dm', sw(0.8, 0.6));
  }
  function mChip(B) {
    var rs = [];
    (function split(x, y, w, h, dep) {
      if (dep > 3 || (dep > 1 && B.ch(0.3)) || w < 34 || h < 26) { rs.push([x, y, w, h]); return; }
      if (w > h * 1.2 || (w > h * 0.8 && B.ch(0.5))) { var c = w * B.u(0.35, 0.65); split(x, y, c, h, dep + 1); split(x + c, y, w - c, h, dep + 1); }
      else { c = h * B.u(0.35, 0.65); split(x, y, w, c, dep + 1); split(x, y + c, w, h - c, dep + 1); }
    })(44, 34, 232, 132, 0);
    var d = '', fill = '', pins = '', wires = '', hot = B.i(0, rs.length - 1);
    rs.forEach(function (r, i) {
      if (i === hot) return;
      var b = M(r[0] + 3, r[1] + 3) + 'h' + f(r[2] - 6) + 'v' + f(r[3] - 6) + 'h' + f(6 - r[2]) + 'z';
      d += b;
      if (B.ch(0.3)) fill += b;
    });
    for (var x = 50; x < 272; x += 9) pins += M(x, 26) + 'v4' + M(x, 170) + 'v4';
    for (var y = 40; y < 162; y += 9) pins += M(36, y) + 'h4' + M(280, y) + 'h4';
    for (var k = 0; k < 4; k++) {
      var a = B.pick(rs), b = B.pick(rs), ax = a[0] + a[2] / 2, ay = a[1] + a[3] / 2, bx = b[0] + b[2] / 2, by_ = b[1] + b[3] / 2;
      wires += M(ax, ay) + 'H' + f(bx) + 'V' + f(by_);
    }
    B.p('M40 30H280V170H40Z', 't-dm', sw(1.2, 0.85));
    B.p(pins, 't-dm', sw(1, 0.6));
    B.p(fill, 't-lf', { opacity: 0.12 });
    B.p(d, 't-ln', sw(1, 0.8));
    B.p(wires, 't-ln', sw(0.8, 0.5, { 'stroke-dasharray': '1 2' }));
    var h = rs[hot];
    B.rect(h[0] + 3, h[1] + 3, h[2] - 6, h[3] - 6, 't-gh', sw(1.5));
  }

  /* neuroscience: a spike raster with a population trace, or a neuron's branching */
  function mNeuron(B) {
    var sx = B.u(120, 200), sy = B.u(86, 116), d = '', tips = [];
    function grow(x, y, a, len, dep) {
      var x2 = x + len * Math.cos(a), y2 = y + len * Math.sin(a), mx = (x + x2) / 2 + B.u(-4, 4), my = (y + y2) / 2 + B.u(-4, 4);
      d += M(x, y) + 'Q' + f(mx) + ' ' + f(my) + ' ' + f(x2) + ' ' + f(y2);
      if (dep >= 4) { tips.push([x2, y2]); return; }
      var sp = B.u(0.3, 0.7);
      grow(x2, y2, a - sp, len * B.u(0.62, 0.8), dep + 1);
      if (B.ch(0.85)) grow(x2, y2, a + sp, len * B.u(0.62, 0.8), dep + 1); else tips.push([x2, y2]);
    }
    var roots = B.i(4, 5), ph = B.u(0, TAU);
    for (var i = 0; i < roots; i++) grow(sx, sy, ph + i * TAU / roots + B.u(-0.3, 0.3), B.u(18, 26), 1);
    var ax = [[sx, sy]], aa = B.u(-0.5, 0.5), x = sx, y = sy;
    for (i = 0; i < 12; i++) { aa += B.u(-0.25, 0.25); x += 12 * Math.cos(aa); y += 12 * Math.sin(aa); ax.push([x, y]); }
    B.p(smooth(ax), 't-dm', sw(1, 0.6, { 'stroke-dasharray': '3 2' }));
    B.p(d, 't-ln', sw(1.1, 0.8));
    B.c(sx, sy, 6.5, 't-lf');
    var t = tips.length ? B.pick(tips) : [sx + 40, sy];
    B.c(t[0], t[1], 3, 't-gf');
    B.c(t[0], t[1], 8, 't-gn', sw(1));
  }

  /* particle physics: a detector cross-section with curling tracks and one jet */
  function mCollision(B) {
    var cx = 160 + B.u(-12, 12), cy = 100, d = '', tr = '', dep = '', jt = '';
    [16, 32, 50, 72].forEach(function (r) { d += ring(cx, cy, r); });
    for (var k = 0; k < 36; k++) { var a = k * TAU / 36; d += seg(cx + 80 * Math.cos(a), cy + 80 * Math.sin(a), cx + 88 * Math.cos(a), cy + 88 * Math.sin(a)); }
    B.p(d, 't-dm', sw(0.8, 0.5));
    var ja = B.u(0, TAU);
    function track(th, rho, into) {
      var x = cx, y = cy, p = [[x, y]];
      while (dist([x, y], [cx, cy]) < 78 && p.length < 60) { x += 3 * Math.cos(th); y += 3 * Math.sin(th); th += 3 / rho; p.push([x, y]); }
      if (into === 'j') jt += poly(p); else tr += poly(p);
      var e = p[p.length - 1], ea = Math.atan2(e[1] - cy, e[0] - cx);
      dep += seg(cx + 81 * Math.cos(ea), cy + 81 * Math.sin(ea), cx + (81 + B.u(3, 10)) * Math.cos(ea), cy + (81 + B.u(3, 10)) * Math.sin(ea));
    }
    for (k = B.i(9, 13); k > 0; k--) track(B.u(0, TAU), B.u(50, 400) * (B.ch(0.5) ? 1 : -1));
    for (k = 0; k < 3; k++) track(ja + B.u(-0.14, 0.14), B.u(300, 900) * (B.ch(0.5) ? 1 : -1), 'j');
    B.p(tr, 't-ln', sw(1, 0.75));
    B.p(dep, 't-ln', sw(4, 0.7, { 'class': 't-ln bt' }));
    B.p(jt, 't-gn', sw(1.2));
    var a1 = ja - 0.24, a2 = ja + 0.24;
    B.p(M(cx, cy) + L(cx + 96 * Math.cos(a1), cy + 96 * Math.sin(a1)) + 'A96 96 0 0 1 ' + f(cx + 96 * Math.cos(a2)) + ' ' + f(cy + 96 * Math.sin(a2)) + 'Z', 't-gn', sw(1, 0.8, { 'stroke-dasharray': '3 3' }));
  }

  /* undescribed life: a cladogram with a new green branch, or a phyllotaxis head */
  function mClade(B) {
    var n = B.i(8, 12), lx = 262, act = [], merges = 0, d = '', step = 200 / (n - 1), leaves = [];
    for (var i = 0; i < n; i++) { var y = 30 + i * (140 / (n - 1)); act.push({ x: lx, y: y, leaf: true }); leaves.push([lx, y]); }
    while (act.length > 1) {
      var k = B.i(0, act.length - 2), a = act[k], b = act[k + 1], px = lx - (++merges) * step * B.u(0.75, 1) - 6;
      px = Math.min(px, a.x - 8, b.x - 8);
      d += M(px, a.y) + 'V' + f(b.y) + M(px, a.y) + 'H' + f(a.x) + M(px, b.y) + 'H' + f(b.x);
      act.splice(k, 2, { x: px, y: (a.y + b.y) / 2 });
    }
    d += M(act[0].x - 12, act[0].y) + 'H' + f(act[0].x);
    B.p(d, 't-ln', sw(1.2, 0.8));
    B.p(leaves.map(function (p) { return dot(p[0], p[1]); }).join(''), 't-ln', sw(4.4));
    var hl = B.pick(leaves.slice(0, n - 1)), bx = hl[0] - B.u(30, 70), ny = hl[1] + 140 / (n - 1) / 2;
    B.p(M(bx, hl[1]) + 'V' + f(ny) + 'H' + f(lx + 16), 't-gn', sw(1.4, null, { 'stroke-dasharray': '3 2' }));
    B.c(lx + 16, ny, 3.6, 't-gf');
  }
  function mPhyllo(B) {
    var cx = 160 + B.u(-50, 50), cy = 100, c = B.u(6.4, 7.6), ga = 2.39996, rot = B.u(0, TAU), bins = ['', '', ''], n = 92, hot = B.i(40, 80), hp = null;
    for (var i = 1; i < n; i++) {
      var r = c * Math.sqrt(i), a = i * ga + rot, x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
      if (i === hot) hp = [x, y]; else bins[i < 30 ? 0 : i < 62 ? 1 : 2] += dot(x, y);
    }
    B.p(bins[0], 't-ln', sw(3, 0.7));
    B.p(bins[1], 't-ln', sw(4.4, 0.85));
    B.p(bins[2], 't-ln', sw(5.8));
    B.c(hp[0], hp[1], 3, 't-gf');
    B.c(hp[0], hp[1], 8, 't-gn', sw(1.2));
  }

  /* crypto math: an elliptic curve over a lattice with the chord rule, or a curve over a finite field */
  function mCurve(B) {
    var a = B.u(-3, -1), b = B.u(0.6, 2.2), X = function (x) { return 160 + x * 44; }, Y = function (y) { return 100 - y * 20; };
    var lat = '';
    for (var gx = 20; gx <= 300; gx += 20) for (var gy = 20; gy <= 180; gy += 20) lat += dot(gx, gy);
    B.p(lat, 't-dm', sw(1.6, 0.45));
    B.p('M20 100H300M160 20V180', 't-dm', sw(0.7, 0.5));
    function rhs(x) { return x * x * x + a * x + b; }
    var comps = [], cur = null;
    for (var x = -2.9; x <= 3.2; x += 0.01) {
      if (rhs(x) >= 0) { if (!cur) { cur = []; comps.push(cur); } cur.push(x); } else cur = null;
    }
    var d = '';
    comps.forEach(function (c) {
      var lo = c.map(function (x) { return [X(x), Y(-Math.sqrt(rhs(x)))]; }).reverse(), up = c.map(function (x) { return [X(x), Y(Math.sqrt(rhs(x)))]; });
      var bounded = c[c.length - 1] < 3.1;
      d += poly(lo.concat(up), bounded);
    });
    B.p(d, 't-ln', sw(1.6, 0.9));
    var main = comps[comps.length - 1];
    for (var t = 0; t < 12; t++) {
      var x1 = main[0] + B.u(0.05, 0.8), x2 = main[0] + B.u(0.9, 1.7), y1 = Math.sqrt(rhs(x1)) * (B.ch(0.5) ? 1 : -1), y2 = Math.sqrt(rhs(x2));
      var lam = (y2 - y1) / (x2 - x1), x3 = lam * lam - x1 - x2, y3 = lam * (x1 - x3) - y1;
      if (x3 > -2.8 && x3 < 3.2 && Math.abs(y3) < 4.2 && Math.abs(x3 - x1) > 0.25 && Math.abs(x3 - x2) > 0.25) {
        var xs = [x1, x2, x3], lx = Math.min.apply(null, xs) - 0.3, hx = Math.max.apply(null, xs) + 0.3;
        B.p(seg(X(lx), Y(y1 + lam * (lx - x1)), X(hx), Y(y1 + lam * (hx - x1))), 't-dm', sw(1, 0.85, { 'stroke-dasharray': '4 3' }));
        B.p(M(X(x3), Y(-y3)) + 'V' + f(Y(y3)), 't-gn', sw(1, 0.85, { 'stroke-dasharray': '2 3' }));
        B.p(dot(X(x1), Y(y1)) + dot(X(x2), Y(y2)) + dot(X(x3), Y(-y3)), 't-ln', sw(5));
        B.c(X(x3), Y(y3), 3.4, 't-gf');
        B.c(X(x3), Y(y3), 8, 't-gn', sw(1.2));
        break;
      }
    }
  }

  /* ---------------- record tables: four layouts, picked from the title */
  function tGrid(B, x0, y0, cols, rows, cw, rh, skip) {
    var g = '', r, c;
    for (r = 0; r <= rows; r++) g += M(x0, y0 + r * rh) + 'h' + f(cols * cw);
    for (c = 0; c <= cols; c++) if (!skip || skip !== c) g += M(x0 + c * cw, y0) + 'v' + f(rows * rh);
    B.p(g, 't-dm', sw(0.7, 0.6));
    B.p(M(x0, y0 + rh) + 'h' + f(cols * cw) + M(x0 + cw, y0) + 'v' + f(rows * rh), 't-ln', sw(1.4, 0.9));
  }
  function tHeads(x0, y0, cols, rows, cw, rh) {
    var d = '', r, c;
    for (c = 1; c < cols; c++) d += M(x0 + c * cw + cw / 2 - 4, y0 + rh / 2) + 'h8';
    for (r = 1; r < rows; r++) d += M(x0 + cw / 2 - 4, y0 + r * rh + rh / 2) + 'h8';
    return d;
  }
  /* bounds: each cell holds an interval lo..hi; most are closed or nearly so, the green one is the widest gap */
  function tBounds(B) {
    var cols = B.i(5, 7), rows = B.i(5, 6), cw = Math.min(B.u(34, 48), 262 / cols), rh = 21;
    var x0 = 160 - cols * cw / 2, y0 = 100 - rows * rh / 2, closed = '', lo = '', gaps = '', cells = [], r, c;
    tGrid(B, x0, y0, cols, rows, cw, rh);
    B.p(tHeads(x0, y0, cols, rows, cw, rh), 't-ln', sw(2.4, 0.9));
    for (r = 1; r < rows; r++) for (c = 1; c < cols; c++) {
      var x = x0 + c * cw + 5, y = y0 + r * rh + rh / 2, w = cw - 10;
      if (B.ch(0.45)) { closed += M(x, y) + 'h' + f(w * B.u(0.35, 0.8)); continue; }
      var a = w * B.u(0.2, 0.4), g = w * B.u(0.08, 0.3);
      lo += M(x, y) + 'h' + f(a) + M(x + a + g, y) + 'h' + f(Math.max(2, w - a - g - 2));
      gaps += M(x + a + 1.5, y) + 'h' + f(Math.max(0, g - 3));
      cells.push([r, c, g]);
    }
    B.p(closed, 't-ln', sw(2.6, 0.75, { 'class': 't-ln bt' }));
    B.p(lo, 't-ln', sw(2.6, 0.75, { 'class': 't-ln bt' }));
    B.p(gaps, 't-dm', sw(1, 0.8, { 'stroke-dasharray': '1 2' }));
    if (!cells.length) cells.push([1, 1, 0]);
    var h = B.pick(cells), hx = x0 + h[1] * cw, hy = y0 + h[0] * rh;
    B.rect(hx + 1.5, hy + 1.5, cw - 3, rh - 3, 't-gh', sw(0.8, 0.9));
    B.p(M(hx + 9, hy + 5) + 'h-3v' + f(rh - 10) + 'h3' + M(hx + cw - 9, hy + 5) + 'h3v' + f(rh - 10) + 'h-3', 't-gn', sw(1.6));
  }
  /* triangular n x k table (codes, arcs, Ramsey numbers): only k <= n is defined, so the empty half is a staircase */
  function tTri(B) {
    var cols = B.i(7, 10), rows = B.i(5, 7), cw = Math.min(B.u(24, 32), 262 / cols), rh = 19;
    var x0 = 160 - cols * cw / 2, y0 = 100 - rows * rh / 2, bars = '', st = '', diag = [], r, c, off = B.i(0, 1);
    tGrid(B, x0, y0, cols, rows, cw, rh);
    B.p(tHeads(x0, y0, cols, rows, cw, rh), 't-ln', sw(2.4, 0.9));
    for (r = 1; r < rows; r++) {
      var first = Math.min(cols - 1, r + off);
      st += (r === 1 ? M(x0 + cw, y0 + rh) : '') + 'H' + f(x0 + first * cw) + 'V' + f(y0 + (r + 1) * rh);
      for (c = first; c < cols; c++) {
        var x = x0 + c * cw + 4, y = y0 + r * rh + rh / 2;
        bars += M(x, y) + 'h' + f((cw - 8) * B.u(0.4, 1));
      }
      diag.push([r, first]);
    }
    var fill = M(x0 + cw, y0 + rh) + st.replace(/^M[^H]*/, '') + 'H' + f(x0 + cw) + 'Z';
    B.p(fill, 't-df', { opacity: 0.16 });
    B.p(st, 't-ln', sw(1.6, 0.9));
    B.p(bars, 't-ln', sw(2.6, 0.75, { 'class': 't-ln bt' }));
    var h = B.pick(diag);
    B.rect(x0 + h[1] * cw + 1.5, y0 + h[0] * rh + 1.5, cw - 3, rh - 3, 't-gh', sw(1.4));
  }
  /* frontier: everything known is filled up to a jagged edge; the green cell is the first one past it */
  function tFront(B) {
    var cols = B.i(10, 13), rows = B.i(6, 7), s = Math.min(19, 250 / cols), x0 = 160 - cols * s / 2, y0 = 100 - rows * s / 2;
    var fr = [], k = cols - B.i(0, 2), r, c, a = '', b = '', e = '', st = '';
    for (r = 0; r < rows; r++) { fr.push(Math.max(1, k)); k -= B.pick([0, 1, 1, 2, 3]); }
    for (r = 0; r < rows; r++) for (c = 0; c < cols; c++) {
      var x = x0 + c * s, y = y0 + r * s;
      if (c < fr[r]) { if ((r * 7 + c * 3) % 5 < 2) a += sq(x + 1.5, y + 1.5, s - 3); else b += sq(x + 1.5, y + 1.5, s - 3); }
      else e += dot(x + s / 2, y + s / 2);
    }
    for (r = 0; r < rows; r++) st += (r ? 'H' + f(x0 + fr[r] * s) : M(x0 + fr[0] * s, y0)) + 'V' + f(y0 + (r + 1) * s);
    B.p(b, 't-lf', { opacity: 0.38 });
    B.p(a, 't-lf', { opacity: 0.75 });
    B.p(e, 't-dm', sw(1.8, 0.7));
    B.p(st, 't-ln', sw(1.8));
    var cand = [];
    for (r = 0; r < rows; r++) if (fr[r] < cols) cand.push(r);
    var hr = cand.length ? B.pick(cand) : rows - 1, hc = Math.min(cols - 1, fr[hr]);
    B.rect(x0 + hc * s + 1, y0 + hr * s + 1, s - 2, s - 2, 't-gh', sw(1.4, null, { 'stroke-dasharray': '3 2' }));
  }
  /* heat strip: a wide table of values shaded in three steps, one cell still blank */
  function tHeat(B) {
    var cols = B.i(12, 15), rows = B.i(4, 5), s = Math.min(19, 262 / (cols + 1)), x0 = 160 - (cols + 1) * s / 2, y0 = 100 - rows * s / 2;
    var L3 = ['', '', ''], hd = '', blank = [], r, c, tr = B.u(-0.25, 0.25);
    for (r = 0; r < rows; r++) {
      hd += M(x0 + 3, y0 + r * s + s / 2) + 'h' + f(s - 8);
      for (c = 0; c < cols; c++) {
        var x = x0 + (c + 1) * s, y = y0 + r * s, v = 0.5 + 0.35 * Math.sin(c * 0.6 + r * 1.3 + tr * 9) + B.u(-0.3, 0.3);
        if (B.ch(0.07)) { blank.push([r, c]); continue; }
        L3[v < 0.4 ? 0 : v < 0.75 ? 1 : 2] += sq(x + 1, y + 1, s - 2);
      }
    }
    B.p(L3[0], 't-lf', { opacity: 0.22 });
    B.p(L3[1], 't-lf', { opacity: 0.5 });
    B.p(L3[2], 't-lf', { opacity: 0.88 });
    B.p(hd, 't-ln', sw(2.4, 0.9));
    B.p(M(x0, y0 - 6) + 'h' + f((cols + 1) * s) + ticks(x0 + s, x0 + (cols + 1) * s, y0 - 6, s, -3), 't-dm', sw(1, 0.75));
    var h = blank.length ? B.pick(blank) : [B.i(0, rows - 1), B.i(0, cols - 1)];
    B.rect(x0 + (h[1] + 1) * s + 1, y0 + h[0] * s + 1, s - 2, s - 2, 't-gh', sw(1.5));
  }
  function mTable(B, t) {
    var k;
    if (/\(n,|\ba\(n|\br\(|\barcs?\b|ramsey|covering|\bcodes?\b|design|ternary|binary/.test(t)) k = B.ch(0.45) ? 1 : B.pick([0, 2, 3]);
    else if (/bound|lower|upper|interval|gap|between/.test(t)) k = B.ch(0.6) ? 0 : B.pick([1, 2, 3]);
    else k = B.pick([0, 1, 2, 3]);
    [tBounds, tTri, tFront, tHeat][k](B);
  }

  /* ---------------- compression: bytes squeezed through a funnel; code golf: a listing with one line cut shorter */
  function mSqueeze(B) {
    var n1 = B.i(24, 30), n2 = B.i(11, 16), s1 = Math.min(9, 256 / n1), s2 = s1 * B.u(1, 1.15), w1 = n1 * s1, w2 = n2 * s2;
    var x1 = 160 - w1 / 2, x2 = 160 - w2 / 2 + B.u(-30, 30), y1 = 36, y2 = 148, lit = '', off = '', out = '', fun = '', i;
    for (i = 0; i < n1; i++) { var q = sq(x1 + i * s1 + 0.8, y1, s1 - 1.6); if (B.ch(0.45)) lit += q; else off += q; }
    var keep = B.i(2, 4);
    for (i = 0; i < n2 - keep; i++) out += sq(x2 + i * s2 + 0.8, y2, s2 - 1.6);
    var k = B.i(3, 5);
    for (i = 0; i < k; i++) {
      var u = i / (k - 1), a = x1 + u * w1, b = x2 + u * w2, ym = (y1 + y2) / 2 + B.u(-8, 8);
      fun += M(a, y1 + s1 + 4) + 'C' + f(a) + ' ' + f(ym) + ' ' + f(b) + ' ' + f(ym) + ' ' + f(b) + ' ' + f(y2 - 5);
    }
    B.p(fun, 't-dm', sw(1, 0.75, { 'stroke-dasharray': '3 3' }));
    B.p(off, 't-ln', sw(1, 0.75));
    B.p(lit, 't-lf', { opacity: 0.75 });
    B.p(out, 't-lf', { opacity: 0.85 });
    var gx = x2 + (n2 - keep) * s2;
    B.p(Array.apply(null, Array(keep)).map(function (_, j) { return sq(gx + j * s2 + 0.8, y2, s2 - 1.6); }).join(''), 't-gh', sw(1.2, null, { 'stroke-dasharray': '2 1.5' }));
    B.p(M(gx, y2 + s2 + 6) + 'v3H' + f(gx + keep * s2) + 'v-3', 't-gn', sw(1.3));
  }
  function mGolf(B) {
    var n = B.i(5, 6), lines = [], i, j, d = '', g = '', strike = '', gut = '', longest = 0, best = 0;
    for (i = 0; i < n; i++) {
      var ind = B.ch(0.4) && i ? B.pick([12, 24]) : 0, x = 52 + ind, toks = [], k = B.i(2, 5);
      for (j = 0; j < k; j++) { var w = B.u(10, 34); toks.push([x, w]); x += w + 7; }
      lines.push(toks);
      if (x > best) { best = x; longest = i; }
    }
    var y0 = 100 - n * 11, row = 0;
    lines.forEach(function (toks, li) {
      var y = y0 + row * 22;
      gut += dot(38, y);
      toks.forEach(function (tk) { d += M(tk[0], y) + 'h' + f(tk[1]); });
      row++;
      if (li !== longest) return;
      var end = toks[toks.length - 1][0] + toks[toks.length - 1][1];
      strike += M(toks[0][0] - 5, y) + 'H' + f(end + 5);
      /* the rewrite: the same line with fewer, shorter tokens */
      var gy = y0 + row * 22, gx = toks[0][0], m = Math.max(1, toks.length - B.i(1, 2));
      for (j = 0; j < m; j++) { var w2 = toks[j][1] * B.u(0.45, 0.8); g += M(gx, gy) + 'h' + f(w2); gx += w2 + 7; }
      gut += dot(38, gy);
      row++;
    });
    B.p(gut, 't-dm', sw(2.2, 0.7));
    B.p(M(45, y0 - 12) + 'V' + f(y0 + (row - 1) * 22 + 12), 't-dm', sw(0.8, 0.6));
    B.p(d, 't-ln', sw(7, 0.6));
    B.p(strike, 't-dm', sw(1.6, 0.95));
    B.p(g, 't-gn', sw(7, 0.9));
    var gyy = y0 + (longest + 1) * 22;
    B.p(M(30, gyy - 6) + 'v12', 't-gn', sw(1.6));
  }
  function mBars(B, t) { return (/golf|shortest|shorter|bytes|brainfuck|loda|metamath|program|proof/.test(t) ? mGolf : mSqueeze)(B); }

  /* ---------------- spectrogram: time across, frequency up; each call is a fundamental with stacked harmonics */
  function mSpectro(B, t) {
    t = t || '';
    var kind = /sperm|coda|click|echoloc/.test(t) ? 'click' : /elephant|rumble|whale|infrasound/.test(t) ? 'low' :
      /dolphin|whistle/.test(t) ? 'whistle' : /bird|song|chirp|frog|insect|\bbat\b/.test(t) ? 'chirp' : B.pick(['whistle', 'chirp', 'chirp']);
    var y0 = 170, i, noise = '', ty = '';
    for (i = 0; i < B.i(44, 58); i++) { var nx = B.u(34, 288), ny = B.u(40, 166); noise += M(nx, ny) + 'v' + f(B.u(2, 6)); }
    for (i = 0; i < 6; i++) ty += M(26, y0 - i * 24) + 'h5';
    B.p(M(31, 26) + 'V' + y0 + 'H292', 't-dm', sw(1, 0.8));
    B.p(ty, 't-dm', sw(1, 0.8));
    B.p(noise, 't-dm', sw(2, 0.22, { 'class': 't-dm bt' }));
    var H = [['', 2.4, 0.95], ['', 1.8, 0.7], ['', 1.2, 0.5], ['', 0.8, 0.35]], calls = [], x = B.u(40, 60);
    function contour(pts, n) {           /* pts: [x, fundamental height]; n harmonics, exact multiples */
      for (var h = 1; h <= n; h++) {
        if (pts.some(function (p) { return p[1] * h > 138; })) break;
        H[Math.min(h - 1, 3)][0] += smooth(pts.map(function (p) { return [p[0], y0 - p[1] * h]; }));
      }
    }
    if (kind === 'click') {
      var clicks = '';
      while (x < 262) {
        var n = B.i(4, 6), gx = x;
        for (i = 0; i < n; i++) { clicks += M(gx, y0 - 4) + 'V' + f(B.u(48, 70)); gx += B.pick([7, 7, 11, 16]); }
        calls.push([x - 3, gx - 4]);
        x = gx + B.u(26, 44);
      }
      B.p(clicks, 't-ln', sw(1.8, 0.9));
    } else {
      while (x < 250) {
        var dur, pts = [], u;
        if (kind === 'low') {
          dur = B.u(70, 110); var lf = B.u(9, 13), wob = B.u(1, 3);
          for (u = 0; u <= 1.001; u += 0.1) pts.push([x + u * dur, lf + wob * Math.sin(u * Math.PI)]);
          contour(pts, 6);
        } else if (kind === 'whistle') {
          dur = B.u(42, 60); var f0 = B.u(22, 34), up = B.u(16, 26), shape = B.i(0, 2);
          for (u = 0; u <= 1.001; u += 0.1) pts.push([x + u * dur, f0 + up * (shape === 0 ? u * u : shape === 1 ? Math.sin(u * Math.PI) : 0.5 + 0.5 * Math.sin(u * 5))]);
          contour(pts, 3);
        } else {
          var m = B.i(3, 4), cx = x; dur = 0;
          for (var j = 0; j < m; j++) {
            var cd = B.u(8, 13), top = B.u(34, 50), p2 = [];
            for (u = 0; u <= 1.001; u += 0.25) p2.push([cx + u * cd, top - (top - 22) * u]);
            contour(p2, 2);
            cx += cd + B.u(4, 8);
          }
          dur = cx - x;
        }
        calls.push([x, x + dur]);
        x += dur + B.u(18, 34);
      }
      for (i = 3; i >= 0; i--) B.p(H[i][0], 't-ln', sw(H[i][1], H[i][2]));
    }
    var c = calls.length > 1 ? calls[B.i(1, calls.length - 1)] : calls[0];
    if (c) B.p(M(c[0], 36) + 'v-5H' + f(c[1]) + 'v5', 't-gn', sw(1.5));
  }

  /* ---------------- genomics: a genome browser, a read pileup with a variant, assembly contigs, or binning clusters */
  function gBrowser(B) {
    var vx = B.u(150, 250), rul = M(30, 30) + 'H290', ex = '', intr = '', reads = '', hm = '', mis = '', cov = [], dir = B.ch(0.5) ? 1 : -1;
    for (var x = 30; x <= 290; x += 13) rul += M(x, 30) + 'v' + ((x - 30) % 52 ? 3 : 6);
    B.p(rul, 't-dm', sw(0.9, 0.7));
    [[52, B.u(36, 70), B.u(220, 284)], [76, B.u(60, 140), B.u(200, 270)]].forEach(function (g, gi) {
      var y = g[0], a = g[1], b = g[2], nEx = B.i(3, 9), step = (b - a) / nEx, s = gi ? -dir : dir;
      intr += M(a, y) + 'H' + f(b);
      for (var c = a + 12; c < b - 6; c += 20) intr += M(c - 2 * s, y - 3) + 'l' + (2 * s) + ' 3l' + (-2 * s) + ' 3';
      for (var e = 0; e < nEx; e++) {
        var w = step * B.u(0.25, 0.6), xx = a + e * step + B.u(0, step - w);
        ex += M(xx, y - (gi ? 4 : 5)) + 'h' + f(w) + 'v' + (gi ? 8 : 10) + 'h' + f(-w) + 'z';
      }
    });
    for (var r = 0; r < 6; r++) {
      var y = 98 + r * 9, x2 = 30 + B.u(0, 24);
      while (x2 < 278) {
        var w2 = Math.min(B.u(26, 54), 290 - x2);
        reads += M(x2, y) + 'h' + f(w2);
        if (x2 < vx && vx < x2 + w2 && B.ch(0.8)) hm += M(vx - 1.3, y) + 'h2.6';
        else if (B.ch(0.25)) { var mx = x2 + B.u(2, w2 - 2); mis += M(mx - 1, y) + 'h2'; }
        x2 += w2 + B.u(3, 10);
      }
    }
    for (x = 30; x <= 290; x += 5) cov.push([x, 162 - 6 * Math.sin(x * 0.05 + vx) - 4 * B.r() - (Math.abs(x - vx) < 8 ? 8 : 0)]);
    B.p(intr, 't-dm', sw(1, 0.8));
    B.p(ex, 't-lf', { opacity: 0.7 });
    B.p(reads, 't-dm', sw(3.4, 0.55, { 'class': 't-dm bt' }));
    B.p(mis, 't-ln', sw(3.4, 0.9, { 'class': 't-ln bt' }));
    B.p(poly(cov), 't-ln', sw(1.1, 0.8));
    B.rect(vx - 4.5, 90, 9, 58, 't-gh', sw(1));
    B.p(hm, 't-gn', sw(3.4, null, { 'class': 't-gn bt' }));
  }
  function gPileup(B) {
    var ref = '', rd = '', mm = '', base = 40, step = 7, n = 34, vc = B.i(14, 28), vx = base + vc * step + step / 2, i;
    for (i = 0; i < n; i++) ref += M(base + i * step + 1.5, 40) + 'h' + f(step - 3);
    B.p(ref, 't-ln', sw(4, 0.8, { 'class': 't-ln bt' }));
    B.p(ticks(base, base + n * step, 50, step * 5, 3), 't-dm', sw(1, 0.7));
    var rows = B.i(10, 12), hits = 0;
    for (var r = 0; r < rows; r++) {
      var y = 62 + r * 8.5, s = B.i(0, 14), len = B.i(10, 20);
      if (s + len > n) s = n - len;
      rd += M(base + s * step + 1, y) + 'H' + f(base + (s + len) * step - 1);
      if (s <= vc && vc < s + len && hits < 6 && B.ch(0.75)) { mm += M(vx, y - 3) + 'v6'; hits++; }
      else if (B.ch(0.2)) { var mc = s + B.i(1, len - 2); mm += M(base + mc * step + step / 2, y - 3) + 'v6'; }
    }
    B.p(rd, 't-dm', sw(4, 0.55));
    B.p(mm, 't-ln', sw(2, 0.95, { 'class': 't-ln bt' }));
    B.rect(vx - 5, 32, 10, 62 + rows * 8.5 - 28, 't-gn', sw(1.3, null, { 'stroke-dasharray': '3 2' }));
  }
  /* assembly: contigs laid along one scaffold, read pairs bridging the gaps; the green bracket is a gap still open */
  function gAssembly(B) {
    var y = 120, x = 34, cs = [], d = '', arcs = '', reads = '', i;
    while (x < 270) { var w = B.u(22, 60); if (x + w > 290) w = 290 - x; cs.push([x, x + w]); x += w + B.u(8, 18); }
    for (i = 1; i < cs.length; i++) {
      var p = cs[i - 1], c = cs[i], k = B.i(1, 3);
      for (var j = 0; j < k; j++) {
        var a = B.u(Math.max(p[0], p[1] - 22), p[1] - 4), b = B.u(c[0] + 4, Math.min(c[1], c[0] + 22)), h = B.u(18, 46);
        arcs += M(a, y - 7) + 'C' + f(a) + ' ' + f(y - 7 - h) + ' ' + f(b) + ' ' + f(y - 7 - h) + ' ' + f(b) + ' ' + f(y - 7);
      }
    }
    cs.forEach(function (c) {
      d += M(c[0], y) + 'H' + f(c[1]);
      for (var r = 0; r < 3; r++) { var rx = B.u(c[0], Math.max(c[0], c[1] - 14)); reads += M(rx, y + 14 + r * 7) + 'h' + f(Math.min(14, c[1] - rx)); }
    });
    B.p(arcs, 't-dm', sw(1, 0.8, { 'stroke-dasharray': '3 3' }));
    B.p(reads, 't-dm', sw(3, 0.55, { 'class': 't-dm bt' }));
    B.p(d, 't-ln', sw(8, 0.8, { 'class': 't-ln bt' }));
    B.p(M(34, 160) + 'H290' + ticks(34, 290, 160, 32, 3), 't-dm', sw(1, 0.7));
    if (cs.length > 1) {
      var g = B.i(1, cs.length - 1), gx0 = cs[g - 1][1] + 2, gx1 = cs[g][0] - 2;
      B.rect(gx0, y - 6, gx1 - gx0, 12, 't-gh', sw(1.3, null, { 'stroke-dasharray': '2 2' }));
    }
  }
  function gBins(B) {
    var k = B.i(5, 7), cs = B.scatter(k, 66, 270, 44, 146, 50), dots = '', i;
    B.p('M36 24V164H296', 't-dm', sw(1, 0.8));
    cs.forEach(function (c) {
      c.push(B.u(9, 18), B.u(7, 14), B.u(0, TAU));
      for (i = 0; i < B.i(9, 16); i++) {
        var a = B.u(0, TAU), r = Math.sqrt(B.r());
        dots += dot(c[0] + c[2] * r * Math.cos(a), c[1] + c[3] * r * Math.sin(a));
      }
    });
    for (i = 0; i < 14; i++) dots += dot(B.u(44, 290), B.u(30, 158));
    B.p(dots, 't-ln', sw(3.2, 0.6));
    var ok = cs.filter(function (c) { return !(c[0] < 150 && c[1] > 130); }), h = ok.length ? B.pick(ok) : cs[0];
    if (h) B.p(M(h[0] - h[2] - 6, h[1]) + 'a' + f(h[2] + 6) + ' ' + f(h[3] + 6) + ' 0 1 0 ' + f(2 * h[2] + 12) + ' 0a' + f(h[2] + 6) + ' ' + f(h[3] + 6) + ' 0 1 0 ' + f(-2 * h[2] - 12) + ' 0',
      't-gn', sw(1.4, null, { 'stroke-dasharray': '4 2.5' }));
  }
  function mGenome(B, t) {
    if (/binning|profil|metagenom|taxonom|microbiom|abundance|ortholog/.test(t) && !/assembl/.test(t)) return gBins(B);
    if (/assembl|contig|scaffold|diploid|telomere/.test(t)) return gAssembly(B);
    if (/somatic|variant|\bsnv|indel|calling|truth|correct/.test(t)) return B.ch(0.7) ? gPileup(B) : gBrowser(B);
    return [gBrowser, gPileup, gAssembly, gBins][B.i(0, 3)](B);
  }

  /* ---------------- sky archives: a star field with spikes and a reticle, plus the signal the title is after */
  function starField(B, y1, n) {
    var a = '', b = '', c = [], spk = '', i;
    for (i = 0; i < n; i++) {
      var x = B.u(18, 302), y = B.u(16, y1), r = B.r();
      if (r < 0.55) a += dot(x, y); else if (r < 0.88) b += dot(x, y); else c.push([x, y]);
    }
    c.slice(0, 3).forEach(function (p) { spk += M(p[0] - 6, p[1]) + 'h12' + M(p[0], p[1] - 6) + 'v12'; });
    B.p(a, 't-dm', sw(2, 0.7));
    B.p(b, 't-dm', sw(3.6, 0.9));
    B.p(spk, 't-ln', sw(0.9, 0.7));
    B.p(c.map(function (p) { return dot(p[0], p[1]); }).join(''), 't-ln', sw(5.6));
  }
  function reticle(B, x, y, r) {
    B.c(x, y, r, 't-gn', sw(1.3));
    B.p(M(x - r - 6, y) + 'h5' + M(x + r + 1, y) + 'h5' + M(x, y - r - 6) + 'v5' + M(x, y + r + 1) + 'v5', 't-gn', sw(1.3));
  }
  function mSky(B, t) {
    var kind = /microlens/.test(t) ? 'lens' : /\bfrb|fast radio|burst|gamma|counterpart|outburst|nova/.test(t) ? 'frb' :
      /proper motion|brown dwarf|companion|\bt or y|common proper|hipparcos|astrometr/.test(t) ? 'pm' :
      /asteroid|precover|comet|near-earth|\bneo\b|trans-neptun|minor planet/.test(t) ? 'track' :
      /transit|eclips|kepler|tess|planet|triple|timing/.test(t) ? 'dip' : B.pick(['dip', 'var', 'lens', 'var']);
    var full = kind === 'pm' || kind === 'track';
    starField(B, full ? 182 : 108, full ? B.i(28, 34) : B.i(24, 30));
    var x, y, pts = [], i;
    if (kind === 'pm') {
      x = B.u(90, 220); y = B.u(50, 110);
      var dx = B.u(18, 28) * (B.ch(0.5) ? 1 : -1), dy = B.u(-14, 14);
      B.p(dot(x - 2 * dx, y - 2 * dy) + dot(x - dx, y - dy), 't-ln', sw(4, 0.45));
      B.p(arrow(x - 2 * dx, y - 2 * dy, x - dx * 0.25, y - dy * 0.25, 4), 't-dm', sw(1.1, 0.9, { 'stroke-dasharray': '3 2.5' }));
      B.c(x, y, 2.8, 't-gf');
      reticle(B, x, y, 8);
      return;
    }
    if (kind === 'track') {
      var x0 = B.u(30, 70), y0 = B.u(40, 150), x1 = B.u(250, 290), y1 = B.u(30, 120), cy = Math.min(y0, y1) - B.u(10, 40), tr = '';
      for (i = 0; i <= 10; i++) {
        var u = i / 10, px = (1 - u) * (1 - u) * x0 + 2 * u * (1 - u) * ((x0 + x1) / 2) + u * u * x1, py = (1 - u) * (1 - u) * y0 + 2 * u * (1 - u) * cy + u * u * y1;
        pts.push([px, py]);
        if (i < 9) tr += dot(px, py);
      }
      B.p(smooth(pts), 't-dm', sw(0.8, 0.6, { 'stroke-dasharray': '2 4' }));
      B.p(tr, 't-ln', sw(3.2, 0.8));
      reticle(B, pts[9][0], pts[9][1], 7);
      return;
    }
    x = B.u(70, 250); y = B.u(34, 96);
    B.c(x, y, 2.8, 't-gf');
    reticle(B, x, y, 8);
    var base = 132, per = B.u(48, 72), ph = B.u(0, per), obs = '', mark = null;
    var spikes = [];
    if (kind === 'frb') { var sx = B.u(50, 80); while (sx < 280) { spikes.push(sx); sx += B.u(22, 70); } }
    var c0 = B.u(130, 220), wdt = B.u(10, 18);
    for (var xx = 30; xx <= 290; xx += 2) {
      var tt = ((xx - ph) % per + per) % per, yy = base, n = B.u(-1.5, 1.5);
      if (kind === 'dip') yy = base + (Math.abs(tt - per / 2) < 5 ? 16 : 0);
      else if (kind === 'var') yy = base + 9 * Math.sin(TAU * tt / per) + 3 * Math.sin(2 * TAU * tt / per);
      else if (kind === 'lens') { var q = (xx - c0) / wdt; yy = base + 14 - 34 / Math.sqrt(1 + q * q * 3); }
      else if (kind === 'frb') { yy = base + 10; spikes.forEach(function (s, j) { if (Math.abs(xx - s) < 2) yy = base + 10 - (j % 2 ? 22 : 34); }); }
      pts.push([xx, yy]);
      if (xx % 6 === 0) obs += dot(xx, yy + n);
      if (!mark && kind === 'dip' && xx > 160 && Math.abs(tt - per / 2) < 1.1) mark = [xx, base + 22];
    }
    if (kind === 'lens') mark = [c0, base - 24];
    if (kind === 'frb') mark = [spikes[spikes.length - 1], base - 28];
    if (kind === 'var') mark = [pts[B.i(70, 120)][0], base + 16];
    B.p(M(30, 166) + 'H290' + ticks(30, 290, 166, 26, -3), 't-dm', sw(0.9, 0.7));
    B.p(obs, 't-dm', sw(2, 0.6));
    B.p(kind === 'frb' || kind === 'dip' ? poly(pts) : smooth(pts.filter(function (p, j) { return j % 2 === 0; })), 't-ln', sw(1.4, 0.9));
    if (mark) B.p(M(mark[0] - 9, mark[1]) + 'h18' + M(mark[0] - 9, mark[1] - 3) + 'v6' + M(mark[0] + 9, mark[1] - 3) + 'v6', 't-gn', sw(1.4));
  }

  /* ---------------- Life: known still lifes, oscillators and a glider with its last two positions */
  var LIFE = {
    glider: [[0, 1], [1, 2], [2, 0], [2, 1], [2, 2]],
    lwss: [[0, 1], [0, 4], [1, 0], [2, 0], [2, 4], [3, 0], [3, 1], [3, 2], [3, 3]],
    blinker: [[1, 0], [1, 1], [1, 2]],
    beehive: [[0, 1], [0, 2], [1, 0], [1, 3], [2, 1], [2, 2]],
    block: [[0, 0], [0, 1], [1, 0], [1, 1]],
    toad: [[0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2]],
    boat: [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1]],
    loaf: [[0, 1], [0, 2], [1, 0], [1, 3], [2, 1], [2, 3], [3, 2]],
    pond: [[0, 1], [0, 2], [1, 0], [1, 3], [2, 0], [2, 3], [3, 1], [3, 2]]
  };
  function mLife(B) {
    var C = 30, R = 17, s = 7.4, x0 = 160 - C * s / 2, y0 = 100 - R * s / 2 - 4, occ = {}, live = '', ghost1 = '', ghost2 = '', i;
    function orient(cells, o) {
      var out = cells.map(function (c) { var r = c[0], q = c[1]; if (o & 1) q = -q; if (o & 2) r = -r; if (o & 4) { var tt = r; r = q; q = tt; } return [r, q]; });
      var mr = Math.min.apply(null, out.map(function (c) { return c[0]; })), mq = Math.min.apply(null, out.map(function (c) { return c[1]; }));
      return out.map(function (c) { return [c[0] - mr, c[1] - mq]; });
    }
    function fits(cells, r0, q0) {
      return cells.every(function (c) {
        for (var a = -1; a <= 1; a++) for (var b = -1; b <= 1; b++) { var r = r0 + c[0] + a, q = q0 + c[1] + b; if (r < 0 || q < 0 || r >= R || q >= C || occ[r + ',' + q]) return false; }
        return true;
      });
    }
    function place(cells, avoidBand) {
      for (var tries = 0; tries < 40; tries++) {
        var r0 = B.i(0, R - 5), q0 = B.i(0, C - 5);
        if (avoidBand && r0 > R - 8 && q0 < 14) continue;
        if (fits(cells, r0, q0)) { cells.forEach(function (c) { occ[(r0 + c[0]) + ',' + (q0 + c[1])] = 1; }); return [r0, q0]; }
      }
      return null;
    }
    /* the glider and its trail: it moves one cell diagonally every four generations */
    var go = B.i(0, 3), dr = go & 2 ? -1 : 1, dq = go & 1 ? -1 : 1, gl = orient(LIFE.glider, (dq < 0 ? 1 : 0) | (dr < 0 ? 2 : 0));
    var block = [];
    for (i = 0; i < 25; i++) block.push([Math.floor(i / 5), i % 5]);
    var gp = place(block, true) || [6, 12];
    var gr = gp[0] + (dr > 0 ? 2 : 0), gq = gp[1] + (dq > 0 ? 2 : 0);
    gl.forEach(function (c) {
      live += sq(x0 + (gq + c[1]) * s + 1, y0 + (gr + c[0]) * s + 1, s - 2);
      ghost1 += sq(x0 + (gq + c[1] - dq) * s + 1, y0 + (gr + c[0] - dr) * s + 1, s - 2);
      ghost2 += sq(x0 + (gq + c[1] - 2 * dq) * s + 1, y0 + (gr + c[0] - 2 * dr) * s + 1, s - 2);
    });
    var names = ['lwss', 'blinker', 'beehive', 'block', 'toad', 'boat', 'loaf', 'pond'], n = B.i(2, 4);
    for (i = 0; i < n; i++) {
      var pat = orient(LIFE[B.pick(names)], B.i(0, 7)), at = place(pat, false);
      if (at) pat.forEach(function (c) { live += sq(x0 + (at[1] + c[1]) * s + 1, y0 + (at[0] + c[0]) * s + 1, s - 2); });
    }
    var grid = '';
    for (i = 0; i <= R; i++) grid += M(x0, y0 + i * s) + 'h' + f(C * s);
    for (i = 0; i <= C; i++) grid += M(x0 + i * s, y0) + 'v' + f(R * s);
    B.p(grid, 't-dm', sw(0.5, 0.3));
    B.p(ghost2, 't-lf', { opacity: 0.2 });
    B.p(ghost1, 't-lf', { opacity: 0.45 });
    B.p(live, 't-lf', { opacity: 0.9 });
    B.rect(x0 + (gq - 1) * s, y0 + (gr - 1) * s, 5 * s, 5 * s, 't-gn', sw(1.4));
  }

  /* ---------------- subtraction game: positions on a line, P-positions filled, the moves from one N-position drawn as
     arcs back to the P-positions they reach; the bracket marks one period */
  function mGame(B) {
    var S = [], i, n;
    while (S.length < B.i(2, 3)) { var v = B.i(1, 7); if (S.indexOf(v) < 0) S.push(v); }
    S.sort(function (a, b) { return a - b; });
    var N = B.i(22, 28), sp = 256 / N, x0 = 160 - (N - 1) * sp / 2, y = 118, Pp = [], hol = '', fil = '';
    for (n = 0; n < 200; n++) { var win = false; for (i = 0; i < S.length; i++) if (n - S[i] >= 0 && Pp[n - S[i]]) win = true; Pp.push(!win); }
    var per = 1;
    for (var p = 1; p < 60; p++) { var ok = true; for (n = 60; n < 140 && ok; n++) ok = Pp[n] === Pp[n + p]; if (ok) { per = p; break; } }
    var tk = '';
    for (n = 0; n < N; n++) {
      var x = x0 + n * sp;
      if (Pp[n]) fil += ring(x, y, 3.4); else hol += ring(x, y, 3.4);
      if (n % 5 === 0) tk += M(x, y + 8) + 'v' + (n % 10 ? 3 : 6);
    }
    B.p(M(x0 - 8, y) + 'H' + f(x0 + (N - 1) * sp + 8), 't-dm', sw(1, 0.6));
    B.p(tk, 't-dm', sw(1, 0.8));
    var from = -1;
    for (n = N - 1; n > S[S.length - 1] + 2; n--) if (!Pp[n] && S.some(function (s) { return Pp[n - s]; })) { from = n; break; }
    if (from < 0) from = N - 1;
    var arcs = '', hot = '';
    S.forEach(function (s) {
      var a = x0 + from * sp, b = x0 + (from - s) * sp, h = 14 + s * sp * 0.55, path = M(a, y - 6) + 'C' + f(a) + ' ' + f(y - 6 - h) + ' ' + f(b) + ' ' + f(y - 6 - h) + ' ' + f(b) + ' ' + f(y - 6);
      var head = M(b - 3, y - 11) + L(b, y - 6) + L(b + 3, y - 11);
      if (Pp[from - s]) hot += path + head; else arcs += path + head;
    });
    B.p(hol, 't-ho', sw(1.3));
    B.p(fil, 't-lf', { opacity: 0.9 });
    B.p(arcs, 't-ln', sw(1.1, 0.6));
    B.p(hot, 't-gn', sw(1.4));
    var ps = per * Math.floor(B.i(0, Math.max(0, N - per - 1)) / per), xs = x0 + ps * sp - sp / 2;
    if (per < N) B.p(M(xs, y + 22) + 'v6H' + f(xs + per * sp) + 'v-6', 't-dm', sw(1.4, 0.9));
  }

  /* ---------------- biology: an RNA arc diagram (stems, a pseudoknot) or a protein ribbon */
  function mArcs(B) {
    var N = B.i(26, 34), x0 = 34, x1 = 286, sp = (x1 - x0) / (N - 1), yb = 150, used = {}, arcs = '', i;
    function X(i) { return x0 + i * sp; }
    function arc(a, b) { var r = (X(b) - X(a)) / 2; return M(X(a), yb - 3) + 'a' + f(r) + ' ' + f(Math.min(r, 120)) + ' 0 0 1 ' + f(2 * r) + ' 0'; }
    var stems = [], tries = 0;
    while (stems.length < B.i(2, 3) && tries++ < 40) {
      var len = B.i(3, 5), a = B.i(0, N - 2 * len - 4), b = B.i(a + 2 * len + 3, Math.min(N - 1, a + 2 * len + 14)), clash = false;
      for (i = 0; i < len; i++) if (used[a + i] || used[b - i]) clash = true;
      if (clash || b >= N) continue;
      for (i = 0; i < len; i++) { used[a + i] = used[b - i] = 1; arcs += arc(a + i, b - i); }
      stems.push([a, b, len]);
    }
    /* a pseudoknot: a short stem that crosses the first one */
    var pk = '', s0 = stems[0];
    if (s0) {
      var pa = Math.floor((s0[0] + s0[2] + s0[1] - s0[2]) / 2), pb = Math.min(N - 1, s0[1] + B.i(2, 5));
      for (i = 0; i < 2; i++) if (!used[pa + i] && !used[pb - i] && pb - i > pa + i + 1) { used[pa + i] = used[pb - i] = 1; pk += arc(pa + i, pb - i); }
    }
    var beads = '', paired = '';
    for (i = 0; i < N; i++) (used[i] ? (paired += ring(X(i), yb, 2.2)) : (beads += ring(X(i), yb, 2.2)));
    B.p(M(X(0), yb) + 'H' + f(X(N - 1)), 't-dm', sw(1.2, 0.8));
    B.p(arcs, 't-ln', sw(1.2, 0.8));
    B.p(pk, 't-ln', sw(1.2, 0.8, { 'stroke-dasharray': '3 2' }));
    B.p(beads, 't-ho', sw(1.2));
    B.p(paired, 't-lf', { opacity: 0.9 });
    var free = [];
    for (i = 0; i < N; i++) if (!used[i]) free.push(i);
    var ga = free.length > 1 ? free[B.i(0, Math.floor(free.length / 2))] : 0, gb = free.length > 1 ? free[free.length - 1 - B.i(0, Math.floor(free.length / 3))] : N - 1;
    if (gb - ga < 4) { ga = 0; gb = N - 1; }
    B.p(arc(ga, gb), 't-gn', sw(1.5, null, { 'stroke-dasharray': '4 3' }));
    B.c(X(ga), yb, 3, 't-gf'); B.c(X(gb), yb, 3, 't-gf');
  }
  function mRibbon(B) {
    var pts = B.scatter(B.i(10, 13), 44, 276, 36, 160, 34), ord = [pts[0]], left = pts.slice(1), i;
    while (left.length) {
      var last = ord[ord.length - 1], bi = 0;
      left.forEach(function (p, j) { if (dist(p, last) < dist(left[bi], last)) bi = j; });
      ord.push(left.splice(bi, 1)[0]);
    }
    /* sample the backbone, then dress three stretches: a helix (a tight coil) and two beta strands (zig-zag arrows) */
    var sm = [];
    for (i = 0; i < ord.length - 1; i++) {
      var p0 = ord[Math.max(0, i - 1)], p1 = ord[i], p2 = ord[i + 1], p3 = ord[Math.min(ord.length - 1, i + 2)];
      for (var u = 0; u < 1; u += 0.1) {
        var u2 = u * u, u3 = u2 * u;
        sm.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3),
                 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)]);
      }
    }
    sm.push(ord[ord.length - 1]);
    var NL = sm.length, hA = B.i(5, Math.floor(NL / 3)), hB = hA + B.i(14, 20), s1 = Math.min(NL - 30, hB + B.i(6, 14)), s2 = Math.min(NL - 12, s1 + B.i(14, 20));
    var coil = '', helix = '', strand = '', run = [];
    function flush() { if (run.length > 1) coil += poly(run); run = []; }
    for (i = 0; i < NL; i++) {
      var inH = i >= hA && i < hB, inS = (i >= s1 && i < s1 + 9) || (i >= s2 && i < s2 + 9);
      if (inH || inS) { if (run.length) { run.push(sm[i]); flush(); } continue; }
      if (!run.length && i) run.push(sm[i - 1]);
      run.push(sm[i]);
    }
    flush();
    function norm(i) { var a = sm[Math.max(0, i - 1)], b = sm[Math.min(NL - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.sqrt(dx * dx + dy * dy) || 1; return [-dy / l, dx / l]; }
    var hp = [];
    /* the helix as a spring: loops around the backbone (a normal swing plus a forward-and-back swing) */
    for (i = hA; i <= hB && i < NL; i++) {
      for (var q = 0; q < 1; q += 0.25) {
        var j0 = Math.min(NL - 1, i), j1 = Math.min(NL - 1, i + 1), nm = norm(j0), bx = sm[j0][0] + (sm[j1][0] - sm[j0][0]) * q, by = sm[j0][1] + (sm[j1][1] - sm[j0][1]) * q;
        var ph = (i - hA + q) * 1.9, tx = -nm[1], ty = nm[0], w = 8 * Math.sin(ph), v = 5 * Math.cos(ph);
        hp.push([bx + nm[0] * w + tx * v, by + nm[1] * w + ty * v]);
      }
    }
    helix = smooth(hp);
    [s1, s2].forEach(function (s) {
      /* a beta strand: a flat ribbon (two edges) ending in an arrowhead */
      var up = [], dn = [], e2 = Math.min(NL - 1, s + 9), b7 = Math.min(NL - 1, s + 6);
      for (var k = s; k <= b7; k++) { var n2 = norm(k); up.push([sm[k][0] + n2[0] * 3.5, sm[k][1] + n2[1] * 3.5]); dn.push([sm[k][0] - n2[0] * 3.5, sm[k][1] - n2[1] * 3.5]); }
      var nb = norm(b7), e = sm[e2], b = sm[b7];
      strand += poly(up.concat([[b[0] + nb[0] * 7, b[1] + nb[1] * 7], e, [b[0] - nb[0] * 7, b[1] - nb[1] * 7]]).concat(dn.reverse()), true);
    });
    B.p(coil, 't-ln', sw(1.6, 0.75));
    B.p(helix, 't-ln', sw(2.6, 0.9));
    B.p(strand, 't-ho', sw(1.4));
    var a = sm[Math.floor(NL * 0.15)], c = sm[Math.floor(NL * 0.8)];
    B.p(seg(a[0], a[1], c[0], c[1]), 't-gn', sw(1.3, null, { 'stroke-dasharray': '3 3' }));
    B.c(a[0], a[1], 3.2, 't-gf'); B.c(c[0], c[1], 3.2, 't-gf');
  }

  /* ---------------- neuroscience: a raster around a stimulus, the highlighted unit boxed (shape, not only colour) */
  function mRaster(B) {
    var rows = B.i(7, 8), stim = B.u(110, 190), d = '', hd = '', hot = B.i(1, rows - 2), all = [], rh = 13, y0 = 30;
    for (var r = 0; r < rows; r++) {
      var y = y0 + r * rh, rate = B.u(0.035, 0.08), x = 36 + B.u(0, 16), resp = B.u(0.6, 1);
      while (x < 288) {
        var s = M(x, y - 4) + 'v8';
        if (r === hot) hd += s; else d += s;
        all.push(x);
        var boost = x > stim && x < stim + 34 ? 1 + 5 * resp : 1;
        x += 2 + -Math.log(1 - B.r()) / (rate * boost);
      }
    }
    B.p(M(stim, y0 - 10) + 'V' + f(y0 + rows * rh + 46), 't-dm', sw(1.1, 0.9, { 'stroke-dasharray': '3 3' }));
    B.p(M(stim - 4, y0 - 12) + 'h8l-4 5z', 't-df');
    B.p(d, 't-ln', sw(1.3, 0.6));
    B.p(hd, 't-ln', sw(1.6));
    B.rect(32, y0 + hot * rh - 7, 258, 14, 't-gn', sw(1.1));
    var hist = [], yb = y0 + rows * rh + 44;
    for (var x2 = 36; x2 <= 288; x2 += 6) {
      var n = all.filter(function (a) { return Math.abs(a - x2) < 7; }).length;
      hist.push([x2, yb - n * 2.2]);
    }
    B.p(M(34, yb) + 'H290', 't-dm', sw(0.8, 0.6));
    B.p(smooth(hist), 't-dm', sw(1.3, 0.9));
  }

  /* ---------------- engineering: a wind farm, three-blade rotors inside a site boundary with their wakes */
  function mWind(B) {
    var th = B.u(-0.6, 0.6) + (B.ch(0.5) ? 0 : Math.PI), c = Math.cos(th), s = Math.sin(th), site = [], i;
    for (i = 0; i < 7; i++) { var a = i * TAU / 7 + B.u(-0.2, 0.2), rr = B.u(0.75, 1); site.push([170 + 118 * rr * Math.cos(a), 104 + 70 * rr * Math.sin(a)]); }
    B.p(poly(site, true), 't-dm', sw(1.1, 0.85, { 'stroke-dasharray': '5 3' }));
    var pts = B.scatter(B.i(7, 10), 84, 260, 54, 156, 30), wk = '', rot = '', hubs = '', hot = B.i(0, pts.length - 1);
    pts.forEach(function (p, j) {
      wk += M(p[0], p[1]) + L(p[0] + 50 * c - 10 * s, p[1] + 50 * s + 10 * c) + L(p[0] + 50 * c + 10 * s, p[1] + 50 * s - 10 * c) + 'Z';
      var ph = B.u(0, TAU), bl = '';
      for (var k = 0; k < 3; k++) bl += M(p[0], p[1]) + L(p[0] + 8 * Math.cos(ph + k * TAU / 3), p[1] + 8 * Math.sin(ph + k * TAU / 3));
      rot += bl; hubs += dot(p[0], p[1]);
    });
    B.p(wk, 't-df', { opacity: 0.13 });
    B.p(rot, 't-ln', sw(1.6, 0.95));
    B.p(hubs, 't-ln', sw(4));
    var ax = 46, ay = 44;
    B.c(ax, ay, 13, 't-dm', sw(0.9, 0.7));
    B.p(arrow(ax - 11 * c, ay - 11 * s, ax + 11 * c, ay + 11 * s, 4), 't-ln', sw(1.4));
    var h = pts[hot];
    if (h) B.c(h[0], h[1], 12, 't-gn', sw(1.4));
  }

  /* ---------------- crypto math: points of y^2 = x^3 + ax + b over a small prime field, each in its cell */
  function mFinite(B) {
    var p = B.pick([11, 13]), a = B.i(1, p - 1), b = B.i(1, p - 1), s = 140 / p, x0 = 160 - 70 + B.u(-40, 40), y0 = 168, grid = '', tk = '', pts = [], d = '', x, y;
    for (var g = 0; g <= p; g++) grid += M(x0 + g * s, y0) + 'v-140' + M(x0, y0 - g * s) + 'h140';
    for (g = 0; g < p; g++) tk += M(x0 + (g + 0.5) * s, y0 + 3) + 'v3' + M(x0 - 3, y0 - (g + 0.5) * s) + 'h-3';
    for (x = 0; x < p; x++) for (y = 0; y < p; y++) if (((y * y - (x * x * x + a * x + b)) % p + p) % p === 0) pts.push([x, y]);
    B.p(grid, 't-dm', sw(0.6, 0.55));
    B.p(tk, 't-dm', sw(1, 0.8));
    B.p(M(x0, y0 - p * s / 2) + 'h140', 't-dm', sw(0.9, 0.8, { 'stroke-dasharray': '3 3' }));
    var hot = pts.length ? B.i(0, pts.length - 1) : -1;
    pts.forEach(function (q, i) { if (i !== hot) d += sq(x0 + q[0] * s + 1.5, y0 - (q[1] + 1) * s + 1.5, s - 3); });
    B.p(d, 't-lf', { opacity: 0.85 });
    if (hot >= 0) {
      var q = pts[hot], m = [q[0], (p - q[1]) % p];
      B.rect(x0 + q[0] * s + 0.5, y0 - (q[1] + 1) * s + 0.5, s - 1, s - 1, 't-gh', sw(1.5));
      if (m[1] !== q[1]) B.p(M(x0 + (q[0] + 0.5) * s, y0 - (q[1] + 0.5) * s) + 'V' + f(y0 - (m[1] + 0.5) * s), 't-gn', sw(1, 0.8, { 'stroke-dasharray': '2 2' }));
    }
  }

  /* ---------------- physics: two sources, sparse rings and the antinodal hyperbolae where they reinforce */
  function mWaves(B) {
    var a = [B.u(90, 130), B.u(70, 130)], b = [B.u(190, 230), B.u(70, 130)], lam = B.u(12, 14), d1 = '', d2 = '';
    for (var r = lam; r < lam * 12; r += lam) { d1 += ring(a[0], a[1], r); d2 += ring(b[0], b[1], r); }
    B.p(d1, 't-ln', sw(0.8, 0.3));
    B.p(d2, 't-dm', sw(0.8, 0.4));
    var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, cc = dist(a, b) / 2, an = Math.atan2(b[1] - a[1], b[0] - a[0]), ca = Math.cos(an), sa = Math.sin(an), hyp = '';
    for (var m = -3; m <= 3; m++) {
      var A = m * lam / 2;
      if (!m || Math.abs(A) >= cc - 2) continue;
      var Bh = Math.sqrt(cc * cc - A * A), pts = [];
      for (var t = -2.6; t <= 2.61; t += 0.2) {
        var u = A * Math.cosh(t), v = Bh * Math.sinh(t);
        pts.push([mx + u * ca - v * sa, my + u * sa + v * ca]);
      }
      hyp += smooth(pts);
    }
    B.p(hyp, 't-ln', sw(1.3, 0.85));
    B.p(seg(mx - 200 * -sa, my - 200 * ca, mx + 200 * -sa, my + 200 * ca), 't-gn', sw(1.2, 0.9, { 'stroke-dasharray': '3 4' }));
    B.c(a[0], a[1], 3.5, 't-lf');
    B.c(b[0], b[1], 3.5, 't-lf');
    B.full = true;
  }
  function mHoney(B) {
    var r = B.u(12, 14), d = '', h = Math.sqrt(3) * r, cells = [], cols = 9, rows = 6, w = cols * h, x0 = 160 - w / 2 + h / 2, y0 = 100 - (rows - 1) * 0.75 * r, atoms = '';
    for (var j = 0; j < rows; j++) for (var i = 0; i < cols - (j % 2); i++) {
      var cx = x0 + i * h + (j % 2 ? h / 2 : 0), cy = y0 + j * 1.5 * r, p = [];
      for (var k = 0; k < 6; k++) { var a = Math.PI / 6 + k * Math.PI / 3; p.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
      d += poly(p, true);
      if (j > 0 && j < rows - 1 && i > 0 && i < cols - 2) cells.push(p);
    }
    B.p(d, 't-ln', sw(1.1, 0.6));
    var hc = B.pick(cells);
    hc.forEach(function (q) { atoms += dot(q[0], q[1]); });
    B.p(poly(hc, true), 't-gh', sw(1.8));
    B.p(atoms, 't-gn', sw(4.4));
  }

  /* ---------------- formal proofs: a Gentzen tree, premises over inference bars, the open goal a hollow green box */
  function mProof(B) {
    function build(dep) {
      var k = dep >= 3 || (dep > 1 && B.ch(0.4)) ? 0 : (dep === 0 ? 2 : B.i(1, 2)), kids = [];
      for (var i = 0; i < k; i++) kids.push(build(dep + 1));
      return { kids: kids, w: B.u(22, 40) * (1 + 0.25 * (3 - dep) / 3), dep: dep };
    }
    var root = build(0), leaves = [], all = [];
    (function walk(n) { all.push(n); if (!n.kids.length) leaves.push(n); n.kids.forEach(walk); })(root);
    var span = 0;
    leaves.forEach(function (l) { span += l.w + 30; });
    var sc = Math.min(1.2, 250 / span), x = 160 - span * sc / 2;
    leaves.forEach(function (l) { l.w *= sc; l.x = x + (l.w + 30 * sc) / 2; x += l.w + 30 * sc; });
    (function place(n) { if (!n.kids.length) return; n.kids.forEach(place); n.x = (n.kids[0].x + n.kids[n.kids.length - 1].x) / 2; })(root);
    var hot = B.pick(leaves), forms = '', rules = '', names = '';
    all.forEach(function (n) {
      n.y = 152 - n.dep * 34;
      if (n !== hot) forms += M(n.x - n.w / 2 + 3, n.y) + 'h' + f(n.w - 6);
      if (n.kids.length) {
        var a = n.kids[0], b = n.kids[n.kids.length - 1], yy = n.y - 13, l = Math.min(a.x - a.w / 2, n.x - n.w / 2) - 2, r = Math.max(b.x + b.w / 2, n.x + n.w / 2) + 2;
        rules += M(l, yy) + 'H' + f(r);
        names += dot(r + 6, yy);
      }
    });
    var tx = root.x - root.w / 2 - 14;
    B.p(rules, 't-dm', sw(1.4, 0.95));
    B.p(names, 't-dm', sw(2.4, 0.8));
    B.p(forms, 't-ln', sw(6, 0.55));
    B.p(M(tx, root.y - 6) + 'v12' + M(tx, root.y) + 'h8', 't-ln', sw(1.6));
    B.rect(hot.x - hot.w / 2, hot.y - 7, hot.w, 14, 't-gh', sw(1.3, null, { 'stroke-dasharray': '3 2' }));
  }
  /* number sieve: a ten-column table; primes filled, composites crossed out, one prime's multiples struck through */
  function mSieve(B) {
    var cols = 10, rows = 6, s = 17, x0 = 160 - cols * s / 2, y0 = 100 - rows * s / 2, s0 = 10 * B.i(0, 99999) + 1, pd = '', cd = '', grid = '', last = null, i;
    for (i = 0; i <= rows; i++) grid += M(x0, y0 + i * s) + 'h' + cols * s;
    for (i = 0; i <= cols; i++) grid += M(x0 + i * s, y0) + 'v' + rows * s;
    for (i = 0; i < cols * rows; i++) {
      var x = x0 + (i % cols) * s, y = y0 + Math.floor(i / cols) * s;
      if (isPrime(s0 + i)) { pd += sq(x + 3, y + 3, s - 6); last = [x, y]; }
      else cd += seg(x + 5, y + 5, x + s - 5, y + s - 5) + seg(x + s - 5, y + 5, x + 5, y + s - 5);
    }
    B.p(grid, 't-dm', sw(0.7, 0.6));
    B.p(cd, 't-dm', sw(1, 0.75));
    B.p(pd, 't-lf', { opacity: 0.85 });
    var first = (11 - (s0 % 11)) % 11, strike = '';
    for (var k = first; k < cols * rows; k += 11) {
      var sx = x0 + (k % cols) * s + s / 2, sy = y0 + Math.floor(k / cols) * s + s / 2;
      if (k + 11 < cols * rows && (k % cols) < cols - 1) strike += seg(sx, sy, sx + s, sy + s);
    }
    B.p(strike, 't-ln', sw(1.2, 0.8, { 'stroke-dasharray': '3 2' }));
    if (last) B.rect(last[0] + 0.5, last[1] + 0.5, s - 1, s - 1, 't-gn', sw(1.6));
  }

  /* ================================================================== dispatch */
  function pick(B, list) { return list[Math.floor(B.r() * list.length)]; }
  var FAM = Object.create(null);
  [['math', 'number-hunts erdos-and-proofs record-tables graphs-games-automata recreational-math formal-proofs crypto-math'],
   ['comp', 'algorithms compression-and-golf machine-learning ml-robustness optimization-benchmarks wildcard'],
   ['phys', 'physics packings-physics particle-physics chemistry-materials engineering earth-and-sky planetary-science sky-archives'],
   ['life', 'biology genomics disease-research drug-discovery neuroscience ecology animal-communication new-species'],
   ['text', 'unbroken-ciphers undeciphered-scripts ancient-texts herculaneum-scrolls uncharted lost-and-hidden']
  ].forEach(function (g) { g[1].split(' ').forEach(function (c) { FAM[c] = g[0]; }); });

  var FULL = [mContour, mHelix, mField, mWaves, mMap];
  var MOTIF = Object.assign(Object.create(null), {
    'graphs-games-automata': function (B, t) {
      if (/\blife\b|glider|catagolue|spaceship|oscillator/.test(t)) return mLife;
      if (/automat|sandpile|\brule\b/.test(t)) return mCA;
      if (/\bgame|\bnim\b|takeaway|p-position/.test(t)) return mGame;
      return mGraph;
    },
    'record-tables': function () { return mTable; },
    'number-hunts': function (B) { return pick(B, [mSpiral, mSpiral, mSieve]); },
    'erdos-and-proofs': function (B, t) { return /bound|constant|radius|inequalit/.test(t) && B.ch(0.7) ? mBounds : pick(B, [mPoints, mMoser, mProof, mBounds]); },
    'physics': function (B, t) { return /percolat/.test(t) ? mPerc : pick(B, [mField, mWaves, mPerc]); },
    'optimization-benchmarks': function (B, t) {
      if (/job.?shop|schedul|makespan|flow.?shop|timetabl/.test(t)) return mGantt;
      if (/\btsp\b|travel|routing|vehicle|tour/.test(t)) return mTour;
      return pick(B, [mConverge, mConverge, mTour]);
    },
    'disease-research': function (B, t) {
      if (/surviv|prognos|mortal|hazard/.test(t)) return mKM;
      if (/\bcell|patholog|segment|tissue|tcr|mhc|microscop/.test(t)) return mCells;
      return pick(B, [mKM, mCells]);
    },
    'recreational-math': function (B, t) { return /sudoku|latin|magic|kakuro|clue/.test(t) ? mSudoku : (/polyomino|tiling|tile|pentomino/.test(t) ? mPolyomino : pick(B, [mPolyomino, mSudoku, mPolyomino])); },
    'biology': function (B, t) {
      if (/\brna\b|ribo|secondary|eterna/.test(t)) return mArcs;
      if (/protein|fold|struct|antibod|scaffold|fitness|enzyme/.test(t)) return mRibbon;
      if (/\bdna\b|genom|nucleotide|minimizer|sequence/.test(t)) return B.ch(0.6) ? mHelix : mArcs;
      return pick(B, [mHelix, mArcs, mRibbon]);
    },
    'wildcard': function () { return mStars; },
    'packings-physics': function (B, t) {
      if (/spher|grassmann|kissing|thomson|energy/.test(t)) return mSphere;
      if (/equal|congruent|packomania/.test(t)) return mEqual;
      return pick(B, [mPack, mPack, mEqual]);
    },
    'earth-and-sky': function () { return mContour; },
    'sky-archives': function () { return mSky; },
    'algorithms': function (B, t) {
      if (/sort|network|comparator|median/.test(t)) return mSortNet;
      if (/matri|tensor|multiplic/.test(t)) return mMatrix;
      return pick(B, [mSortNet, mTree, mMatrix]);
    },
    'machine-learning': function (B, t) { return /forecast|time series|temporal/.test(t) ? mForecast : pick(B, [mNet, mLoss]); },
    'unbroken-ciphers': function (B, t) { return /enigma|rotor|m-209|hagelin|lorenz|typex|sigaba|wheel|chaocipher|machine/.test(t) ? mRotor : mCipher; },
    'undeciphered-scripts': function (B, t) { return /khipu|quipu/.test(t) ? mKhipu : (/cuneiform|wedge|proto-elamite/.test(t) ? mWedges : mTablet); },
    'ancient-texts': function (B, t) { return /rejoin|\bjoin|matching|fragment.*(pair|join)/.test(t) ? mJoin : (/cuneiform/.test(t) ? mWedges : mFragment); },
    'herculaneum-scrolls': function (B, t) { return /ink|layer|surface|segment/.test(t) && B.ch(0.6) ? mLayers : pick(B, [mScroll, mLayers]); },
    'formal-proofs': function () { return mProof; },
    'drug-discovery': function () { return mMolecule; },
    'uncharted': function (B, t) { return /mars|lunar|moon|impact|crater|\bpit/.test(t) ? mCraters : mMap; },
    'lost-and-hidden': function (B, t) { return /maya|lidar|structure|archaeolog|chactun|settlement|geoglyph/.test(t) ? mSurvey : mSonar; },
    'ml-robustness': function () { return mBoundary; },
    'planetary-science': function (B, t) { return /\bpit|crater|impact/.test(t) ? mCraters : mPlanet; },
    'genomics': function () { return mGenome; },
    'ecology': function (B, t) { return /sound|acoust|audio|bird|beans|call|song/.test(t) ? mSpectro : mWeb; },
    'chemistry-materials': function (B, t) { return /qm9|molec|adsorpt|catalys/.test(t) ? mMolecule : pick(B, [mCrystal, mHoney]); },
    'engineering': function (B, t) {
      if (/wind|turbine/.test(t)) return mWind;
      if (/chip|placement|routing|ispd|circuit|vlsi|eda|fpga|gate/.test(t)) return mChip;
      return pick(B, [mTruss, mChip]);
    },
    'neuroscience': function (B, t) { return /segment|neuron instance|morpholog|connectom|flylight|reconstruct/.test(t) ? mNeuron : mRaster; },
    'compression-and-golf': function () { return mBars; },
    'particle-physics': function () { return mCollision; },
    'animal-communication': function () { return mSpectro; },
    'new-species': function (B) { return pick(B, [mClade, mClade, mPhyllo]); },
    'crypto-math': function (B, t) { return /apn|finite|gf\(|boolean|field/.test(t) ? mFinite : mCurve; }
  });

  /* ---------------- signature token: strict patterns only, at most 14 characters from a small alphabet */
  var SIG_OK = /^[A-Za-z0-9(),=\[\]<>. -]{1,14}$/;
  var SIGS = [
    [/\bA\d{6}\b/, null],
    [/\[\[\d{1,4},\s?\d{1,4}(?:,\s?\d{1,4})?\]\]/, 1],
    [/\b[A-Z][A-Za-z]{0,3}\(\d{1,4}(?:,\s?\d{1,4}){1,3}\)/, 1],
    [/\(\d{1,4}(?:,\s?\d{1,4}){1,3}\)/, 1],
    [/\bn\s?=\s?\d{1,6}\b/, 2],
    /* a year only where it names a contest or an edition (ISIC 2018, IHTC-2024, SV-COMP 2026), not a cited paper's */
    [/\b(?:[A-Z]{1,6}-)?[A-Z][A-Za-z]{0,8}[A-Z][A-Za-z]{0,8}[- ](?:19|20)\d{2}\b/, null]
  ];
  function sig(title) {
    var t = String(title == null ? '' : title).slice(0, 400);
    for (var i = 0; i < SIGS.length; i++) {
      var m = SIGS[i][0].exec(t);
      if (!m) continue;
      var s = m[0];
      if (SIGS[i][1] === 1) s = s.replace(/\s+/g, '');
      if (SIGS[i][1] === 2) s = 'n = ' + s.replace(/\D+/g, '');
      if (SIG_OK.test(s)) return s;
    }
    return null;
  }

  function make(k) {
    k = k || {};
    var id = typeof k.id === 'string' && SLUG.test(k.id) ? k.id : '';
    var cat = typeof k.cat === 'string' && SLUG.test(k.cat) ? k.cat : '';
    var title = typeof k.t === 'string' ? k.t.slice(0, 400) : '';
    var t = title.toLowerCase();
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 320 200');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    svg.setAttribute('class', 'thumb f-' + (FAM[cat] || 'misc'));
    var B = new Pen(svg, mulberry(hash(id + '|' + cat)));
    /* faint blueprint grid */
    var g = '';
    for (var x = 20; x < 320; x += 20) g += 'M' + x + ' 0V200';
    for (var y = 20; y < 200; y += 20) g += 'M0 ' + y + 'H320';
    B.p(g, 't-gr', sw(0.6));
    var V = new Pen(svg, mulberry(hash(id, 0x5bd1e995)));   /* a second stream picks the variant */
    var chooser = MOTIF[cat], fn = chooser ? chooser(V, t) : mStars;
    try { fn(B, t); } catch (e) { /* a motif must never break the page: keep the frame */ }
    /* corner marks, left out where the motif runs to the edge so they never cut through it. Each is its own path, so
       the corner under the token (bottom left, or top left once fit() moves it there) can be left out */
    var tok = sig(title), cn = null;
    if (!B.full && FULL.indexOf(fn) < 0) {
      cn = ['M8 18V8H18', 'M302 8H312V18', 'M312 182V192H302', 'M18 192H8V182'].map(function (d) { return B.p(d, 't-dm', sw(1, 0.7)); });
      if (tok) svg.removeChild(cn[3]);
    }
    if (tok) {
      var tg = B.el('g', { 'class': 'tk' }), tw = tok.length * 9 + 14;
      B.rect(18, 172, tw, 21, 't-bg', null, tg);
      B.el('path', { d: 'M18 176v13', 'class': 't-gn', 'stroke-width': 1.6 }, tg);
      var te = B.el('text', { x: 25, y: 187.5, 'class': 't-tx' }, tg);
      te.textContent = tok;
      tg._w = tw; tg._cn = cn;
    }
    return svg;
  }

  /* once the picture is in the page: if a green mark sits under the token, move the token to a free corner */
  function fit(svg) {
    var tg = svg && svg.querySelector && svg.querySelector('g.tk');
    if (!tg || !tg._w) return;
    var w = tg._w, spots = [[0, 0], [0, -163], [302 - 18 - w - 18, 0], [302 - 18 - w - 18, -163]], marks = [];
    try {
      Array.prototype.forEach.call(svg.querySelectorAll('.t-gn,.t-gf,.t-gh'), function (e) {
        if (tg.contains(e)) return;
        var b = e.getBBox();
        if (b.width || b.height) marks.push(b);
      });
    } catch (e) { return; }
    for (var i = 0; i < spots.length; i++) {
      var x0 = 18 + spots[i][0] - 3, y0 = 172 + spots[i][1] - 3, x1 = x0 + w + 6, y1 = y0 + 27;
      if (!marks.some(function (b) { return b.x < x1 && b.x + b.width > x0 && b.y < y1 && b.y + b.height > y0; })) {
        if (i) {
          tg.setAttribute('transform', 'translate(' + spots[i][0] + ' ' + spots[i][1] + ')');
          /* the bottom-left corner mark comes back; at the top left, that corner's mark goes */
          var cn = tg._cn;
          if (cn) { svg.insertBefore(cn[3], tg); if (i === 1 && cn[0].parentNode) cn[0].parentNode.removeChild(cn[0]); }
        }
        return;
      }
    }
  }

  window.V3Thumb = Object.freeze({ make: make, sig: sig, fit: fit });
  /* app.js may have laid out cards before this file ran: tell it to draw them */
  try { document.dispatchEvent(new Event('v3thumb')); } catch (e) {}
})();
