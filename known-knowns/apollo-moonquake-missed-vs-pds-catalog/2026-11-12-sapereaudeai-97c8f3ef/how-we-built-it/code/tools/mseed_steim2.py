"""Minimal pure-Python/numpy MiniSEED reader (SEED 2.4), written for this run.

Supports: fixed 48-byte data header, blockettes 1000 (encoding, word order, record length)
and 1001 (microseconds), encodings 11 (Steim2), 10 (Steim1), 3 (INT32), 4 (FLOAT32),
5 (FLOAT64), big-endian word order. Written from the SEED 2.4 manual's published layout
(fixed section of data header, Appendix B Steim compression).

read_mseed(path) -> list of records: dict(net, sta, loc, cha, start (numpy datetime64[ns]
                    as int ns since epoch), rate (Hz), data (int64 or float64 array))
"""
import struct
import datetime as _dt
import numpy as np

_EPOCH = _dt.datetime(1970, 1, 1)


def _btime_ns(b):
    yr, doy, hh, mm, ss, _unused, frac = struct.unpack('>HHBBBBH', b)
    t = _dt.datetime(yr, 1, 1) + _dt.timedelta(days=doy - 1, hours=hh, minutes=mm, seconds=ss)
    d = t - _EPOCH
    return (d.days * 86400 + d.seconds) * 1_000_000_000 + frac * 100_000  # frac in 0.0001 s


def _rate(factor, mult):
    if factor > 0:
        r = float(factor)
    elif factor < 0:
        r = -1.0 / factor
    else:
        return 0.0
    if mult > 0:
        r *= mult
    elif mult < 0:
        r /= -mult
    return r


def _sext(v, bits):
    v = v.astype(np.int64)
    sign = np.int64(1) << (bits - 1)
    return (v ^ sign) - sign


def _steim_diffs(words, steim):
    """words: uint32 array shape (nframes, 16). Returns (diffs int64 array, X0, Xn)."""
    nib = words[:, 0]
    X0 = int(np.int32(np.uint32(words[0, 1])))
    Xn = int(np.int32(np.uint32(words[0, 2])))
    nf = words.shape[0]
    k = np.arange(16, dtype=np.uint32)
    codes = (nib[:, None] >> (np.uint32(30) - 2 * k)[None, :]) & np.uint32(3)
    mask = np.ones((nf, 16), bool)
    mask[:, 0] = False
    mask[0, 1] = False
    mask[0, 2] = False
    w = words[mask]
    c = codes[mask]
    out_pieces = []  # (word_index, array of diffs)
    idx = np.arange(w.size)
    counts = np.zeros(w.size, np.int64)
    pieces = {}
    if steim == 1:
        # 01: four 8-bit, 10: two 16-bit, 11: one 32-bit
        sel = c == 1
        if sel.any():
            ws = w[sel]
            d = np.stack([_sext((ws >> np.uint32(s)) & np.uint32(0xFF), 8) for s in (24, 16, 8, 0)], 1)
            pieces[('a',)] = (idx[sel], d); counts[sel] = 4
        sel = c == 2
        if sel.any():
            ws = w[sel]
            d = np.stack([_sext((ws >> np.uint32(s)) & np.uint32(0xFFFF), 16) for s in (16, 0)], 1)
            pieces[('b',)] = (idx[sel], d); counts[sel] = 2
        sel = c == 3
        if sel.any():
            ws = w[sel]
            d = _sext(ws, 32)[:, None]
            pieces[('c',)] = (idx[sel], d); counts[sel] = 1
    else:
        dnib = (w >> np.uint32(30)) & np.uint32(3)
        specs = []
        # code 01: four 8-bit diffs
        specs.append((c == 1, 8, 4))
        # code 10: dnib 01 one 30-bit, 10 two 15-bit, 11 three 10-bit
        specs.append(((c == 2) & (dnib == 1), 30, 1))
        specs.append(((c == 2) & (dnib == 2), 15, 2))
        specs.append(((c == 2) & (dnib == 3), 10, 3))
        # code 11: dnib 00 five 6-bit, 01 six 5-bit, 10 seven 4-bit
        specs.append(((c == 3) & (dnib == 0), 6, 5))
        specs.append(((c == 3) & (dnib == 1), 5, 6))
        specs.append(((c == 3) & (dnib == 2), 4, 7))
        bad = ((c == 2) & (dnib == 0)) | ((c == 3) & (dnib == 3))
        if bad.any():
            raise ValueError('invalid Steim2 dnib')
        for j, (sel, bits, n) in enumerate(specs):
            if not sel.any():
                continue
            ws = w[sel]
            m = np.uint32((1 << bits) - 1)
            shifts = [bits * (n - 1 - i) for i in range(n)]
            d = np.stack([_sext((ws >> np.uint32(s)) & m, bits) for s in shifts], 1)
            pieces[j] = (idx[sel], d)
            counts[sel] = n
    offs = np.concatenate([[0], np.cumsum(counts)])
    total = int(offs[-1])
    diffs = np.zeros(total, np.int64)
    for key, (wi, d) in pieces.items():
        n = d.shape[1]
        pos = offs[wi][:, None] + np.arange(n)[None, :]
        diffs[pos.ravel()] = d.ravel()
    return diffs, X0, Xn


