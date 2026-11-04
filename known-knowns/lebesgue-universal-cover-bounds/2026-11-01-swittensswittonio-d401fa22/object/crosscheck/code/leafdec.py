"""Decoder for LEBCERTB certificates (format from REGENERATE.md / verifyB.py header+split rule)."""
import struct, numpy as np
TWO_PI = 2.0*np.pi
def _circ5():
    m=2; circ=1.0/(2.0*np.sin(np.pi*m/5)); a=TWO_PI*np.arange(5)/5
    V=np.stack([circ*np.cos(a),circ*np.sin(a)],1)
    return float(np.max(np.hypot(V[:,0],V[:,1])))
CIRC5=_circ5()

class Cert:
    def __init__(self,path):
        d=open(path,'rb').read(); self.d=d
        assert d[:8]==b"LEBCERTB"
        (self.target,self.thresh,self.tmax,self.m,self.K,self.depth,self.nseed)=struct.unpack("<dddiiii",d[8:48])
        (self.inflate,)=struct.unpack("<d",d[48:56]); (self.nblk,)=struct.unpack("<Q",d[56:64])
        o=64; self.sizes=np.frombuffer(d,dtype='<u4',count=self.nblk,offset=o).astype(np.int64); o+=4*self.nblk
        self.base=o; self.offs=np.concatenate([[0],np.cumsum(self.sizes)])
        assert o+self.offs[-1]==len(d)
        self.raw=np.frombuffer(d,dtype=np.uint8,offset=o)
        lut=np.array([bin(i).count('1') for i in range(256)],dtype=np.int64)
        ones=np.add.reduceat(lut[self.raw],self.offs[:-1])
        self.leaves=ones+1                      # one tree per block: ones = internal nodes = leaves-1
        self.cum=np.concatenate([[0],np.cumsum(self.leaves)])
        self.root=(0.0,self.tmax,0.0,self.tmax,np.pi/5,np.pi/5,0.0,self.tmax,0.0,self.tmax)
    def split(self,b):
        w=(b[1],b[3],CIRC5*b[5],b[7],b[9]); k=int(np.argmax(w)); half=b[2*k+1]*0.5; out=[]
        for s in (-1,1):
            n=list(b); n[2*k]=b[2*k]+s*half; n[2*k+1]=half*(1.0+self.inflate); out.append(tuple(n))
        return out
    def seed_box(self,i):
        b=self.root
        for lev in range(self.depth-1,-1,-1):
            b=self.split(b)[(i>>lev)&1]
        return b
    def walk(self,i,maxleaf=None):
        """yield (leaf_index_in_block, depth, box); raise if bitstream does not end exactly."""
        blk=self.raw[self.offs[i]:self.offs[i+1]].tobytes()
        stack=[(self.seed_box(i),self.depth)]; pos=0; k=0
        while stack:
            b,dp=stack.pop(); bit=(blk[pos>>3]>>(7-(pos&7)))&1; pos+=1
            if bit==0:
                yield k,dp,b; k+=1
                if maxleaf is not None and k>=maxleaf: return
            else:
                c1,c2=self.split(b); stack.append((c2,dp+1)); stack.append((c1,dp+1))
        assert not(pos>8*len(blk) or 8*len(blk)-pos>=8), "bitstream mismatch block %d"%i


class BlockIndex:
    """Random access into one block's pre-order bit tree without walking it (for heavy blocks).
    E[i] = (#ones - #zeros) in bits[:i]. Subtree starting at q ends (exclusive) at the first r>q with E[r]=E[q]-1."""
    def __init__(self,cert,i):
        self.c=cert; self.i=i
        raw=cert.raw[cert.offs[i]:cert.offs[i+1]]
        self.nbytes=len(raw)
        self.bits=np.unpackbits(raw)            # MSB first = pre-order
        step=np.where(self.bits==1,1,-1).astype(np.int32)
        self.E=np.concatenate([[0],np.cumsum(step,dtype=np.int32)])
        self.idx=np.argsort(self.E,kind='stable'); self.Es=self.E[self.idx]
        self.root=cert.seed_box(i)
        e0=self.end(0)
        assert 8*self.nbytes-e0<8 and not self.bits[e0:].any(), "bitstream mismatch block %d"%i   # exact consumption + zero padding
        self.nbits=e0
    def end(self,q):
        v=int(self.E[q])-1
        lo=np.searchsorted(self.Es,v,'left'); hi=np.searchsorted(self.Es,v,'right')
        seg=self.idx[lo:hi]; j=np.searchsorted(seg,q,'right')
        return int(seg[j])
    def leaf_pos(self,k):
        return int(np.flatnonzero(self.bits[:self.nbits]==0)[k]) if not hasattr(self,'_z') else int(self._z[k])
    def zeros(self):
        self._z=np.flatnonzero(self.bits[:self.nbits]==0); return self._z
    def descend_to_pos(self,p):
        q=0; b=self.root; depth=self.c.depth
        while q!=p:
            assert self.bits[q]==1
            c1,c2=self.c.split(b); e=self.end(q+1)
            if p<e: q=q+1; b=c1
            else: q=e; b=c2
            depth+=1
        assert self.bits[p]==0
        return b,depth
    def descend_to_box(self,target):
        q=0; b=self.root; depth=self.c.depth
        while self.bits[q]==1:
            c1,c2=self.c.split(b)
            w=(b[1],b[3],CIRC5*b[5],b[7],b[9]); ax=int(np.argmax(w))
            if target[2*ax]<b[2*ax]: q=q+1; b=c1
            else: q=self.end(q+1); b=c2
            depth+=1
        if b!=tuple(target): return None
        zb=(q-int(self.E[q]))//2                # zeros before position q = leaf index in block
        return zb,depth
