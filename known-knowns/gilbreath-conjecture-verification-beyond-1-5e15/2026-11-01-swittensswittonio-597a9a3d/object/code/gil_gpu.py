#!/usr/bin/env python
"""GPU pipeline: segmented sieve + Gilbreath local depths over a contiguous prime range.
Definitions (see PREREG.md): primes q_0,q_1,... of the range in increasing order (all primes >= A).
Block c owns gap entries i in [cM, cM+M) (row 1 entry i = q_{i+1}-q_i) and reads M+O gaps (overlap O).
Row k (k>=1) entry i = |row_{k-1}(i) - row_{k-1}(i+1)|, row 0 = primes.
depth(c) = smallest k>=1 with every owned entry of row k in {0,2}; must satisfy k < O (else flagged 0xFFFF).
"""
import os, sys, time, json, struct, argparse, hashlib
import numpy as np
import cupy as cp

M = 8192
O = 1536
KSTAR = 1280
L = M + O
T = 65536

SRC = r'''
typedef unsigned long long u64; typedef unsigned int u32;
#define T 65536
#define M 8192
#define O 1536
#define L (M+O)
#define KSTAR 1280

__device__ __forceinline__ u64 modmagic(u64 n,u64 p,u64 mg){ u64 q=__umul64hi(n,mg); u64 r=n-q*p; if(r>=p) r-=p; if(r>=p) r-=p; return r; }

extern "C" __global__ void k_big(const u32* __restrict__ primes, const u64* __restrict__ magic, int np, u64 lo, u64 NB, unsigned char* flags){
  int t=blockIdx.x*blockDim.x+threadIdx.x; if(t>=np) return;
  u64 p=primes[t];
  u64 r=modmagic(lo,p,magic[t]); u64 first=r?(p-r):0;
  if(((lo+first)&1ull)==0) first+=p;
  for(u64 j=first>>1; j<NB; j+=p) flags[j]=1;
}

extern "C" __global__ void k_small(const u32* __restrict__ sp, const u64* __restrict__ magic, int nsp, u64 lo, unsigned char* flags, int* tilecnt, const unsigned char* __restrict__ pat){
  extern __shared__ __align__(16) unsigned char s[];
  __shared__ int red[32];
  u64 base=(u64)blockIdx.x*T; u64 nb=lo+2*base;
  const uint4* g=(const uint4*)(flags+base); uint4* sh=(uint4*)s;
  // pattern index: j -> (lo+2j) mod 15015 related; pat holds period-15015 table indexed by (j mod 15015) for this window's lo
  u32 pj=(u32)(base%15015ull);
  for(int i=threadIdx.x;i<T/16;i+=blockDim.x){
    uint4 v=g[i];
    unsigned char* vb=(unsigned char*)&v;
    u32 q=pj+i*16; q%=15015;
    #pragma unroll
    for(int k=0;k<16;k++){ vb[k]|=pat[q]; q++; if(q==15015) q=0; }
    sh[i]=v;
  }
  __syncthreads();
  for(int q=threadIdx.x;q<nsp;q+=blockDim.x){
    u64 p=sp[q]; u64 r=modmagic(nb,p,magic[q]); u64 first=r?(p-r):0; if(((nb+first)&1ull)==0) first+=p;
    for(u64 j=first>>1;j<T;j+=p) s[j]=1;
  }
  __syncthreads();
  int c=0; uint4* gw=(uint4*)(flags+base);
  for(int i=threadIdx.x;i<T/16;i+=blockDim.x){
    uint4 v=sh[i]; gw[i]=v;
    c+=__popc((~v.x)&0x01010101u)+__popc((~v.y)&0x01010101u)+__popc((~v.z)&0x01010101u)+__popc((~v.w)&0x01010101u);
  }
  for(int o=16;o>0;o>>=1) c+=__shfl_down_sync(0xffffffffu,c,o);
  if((threadIdx.x&31)==0) red[threadIdx.x>>5]=c;
  __syncthreads();
  if(threadIdx.x==0){ int s2=0; for(int w=0;w<blockDim.x/32;w++) s2+=red[w]; tilecnt[blockIdx.x]=s2; }
}

extern "C" __global__ void k_emit(const unsigned char* __restrict__ flags, const long long* __restrict__ tileoff, u64 lo, u64* out){
  __shared__ int sc[256];
  u64 base=(u64)blockIdx.x*T; int t=threadIdx.x;
  const uint4* g=(const uint4*)(flags+base+t*256);
  uint4 v[16]; int c=0;
  #pragma unroll
  for(int k=0;k<16;k++){ v[k]=g[k]; c+=__popc((~v[k].x)&0x01010101u)+__popc((~v[k].y)&0x01010101u)+__popc((~v[k].z)&0x01010101u)+__popc((~v[k].w)&0x01010101u); }
  sc[t]=c; __syncthreads();
  for(int o=1;o<256;o<<=1){ int a=(t>=o)?sc[t-o]:0; __syncthreads(); sc[t]+=a; __syncthreads(); }
  long long pos=tileoff[blockIdx.x]+(sc[t]-c);
  const unsigned char* b=(const unsigned char*)v;
  u64 j0=base+t*256;
  for(int k=0;k<256;k++){ if(b[k]==0){ out[pos++]=lo+2*(j0+k); } }
}

__device__ __forceinline__ u32 funnel(u32 x,u32 y,int s){ return __funnelshift_r(x,y,s); }

extern "C" __global__ void k_rows(const u64* __restrict__ P, unsigned short* depth_out, unsigned char* clean_out, u64 chunk0){
  extern __shared__ u32 sm[];
  const int LW=L/2;             // 16-bit words
  u32* b0=sm; u32* b1=sm+(LW+2);
  u64 chunk=chunk0+blockIdx.x; u64 base=chunk*M;
  int t=threadIdx.x;
  for(int i=t;i<LW+2;i+=blockDim.x){ b0[i]=0; b1[i]=0; }
  __syncthreads();
  for(int i=t;i<LW;i+=blockDim.x){
    u64 a=P[base+2*i], b=P[base+2*i+1], c=P[base+2*i+2];
    b0[i]=(u32)(b-a) | ((u32)(c-b)<<16);
  }
  __syncthreads();
  u32* cur=b0; u32* nxt=b1;
  int row=1; int depth=0xFFFF; int cleanK=0;
  { // row 1 owned test (never clean in practice)
    u32 bad=0; for(int i=t;i<M/2;i+=blockDim.x) bad|=cur[i]&0xFFFDFFFDu;
    int anybad=__syncthreads_or(bad!=0);
    if(!anybad){ depth=1; }
  }
  bool bytes=false;
  while(row<KSTAR){
    if(!bytes){
      u32 big=0; int nvalid=L-(row-1);
      for(int i=t;i<LW;i+=blockDim.x){
        int nv=nvalid-2*i; u32 m= nv>=2?0xFF00FF00u:(nv==1?0x0000FF00u:0u);
        big|=cur[i]&m;
      }
      int anybig=__syncthreads_or(big!=0);
      if(!anybig){
        for(int j=t;j<L/4;j+=blockDim.x){
          u32 w0=cur[2*j], w1=cur[2*j+1];
          nxt[j]=(w0&0xFFu)|(((w0>>16)&0xFFu)<<8)|((w1&0xFFu)<<16)|(((w1>>16)&0xFFu)<<24);
        }
        if(t==0){ nxt[L/4]=0; }
        __syncthreads();
        u32* tmp=cur; cur=nxt; nxt=tmp; bytes=true;
        for(int i=t;i<LW+2;i+=blockDim.x) nxt[i]=0;
        __syncthreads();
        continue;
      }
      u32 bad=0;
      for(int i=t;i<LW;i+=blockDim.x){
        u32 x=cur[i], y=cur[i+1]; u32 n=funnel(x,y,16); u32 nw=__vabsdiffu2(x,n);
        nxt[i]=nw; if(i<M/2) bad|=nw&0xFFFDFFFDu;
      }
      row++;
      int anybad=__syncthreads_or(bad!=0);
      { u32* tmp=cur; cur=nxt; nxt=tmp; }
      if(depth==0xFFFF && !anybad) depth=row;
      if(row==KSTAR) cleanK=!anybad;
    } else {
      u32 bad=0;
      for(int i=t;i<L/4;i+=blockDim.x){
        u32 x=cur[i], y=cur[i+1]; u32 n=funnel(x,y,8); u32 nw=__vabsdiffu4(x,n);
        nxt[i]=nw; if(i<M/4) bad|=nw&0xFDFDFDFDu;
      }
      row++;
      int anybad=__syncthreads_or(bad!=0);
      { u32* tmp=cur; cur=nxt; nxt=tmp; }
      if(depth==0xFFFF && !anybad) depth=row;
      if(row==KSTAR) cleanK=!anybad;
    }
  }
  if(t==0) clean_out[blockIdx.x]=(unsigned char)cleanK;
  if(t==0) depth_out[blockIdx.x]=(unsigned short)depth;
}
'''