def read_mseed(path, check=True):
    raw = open(path, 'rb').read()
    recs = []
    off = 0
    while off < len(raw):
        h = raw[off:off + 48]
        if len(h) < 48:
            break
        if h[6:7] not in (b'D', b'R', b'Q', b'M'):
            raise ValueError('not a data record at %d' % off)
        sta = h[8:13].decode().strip(); loc = h[13:15].decode().strip()
        cha = h[15:18].decode().strip(); net = h[18:20].decode().strip()
        start = _btime_ns(h[20:30])
        ns, srf, srm = struct.unpack('>Hhh', h[30:36])
        act, io, dq, nblk, tcorr, bod, bfb = struct.unpack('>BBBBiHH', h[36:48])
        enc = None; wo = 1; reclen = None; usec = 0
        b = bfb
        while b:
            btype, bnext = struct.unpack('>HH', raw[off + b:off + b + 4])
            if btype == 1000:
                enc, wo, rl = struct.unpack('>BBB', raw[off + b + 4:off + b + 7])
                reclen = 1 << rl
            elif btype == 1001:
                usec = struct.unpack('>b', raw[off + b + 5:off + b + 6])[0]
            b = bnext
        if reclen is None:
            raise ValueError('no blockette 1000')
        if wo != 1:
            raise ValueError('little-endian word order not supported')
        start += usec * 1000
        if (act & 0x02) == 0 and tcorr != 0:
            start += tcorr * 100_000  # time correction not yet applied (0.0001 s units)
        body = raw[off + bod:off + reclen]
        if ns == 0:
            data = np.zeros(0, np.int64)
        elif enc in (10, 11):
            nfr = len(body) // 64
            words = np.frombuffer(body[:nfr * 64], dtype='>u4').reshape(nfr, 16).astype(np.uint32)
            diffs, X0, Xn = _steim_diffs(words, 1 if enc == 10 else 2)
            if diffs.size < ns:
                raise ValueError('Steim: %d diffs < %d samples' % (diffs.size, ns))
            data = np.empty(ns, np.int64)
            data[0] = X0
            data[1:] = X0 + np.cumsum(diffs[1:ns])
            if check and data[-1] != Xn:
                raise ValueError('Steim reverse integration constant mismatch at record %d: %d vs %d'
                                 % (off // reclen, data[-1], Xn))
        elif enc == 3:
            data = np.frombuffer(body[:ns * 4], dtype='>i4').astype(np.int64)
        elif enc == 4:
            data = np.frombuffer(body[:ns * 4], dtype='>f4').astype(np.float64)
        elif enc == 5:
            data = np.frombuffer(body[:ns * 8], dtype='>f8').astype(np.float64)
        else:
            raise ValueError('unsupported encoding %s' % enc)
        recs.append(dict(net=net, sta=sta, loc=loc, cha=cha, start=start,
                         rate=_rate(srf, srm), data=data, seq=h[0:6].decode()))
        off += reclen
    return recs


def ns_to_iso(t):
    return str(np.datetime64(int(t), 'ns'))


if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        r = read_mseed(p)
        n = sum(len(x['data']) for x in r)
        last = r[-1]
        end = last['start'] + int(round((len(last['data']) - 1) / last['rate'] * 1e9))
        print(p.replace('\\', '/').split('/')[-1], 'records', len(r), 'samples', n,
              'rate', r[0]['rate'], 'start', ns_to_iso(r[0]['start']), 'end', ns_to_iso(end),
              'min', min(int(x['data'].min()) for x in r if len(x['data'])),
              'max', max(int(x['data'].max()) for x in r if len(x['data'])))
