"""Minimal OLE2 (CFB) + BIFF8 reader: dump every sheet of a .xls as TSV. Standard library only.
Usage: python -I xls_dump.py <file.xls> <outdir>"""
import sys, os, struct, datetime

def u16(b, o): return struct.unpack_from('<H', b, o)[0]
def u32(b, o): return struct.unpack_from('<I', b, o)[0]

class CFB:
    def __init__(self, data):
        assert data[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1', 'not an OLE2 file'
        self.d = data
        self.ssz = 1 << u16(data, 30)
        self.msz = 1 << u16(data, 32)
        self.n_fat = u32(data, 44)
        self.dir0 = u32(data, 48)
        self.cutoff = u32(data, 56)
        self.mfat0, self.n_mfat = u32(data, 60), u32(data, 64)
        self.difat0, self.n_difat = u32(data, 68), u32(data, 72)
        self.fat = self._fat()
        self.dirs = self._dirs()
        root = self.dirs[0]
        self.mini = self._read_chain(root[2], root[3], mini=False)
        self.mfat = self._mini_fat()

    def sect(self, n):
        off = (n + 1) * self.ssz
        return self.d[off:off + self.ssz]

    def _fat(self):
        difat = [u32(self.d, 76 + 4 * i) for i in range(109)]
        nxt, left = self.difat0, self.n_difat
        while nxt not in (0xFFFFFFFE, 0xFFFFFFFF) and left > 0:
            s = self.sect(nxt)
            per = self.ssz // 4 - 1
            difat += [u32(s, 4 * i) for i in range(per)]
            nxt = u32(s, 4 * per)
            left -= 1
        fat = []
        for sec in difat[:self.n_fat]:
            if sec in (0xFFFFFFFE, 0xFFFFFFFF):
                continue
            s = self.sect(sec)
            fat += [u32(s, 4 * i) for i in range(self.ssz // 4)]
        return fat

    def _mini_fat(self):
        out, nxt, left = [], self.mfat0, self.n_mfat
        while nxt not in (0xFFFFFFFE, 0xFFFFFFFF) and left > 0:
            s = self.sect(nxt)
            out += [u32(s, 4 * i) for i in range(self.ssz // 4)]
            nxt = self.fat[nxt] if nxt < len(self.fat) else 0xFFFFFFFE
            left -= 1
        return out

    def _dirs(self):
        raw, nxt = b'', self.dir0
        while nxt not in (0xFFFFFFFE, 0xFFFFFFFF):
            raw += self.sect(nxt)
            nxt = self.fat[nxt] if nxt < len(self.fat) else 0xFFFFFFFE
        out = []
        for i in range(len(raw) // 128):
            e = raw[128 * i:128 * i + 128]
            nl = u16(e, 64)
            name = e[:max(0, nl - 2)].decode('utf-16-le', 'ignore')
            out.append((name, e[66], u32(e, 116), struct.unpack_from('<Q', e, 120)[0]))
        return out

    def _read_chain(self, start, size, mini):
        buf, nxt = b'', start
        fat = self.mfat if mini else self.fat
        unit = self.msz if mini else self.ssz
        guard = 0
        while nxt not in (0xFFFFFFFE, 0xFFFFFFFF) and guard < 10 ** 7:
            if mini:
                buf += self.mini[nxt * unit:(nxt + 1) * unit]
            else:
                buf += self.sect(nxt)
            nxt = fat[nxt] if nxt < len(fat) else 0xFFFFFFFE
            guard += 1
        return buf[:size] if size else buf

    def stream(self, name):
        for nm, typ, start, size in self.dirs:
            if nm == name and typ == 2:
                return self._read_chain(start, size, mini=(size < self.cutoff))
        return None


def records(buf):
    o, n = 0, len(buf)
    while o + 4 <= n:
        rid, ln = u16(buf, o), u16(buf, o + 2)
        yield o, rid, buf[o + 4:o + 4 + ln]
        o += 4 + ln


def parse_sst(buf, start_off):
    """Return list of strings; start_off = offset of the SST record header."""
    recs = []
    for o, rid, data in records(buf[start_off:]):
        if not recs:
            recs.append(data)            # the SST record itself
            continue
        if rid == 0x003C:                # CONTINUE
            recs.append(data)
        else:
            break
    blob = b''.join(recs)
    bounds, pos = [], 0
    for r in recs:
        bounds.append((pos, pos + len(r)))
        pos += len(r)
    n_unique = u32(blob, 4)
    p = 8
    out = []

    def is_start(p):                      # start of a CONTINUE block?
        return any(p == b[0] for b in bounds[1:])

    for _ in range(n_unique):
        if p + 3 > len(blob):
            break
        cch = u16(blob, p); flags = blob[p + 2]; p += 3
        rich = u16(blob, p) if flags & 0x08 else 0
        p += 2 if flags & 0x08 else 0
        ext = u32(blob, p) if flags & 0x04 else 0
        p += 4 if flags & 0x04 else 0
        wide = flags & 0x01
        chars, got = [], 0
        while got < cch:
            if is_start(p):               # continuation: a fresh flags byte
                wide = blob[p] & 0x01
                p += 1
            end_blk = min([b[1] for b in bounds if b[0] <= p < b[1]] or [len(blob)])
            take = min(cch - got, (end_blk - p) // (2 if wide else 1))
            if take <= 0:
                break
            raw = blob[p:p + take * (2 if wide else 1)]
            chars.append(raw.decode('utf-16-le' if wide else 'latin-1', 'ignore'))
            p += take * (2 if wide else 1); got += take
        out.append(''.join(chars))
        p += rich * 4 + ext
    return out


def rk_value(rk):
    if rk & 0x02:
        v = float(rk >> 2 if rk < 0x80000000 else (rk >> 2) - 0x40000000)
    else:
        v = struct.unpack('<d', struct.pack('<Q', (rk & 0xFFFFFFFC) << 32))[0]
    return v / 100.0 if rk & 0x01 else v


def serial(v):
    """Excel 1900 serial -> ISO string, if plausible as a date."""
    try:
        if 1 < v < 80000:
            d = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=float(v))
            return d.strftime('%Y-%m-%dT%H:%M:%S')
    except Exception:
        pass
    return ''


def main():
    path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    cfb = CFB(open(path, 'rb').read())
    wb = cfb.stream('Workbook') or cfb.stream('Book')
    assert wb, 'no Workbook stream'
    sheets, sst_off = [], None
    for o, rid, data in records(wb):
        if rid == 0x0085:                                  # BOUNDSHEET
            pos = u32(data, 0); nl = data[6]; flags = data[7]
            nm = data[8:8 + nl * (2 if flags & 1 else 1)].decode('utf-16-le' if flags & 1 else 'latin-1', 'ignore')
            sheets.append((pos, nm))
        elif rid == 0x00FC:                                # SST
            sst_off = o
    sst = parse_sst(wb, sst_off) if sst_off is not None else []
    sheets.sort()
    base = os.path.splitext(os.path.basename(path))[0]
    for i, (pos, nm) in enumerate(sheets):
        end = sheets[i + 1][0] if i + 1 < len(sheets) else len(wb)
        cells = {}
        for o, rid, data in records(wb[pos:end]):
            if rid in (0x00FD, 0x0203, 0x027E, 0x0006, 0x0205, 0x0201):
                r, c = u16(data, 0), u16(data, 2)
            if rid == 0x00FD:                               # LABELSST
                k = u32(data, 6); cells[(r, c)] = sst[k] if k < len(sst) else ''
            elif rid == 0x0203:                             # NUMBER
                v = struct.unpack_from('<d', data, 6)[0]
                cells[(r, c)] = repr(v) + (('  [' + serial(v) + ']') if serial(v) else '')
            elif rid == 0x027E:                             # RK
                v = rk_value(u32(data, 6)); cells[(r, c)] = repr(v) + (('  [' + serial(v) + ']') if serial(v) else '')
            elif rid == 0x00BD:                             # MULRK
                r, c0 = u16(data, 0), u16(data, 2)
                n = (len(data) - 6) // 6
                for j in range(n):
                    v = rk_value(u32(data, 4 + 6 * j + 2))
                    cells[(r, c0 + j)] = repr(v) + (('  [' + serial(v) + ']') if serial(v) else '')
            elif rid == 0x0006:                             # FORMULA (cached value)
                bits = data[6:14]
                if bits[6:8] == b'\xff\xff':
                    cells[(r, c)] = '<str/bool/err>'
                else:
                    v = struct.unpack('<d', bits)[0]
                    cells[(r, c)] = repr(v) + (('  [' + serial(v) + ']') if serial(v) else '')
            elif rid == 0x0207 and cells:                   # STRING (result of last FORMULA)
                cch = u16(data, 0); wide = data[2] & 1
                s = data[3:3 + cch * (2 if wide else 1)].decode('utf-16-le' if wide else 'latin-1', 'ignore')
                cells[max(cells)] = s
        if not cells:
            continue
        rows = max(k[0] for k in cells) + 1
        cols = max(k[1] for k in cells) + 1
        safe = ''.join(ch if ch.isalnum() else '_' for ch in nm)
        out = os.path.join(outdir, '%s__%s.tsv' % (base, safe))
        with open(out, 'w', encoding='utf-8', newline='\n') as f:
            for r in range(rows):
                f.write('\t'.join(str(cells.get((r, c), '')).replace('\t', ' ') for c in range(cols)) + '\n')
        print('%s  sheet=%r  rows=%d cols=%d' % (out, nm, rows, cols))


main()
