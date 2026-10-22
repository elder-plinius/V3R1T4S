// Memory-lean open-strip king-graph transfer matrix. Site-by-site frontier DP with frontier states indexed by
// (rank of new-part independent string, A bit, rank of old-part independent string); ranks are arithmetic (Fibonacci order).
// usage: tmlean m iters nthreads outprefix [count]   (count: exact Z(m, iters+1) printed; no scaling)
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "pthread.h"
typedef unsigned __int128 u128;
static int m, NT; static uint64_t *Cn; // Cn[k+1]=cnt[k]
#define CNT(k) (Cn[(k)+1])
static u128 *X, *Y;      // current (level i) and next (level i+1) frontier arrays
static int cur_i;
typedef struct {int t;} targ;
static void *work(void *p){
  int t=((targ*)p)->t; int i=cur_i;
  uint64_t c2=CNT(m-i-1);                 // old-part count at level i+1
  uint64_t cOld=CNT(m-i);                 // old-part count at level i
  uint64_t Ny=CNT(i+1)*2*c2;
  uint64_t lo=Ny/NT*t + (Ny%NT<(uint64_t)t?Ny%NT:t), hi=Ny/NT*(t+1)+(Ny%NT<(uint64_t)(t+1)?Ny%NT:(t+1));
  int Lo=m-i;
  uint64_t cs0=CNT(Lo-2);                 // old rest starting with 0 count (strings of length Lo-1 starting with 0)
  uint64_t cLo1=CNT(Lo-1);
  uint64_t idx=lo;
  while(idx<hi){
    uint64_t row=idx/c2, ro=idx%c2;
    uint64_t rn1=row>>1; int a=row&1;
    uint64_t seg_end = (hi-idx < c2-ro)? hi : idx+(c2-ro);
    int b = rn1>=CNT(i);
    uint64_t rn = b? rn1-CNT(i) : rn1;
    uint64_t base0=(rn*2+0)*cOld, base1=(rn*2+1)*cOld;
    uint64_t n=seg_end-idx;
    u128 *out=Y+idx;
    if(b==0){
      if(a==0){ for(uint64_t k=0;k<n;k++){ uint64_t r=ro+k; out[k]=X[base0+r]+X[base1+r]; } }
      else { for(uint64_t k=0;k<n;k++){ uint64_t r=ro+k; out[k]= (r<cs0)? X[base0+cLo1+r] : 0; } }
    } else {
      if(a==1){ for(uint64_t k=0;k<n;k++) out[k]=0; }
      else { for(uint64_t k=0;k<n;k++){ uint64_t r=ro+k; out[k]=(r<cs0)? X[base0+r] : 0; } }
    }
    idx=seg_end;
  }
  return 0;
}
int main(int argc,char**argv){
  m=atoi(argv[1]); int iters=atoi(argv[2]); NT=atoi(argv[3]); char*pre=argv[4]; int cnt_mode=(argc>5);
  Cn=malloc((m+4)*sizeof(uint64_t)); Cn[0]=1; Cn[1]=1; Cn[2]=2; for(int k=2;k<=m+1;k++) Cn[k+1]=Cn[k]+Cn[k-1];
  uint64_t mx=0; for(int i=0;i<=m;i++){ uint64_t s=CNT(i)*2*CNT(m-i); if(s>mx)mx=s; }
  X=malloc(mx*16); Y=malloc(mx*16);
  uint64_t nv=CNT(m);
  u128 *vec=malloc(nv*16), *vec2=malloc(nv*16);
  for(uint64_t r=0;r<nv;r++) vec[r]= cnt_mode? (u128)1 : ((u128)1<<60);
  int total = cnt_mode? iters : iters;   // sweeps
  for(int it=0; it<total; it++){
    // level 0: X[(0*2+A)*CNT(m)+ro]; A=0 only
    memset(X,0,CNT(m)*2*16); memcpy(X,vec,nv*16);
    for(int i=0;i<m;i++){
      cur_i=i; pthread_t th[64]; targ ta[64];
      for(int t=0;t<NT;t++){ta[t].t=t;pthread_create(&th[t],0,work,&ta[t]);}
      for(int t=0;t<NT;t++)pthread_join(th[t],0);
      u128*tmp=X;X=Y;Y=tmp;
    }
    // level m: idx=rn*2+A
    for(uint64_t r=0;r<nv;r++) vec2[r]=X[2*r]+X[2*r+1];
    if(cnt_mode){
      if(it==total-1){ u128 tot=0; for(uint64_t r=0;r<nv;r++) tot+=vec2[r];
        char buf[64]; int n=0; if(!tot)buf[n++]='0'; while(tot){buf[n++]='0'+(int)(tot%10);tot/=10;} while(n--)putchar(buf[n]); putchar('\n'); return 0; }
      memcpy(vec,vec2,nv*16); continue;
    }
    if(it==total-1){
      // sums of squares with 40-bit limbs: S = sum_k c[k] 2^(40k), for w=vec2 and v=vec
      for(int which=0;which<2;which++){
        u128 *a=which?vec:vec2; u128 c[5]={0,0,0,0,0};
        for(uint64_t r=0;r<nv;r++){ u128 x=a[r]; uint64_t x0=(uint64_t)(x&0xFFFFFFFFFFULL), x1=(uint64_t)((x>>40)&0xFFFFFFFFFFULL), x2=(uint64_t)(x>>80);
          c[0]+=(u128)x0*x0; c[1]+=(u128)2*x1*x0; c[2]+=(u128)x1*x1+(u128)2*x2*x0; c[3]+=(u128)2*x2*x1; c[4]+=(u128)x2*x2; }
        printf("%s",which?"V":"W");
        for(int k=0;k<5;k++){ char buf[64]; int n=0; u128 t=c[k]; if(!t)buf[n++]='0'; while(t){buf[n++]='0'+(int)(t%10);t/=10;} printf(" "); while(n--)putchar(buf[n]); }
        printf("\n");
      }
      break; }
    u128 M=0; for(uint64_t r=0;r<nv;r++) if(vec2[r]>M)M=vec2[r];
    int bl=0; u128 q=M; while(q){bl++;q>>=1;}
    int sh=bl-100;
    for(uint64_t r=0;r<nv;r++) vec[r]= sh>=0? (vec2[r]>>sh):(vec2[r]<<(-sh));
  }
  return 0;
}
