/* lant_cuda.cu - CUDA Langton's-ant exhaustive-box solver: one persistent thread = one ant at a time, threads pull
 * mask indices from a global atomic counter. Uses exactly the same lant_run() as the CPU solver (src/lant_core.h).
 * Output format identical to ref/lant_ref.c (see README):  mask tcap vx vy dir steps STATUS
 * WINDOW_OVERFLOW lines must be replaced by the reference run (scripts/fixup.sh does that).
 *
 *   nvcc -O3 -o lant_cuda src/lant_cuda.cu            (e.g. add -arch=sm_86 for an RTX 3090)
 *   ./lant_cuda W H START END CAP [THREADS]            (THREADS = persistent GPU threads, default 8192; each owns 256 KB + 5 KB)
 *
 * CPU-EMULATION BUILD (no GPU/nvcc needed; runs the SAME kernel source on the CPU, used to test the algorithm):
 *   gcc -O2 -x c -DLANT_EMULATE -Isrc -o lant_cuda_emu src/lant_cuda.cu
 * STATUS: written without access to a CUDA toolchain or GPU. The emulation build was tested; the CUDA build was NOT compiled or run. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lant_core.h"
typedef struct { long tc; long steps; int vx,vy,dc,r; } Res;

#ifdef LANT_EMULATE
#define LANT_GLOBAL
static unsigned long long emu_counter;
static unsigned atomicAddU(unsigned long long*p){ return (unsigned)((*p)++); }
#else
#define LANT_GLOBAL __global__
__device__ static inline unsigned atomicAddU(unsigned long long*p){ return (unsigned)atomicAdd(p,1ULL); }
#endif

/* Each thread slot `slot` owns planes G,P (PLANE_BYTES each) and a Ring. */
LANT_GLOBAL void lant_kernel(int W,int H,unsigned long long start,unsigned long long count,long cap,
                             uint8_t*Gall,uint8_t*Pall,Ring*Rall,Res*out,unsigned long long*counter,int slot){
#ifndef LANT_EMULATE
  slot=blockIdx.x*blockDim.x+threadIdx.x;
#endif
  uint8_t*G=Gall+(size_t)slot*PLANE_BYTES,*P=Pall+(size_t)slot*PLANE_BYTES; Ring*R=Rall+slot;
  for(;;){
    unsigned long long i=atomicAddU(counter);
    if(i>=count) break;
    Res q; q.tc=-1;q.vx=q.vy=q.dc=0;
    q.r=lant_run(W,H,start+i,cap,G,P,R,&q.tc,&q.vx,&q.vy,&q.dc,&q.steps);
    out[i]=q;
  }
}

#ifndef LANT_EMULATE
#define CK(x) do{cudaError_t e_=(x); if(e_!=cudaSuccess){fprintf(stderr,"CUDA error %s at %s:%d\n",cudaGetErrorString(e_),__FILE__,__LINE__);exit(2);}}while(0)
#endif

int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: lant_cuda W H START END CAP [THREADS]\n");return 1;}
  int W=atoi(argv[1]),H=atoi(argv[2]); unsigned long long ST=strtoull(argv[3],0,10),EN=strtoull(argv[4],0,10); long CAP=atol(argv[5]);
  int T=argc>6?atoi(argv[6]):8192; if(T<1)T=1; if(EN<=ST) return 0;
  unsigned long long N=EN-ST; if((unsigned long long)T>N) T=(int)N;   /* (CUDA build re-rounds T below) */
  Res*res=(Res*)malloc(sizeof(Res)*N);
#ifdef LANT_EMULATE
  uint8_t*G=(uint8_t*)calloc((size_t)T,PLANE_BYTES),*P=(uint8_t*)calloc((size_t)T,PLANE_BYTES); Ring*R=(Ring*)calloc((size_t)T,sizeof(Ring));
  emu_counter=0;
  /* emulate the persistent threads: round-robin one mask per slot, which exercises slot-private state like the GPU does */
  for(unsigned long long base=0;base<N;base+=T) for(int s=0;s<T&&base+s<N;s++){
    unsigned long long c=0; /* one-mask launch per slot using the identical kernel body */
    uint8_t*Gs=G+(size_t)s*PLANE_BYTES,*Ps=P+(size_t)s*PLANE_BYTES; Ring*Rs=R+s;
    Res q; q.tc=-1;q.vx=q.vy=q.dc=0; q.r=lant_run(W,H,ST+base+s,CAP,Gs,Ps,Rs,&q.tc,&q.vx,&q.vy,&q.dc,&q.steps); res[base+s]=q; (void)c; }
  /* also run the real kernel function once over the whole range on slot 0 as a self-consistency check of the kernel body */
  { Res*chk=(Res*)malloc(sizeof(Res)*N); unsigned long long cnt=0;
    lant_kernel(W,H,ST,N,CAP,G,P,R,chk,&cnt,0);
    if(memcmp(chk,res,sizeof(Res)*N)!=0){fprintf(stderr,"EMULATION MISMATCH between kernel body and per-slot run\n");return 3;} free(chk);}
#else
  int bs=128; int gs=(T+bs-1)/bs; T=gs*bs;      /* THREADS rounded up to a multiple of the block size */
  uint8_t*dG,*dP; Ring*dR; Res*dO; unsigned long long*dC;
  CK(cudaMalloc(&dG,(size_t)T*PLANE_BYTES)); CK(cudaMemset(dG,0,(size_t)T*PLANE_BYTES));
  CK(cudaMalloc(&dP,(size_t)T*PLANE_BYTES)); CK(cudaMemset(dP,0,(size_t)T*PLANE_BYTES));
  CK(cudaMalloc(&dR,(size_t)T*sizeof(Ring)));
  CK(cudaMalloc(&dO,sizeof(Res)*N)); CK(cudaMalloc(&dC,sizeof(unsigned long long))); CK(cudaMemset(dC,0,sizeof(unsigned long long)));
  lant_kernel<<<gs,bs>>>(W,H,ST,N,CAP,dG,dP,dR,dO,dC,0);
  CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
  CK(cudaMemcpy(res,dO,sizeof(Res)*N,cudaMemcpyDeviceToHost));
  cudaFree(dG);cudaFree(dP);cudaFree(dR);cudaFree(dO);cudaFree(dC);
#endif
  for(unsigned long long i=0;i<N;i++) printf("%llu %ld %d %d %d %ld %s\n",ST+i,res[i].tc,res[i].vx,res[i].vy,res[i].dc,res[i].steps,lant_status_name(res[i].r));
  return 0;
}
