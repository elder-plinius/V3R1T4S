# builds tampered copies of the author's small control certificate (family B, certB_test.bin, tau 0.83) in work/tamper/
import struct, shutil, os, sys
src = sys.argv[1] if len(sys.argv) > 1 else 'work/certB_test.bin'   # path of the author's small valid control certificate

out = 'work/tamper'; os.makedirs(out, exist_ok=True)
d = bytearray(open(src,'rb').read())
HDR = 8   # magic
# layout: magic 8 | target d | thresh d | tmax d | m i | K i | depth i | nseed i | inflate d | nblk Q | sizes I*nblk | blocks
nseed = struct.unpack_from('<i', d, 8+24+12)[0]
sizes_off = 8+40+8+8
sizes = struct.unpack_from('<%dI'%nseed, d, sizes_off)
data_off = sizes_off + 4*nseed
# find a seed with multiple bytes
big = max(range(nseed), key=lambda i: sizes[i]); boff = data_off + sum(sizes[:big])
print('seed', big, 'size', sizes[big], file=sys.stderr)
def w(name, b): open(os.path.join(out, name),'wb').write(bytes(b))
# 1 flipped bit: flip first bit (root of the block: 1 -> 0 makes it a leaf) of a big block; also flip a middle bit in another
b = bytearray(d); b[boff] ^= 0x80; w('flip_first_bit.bin', b)
b = bytearray(d); b[boff + sizes[big]//2] ^= 0x10; w('flip_mid_bit.bin', b)
# 2 truncated
w('truncated_file.bin', d[:len(d)-1000])
# truncated bitstream: shrink the last block by one byte and fix file length consistently (size table adjusted)
last = nseed-1
while sizes[last] < 2: last -= 1
b = bytearray(d[:data_off]); sz = list(sizes); sz[last] -= 1
struct.pack_into('<%dI'%nseed, b, sizes_off, *sz)
pos = data_off
for i in range(nseed):
    blk = d[pos:pos+sizes[i]]; pos += sizes[i]
    b += blk[:sz[i]]
w('truncated_block.bin', b)
# 3 tau raised
b = bytearray(d); struct.pack_into('<d', b, 8, 0.8348); w('tau_0.8348.bin', b)
b = bytearray(d); struct.pack_into('<d', b, 8, 0.8301); w('tau_0.8301.bin', b)   # just above the certificate's own emitter threshold margin
# 4 smaller domain
b = bytearray(d); struct.pack_into('<d', b, 8+16, 0.65); w('tmax_0.65.bin', b)
b = bytearray(d); struct.pack_into('<d', b, 8+16, 0.60); w('tmax_0.60.bin', b)
# 5 negative child inflation
b = bytearray(d); struct.pack_into('<d', b, 8+40, -1e-3); w('inflate_negative.bin', b)
b = bytearray(d); struct.pack_into('<d', b, 8+40, 0.0); w('inflate_zero.bin', b)
# 6 trailing garbage byte at end of file
w('trailing_byte.bin', d + b'\x00')
# 7 wrong magic
b = bytearray(d); b[7] = ord('X'); w('bad_magic.bin', b)
# 8 refined witness resolution header (m,K) -> must still be ACCEPTED (my verifier ignores them) 
b = bytearray(d); struct.pack_into('<ii', b, 8+24, 2048, 2048); w('accept_m_K_2048.bin', b)
b = bytearray(d); struct.pack_into('<ii', b, 8+24, 4096, 4096); w('accept_m_K_4096.bin', b)
print('ok')
