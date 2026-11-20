/* mcnf: SECOND encoding (written fresh, no code from tcnf.c). "No h x w orphan" as plain SAT, meet-in-the-middle shape.
   Predecessor = (h+2) x (w+2) grid; column q (0..w+1) is an (h+2)-bit word. Target column t (1..w) depends on pred columns t-1,t,t+1.
   Vars: X[i][t] target cell (row i, col t); Y[t][v] "target column t equals v" (forced by clause Y v (X != v));
         F[t][(p,q)] left superset: pair (pred col t, pred col t+1) reachable from the left, t = 0..m  (F[0] all true);
         B[t][(p,q)] right superset: pair (pred col t, pred col t+1) extendable to the right edge, t = m..w (B[w] all true).
   Left step  (t=1..m):   -F[t-1][(x,y)] v -Y[t][next(x,y,z)] v F[t][(y,z)]
   Right step (t=w..m+1): -B[t][(y,z)] v -Y[t][next(x,y,z)] v B[t-1][(x,y)]
   Join: -F[m][s] v -B[m][s] for all s.   SAT => target has no predecessor (any predecessor makes some s true in both). Orphan => exact sets satisfy.
   Usage: mcnf h w m BM SM [cubecol cubeval]   (cube: adds units on X[.][cubecol], cubecol in 1..w; no clauses dropped) */
#include <stdio.h>
#include <stdlib.h>
int h,w,m,W,NP; long bm,sm; unsigned char *nx;
long X(int i,int t){return 1+(long)(t-1)*h+i;}
long Y(int t,int v){return 1+(long)h*w+(long)(t-1)*(1<<h)+v;}
long Fv(int t,long s){return 1+(long)h*w+(long)w*(1<<h)+(long)t*NP+s;}          /* t=0..m (F[0] not used as var) */
long Bv(int t,long s){return 1+(long)h*w+(long)w*(1<<h)+(long)(m+1)*NP+(long)(t-m)*NP+s;} /* t=m..w */
int bit(long x,int r){return (x>>r)&1;}
int nextcol(int x,int y,int z){ int out=0; for(int i=0;i<h;i++){ int r=i+1; /* pred row of target row i */
   int cnt=0; for(int dr=-1;dr<=1;dr++){ cnt+=bit(x,r+dr)+bit(z,r+dr); if(dr) cnt+=bit(y,r+dr);} 
   int me=bit(y,r); int born = me ? ((sm>>cnt)&1) : ((bm>>cnt)&1); if(born) out|=1<<i; } return out; }
int main(int c,char**v){ h=atoi(v[1]); w=atoi(v[2]); m=atoi(v[3]); bm=atol(v[4]); sm=atol(v[5]); int cc=c>7?atoi(v[6]):0, cv=c>7?atoi(v[7]):0;
 if(m<1||m>=w){fprintf(stderr,"need 1<=m<w\n");return 2;} W=1<<(h+2); NP=W*W; nx=malloc((size_t)W*W*W);
 for(int x=0;x<W;x++)for(int y=0;y<W;y++)for(int z=0;z<W;z++) nx[((size_t)x*W+y)*W+z]=nextcol(x,y,z);
 long nv=Bv(w,NP-1); long ncl=(long)w*(1<<h) + (long)w*W*(long)NP + NP + (cc?h:0);
 printf("p cnf %ld %ld\n",nv,ncl);
 for(int t=1;t<=w;t++)for(int val=0;val<(1<<h);val++){ printf("%ld",Y(t,val)); for(int i=0;i<h;i++) printf(" %ld", bit(val,i)? -X(i,t): X(i,t)); printf(" 0\n"); }
 for(int t=1;t<=m;t++) for(int x=0;x<W;x++)for(int y=0;y<W;y++)for(int z=0;z<W;z++){ int k=nx[((size_t)x*W+y)*W+z];
   if(t==1) printf("%ld %ld 0\n",-Y(t,k),Fv(t,(long)y*W+z)); else printf("%ld %ld %ld 0\n",-Fv(t-1,(long)x*W+y),-Y(t,k),Fv(t,(long)y*W+z)); }
 for(int t=w;t>=m+1;t--) for(int x=0;x<W;x++)for(int y=0;y<W;y++)for(int z=0;z<W;z++){ int k=nx[((size_t)x*W+y)*W+z];
   if(t==w) printf("%ld %ld 0\n",-Y(t,k),Bv(t-1,(long)x*W+y)); else printf("%ld %ld %ld 0\n",-Bv(t,(long)y*W+z),-Y(t,k),Bv(t-1,(long)x*W+y)); }
 for(long s=0;s<NP;s++) printf("%ld %ld 0\n",-Fv(m,s),-Bv(m,s));
 if(cc) for(int i=0;i<h;i++) printf("%ld 0\n", bit(cv,i)? X(i,cc): -X(i,cc));
 return 0; }