mod = cp.RawModule(code=SRC, options=('-std=c++17',))
k_big = mod.get_function('k_big'); k_small = mod.get_function('k_small')
k_emit = mod.get_function('k_emit'); k_rows = mod.get_function('k_rows')

def odd_primes_upto(n):
    s = np.ones(n//2+1, dtype=bool); s[0]=False
    for i in range(1, int(n**0.5)//2+1):
        if s[i]:
            p = 2*i+1; s[(p*p)//2::p] = False
    return (2*np.nonzero(s)[0]+1).astype(np.uint32)

def ref_clean(P, c):
    seg = np.asarray(P[c*M : c*M+L+1], dtype=np.int64)
    a = np.abs(np.diff(seg))
    for k in range(2, KSTAR+1): a = np.abs(np.diff(a))
    return bool(np.all((a[:M] == 0) | (a[:M] == 2)))

def ref_depth(P, c):
    """independent numpy reference for block c from the prime list P (numpy uint64/int64 slice of length >= (c+1)M+O+1)."""
    seg = np.asarray(P[c*M : c*M+L+1], dtype=np.int64)
    a = np.abs(np.diff(seg)); k = 1
    while True:
        if np.all((a[:M] == 0) | (a[:M] == 2)): return k
        k += 1
        if k >= O: return 0xFFFF
        a = np.abs(np.diff(a))

def magic_of(p):
    return np.array([(1<<64)//int(x) for x in p], dtype=np.uint64)

class Pipe:
    SMALL_MAX = 262144
    def __init__(self, NB=1<<30, cap=None, pmax=40_100_000):
        self.NB = NB; assert NB % T == 0
        allp = odd_primes_upto(pmax)
        sm = allp[(allp < self.SMALL_MAX) & (allp > 13)]
        bg = allp[allp >= self.SMALL_MAX]
        self.small = cp.asarray(sm); self.big = cp.asarray(bg)
        self.msmall = cp.asarray(magic_of(sm)); self.mbig = cp.asarray(magic_of(bg))
        self.nsmall = int(sm.size); self.nbig = int(bg.size)
        self.flags = cp.zeros(NB, dtype=cp.uint8)
        self.ntile = NB//T
        self.tilecnt = cp.zeros(self.ntile, dtype=cp.int32)
        self.cap = cap or int(NB*2/30)+ (1<<22) + 100000
        self.P = cp.zeros(self.cap, dtype=cp.uint64)
        self.carry = 0
        self.smem = 2*(L//2+2)*4
        k_small.max_dynamic_shared_size_bytes = T
        self.xs = np.arange(15015, dtype=np.int64)
    def pattern(self, lo):
        pat = np.zeros(15015, dtype=np.uint8)
        for q in (3,5,7,11,13):
            pat |= (((lo + 2*self.xs) % q) == 0).astype(np.uint8)
        return cp.asarray(pat)
    def sieve(self, lo, dst_off):
        """sieve odd numbers lo, lo+2, ..., lo+2(NB-1) (lo odd); append primes into P at dst_off. returns count"""
        NB = self.NB
        self.flags[:] = 0
        k_big(((self.nbig+255)//256,), (256,), (self.big, self.mbig, np.int32(self.nbig), np.uint64(lo), np.uint64(NB), self.flags))
        k_small((self.ntile,), (256,), (self.small, self.msmall, np.int32(self.nsmall), np.uint64(lo), self.flags, self.tilecnt, self.pattern(lo)), shared_mem=T)
        off = cp.cumsum(self.tilecnt, dtype=cp.int64)
        total = int(off[-1]); off = off - self.tilecnt.astype(cp.int64) + dst_off
        assert dst_off + total <= self.cap, "cap"
        k_emit((self.ntile,), (256,), (self.flags, off, np.uint64(lo), self.P))
        return total
    def rows(self, nch, chunk0, depth_out, clean_out):
        k_rows((nch,), (256,), (self.P, depth_out, clean_out, np.uint64(chunk0)), shared_mem=self.smem)

if __name__ == '__main__':
    pass
