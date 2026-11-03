/* tcnf: plain CNF whose UNSAT means "no h x w orphan" (column-transfer reachability, forward implications only).
   Vars: T[r][j] target bits; E[j][v] (forced true when column j of T == v); R[j][s] s=(p_j,p_{j+1}) reachable superset.
   Clauses: E[j][v] OR (T col j != v); (-R[j-1][a,b] -E[j][col(a,b,d)] R[j][b,d]); final -R[w][s].
   SAT model T => R >= true reachable set, all final false => T has no predecessor (orphan). Orphan => SAT. Usage: tcnf h w [BMASK SMASK] */
#include <stdio.h>
#include <stdlib.h>
int h,w,P,NS,NV; long BM=8,SM=12;
int tv(int r,int j){return 1+r*w+j;}
int ev(int j,int v){return 1+h*w+(j-1)*NV+v;}
int rv(int j,int s){return 1+h*w+w*NV+(j-1)*NS+s;}
int col(int a,int b,int d){int out=0;for(int r=0;r<h;r++){int n=0;for(int k=r;k<r+3;k++){n+=(a>>k)&1;n+=(d>>k)&1;if(k!=r+1)n+=(b>>k)&1;}
 int alive=(b>>(r+1))&1; int nb= alive? (SM>>n)&1 : (BM>>n)&1; out|=nb<<r;} return out;}
int main(int c,char**v){h=atoi(v[1]);w=atoi(v[2]);if(c>4){BM=atol(v[3]);SM=atol(v[4]);}
 P=h+2;NS=1<<(2*P);NV=1<<h;int npc=1<<P;
 int *C=malloc(sizeof(int)*(1L<<(3*P)));
 for(int a=0;a<npc;a++)for(int b=0;b<npc;b++)for(int d=0;d<npc;d++)C[(a<<(2*P))|(b<<P)|d]=col(a,b,d);
 long nvars=h*w+(long)w*NV+(long)w*NS; long ncl=(long)w*NV+(long)NS*npc + (long)(w-1)*npc*NS + NS;
 printf("p cnf %ld %ld\n",nvars,ncl);
 for(int j=1;j<=w;j++)for(int x=0;x<NV;x++){printf("%d",ev(j,x));for(int r=0;r<h;r++)printf(" %d",((x>>r)&1)?-tv(r,j-1):tv(r,j-1));printf(" 0\n");}
 for(int a=0;a<npc;a++)for(int b=0;b<npc;b++)for(int d=0;d<npc;d++)printf("%d %d 0\n",-ev(1,C[(a<<(2*P))|(b<<P)|d]),rv(1,(b<<P)|d));
 for(int j=2;j<=w;j++)for(int a=0;a<npc;a++)for(int b=0;b<npc;b++)for(int d=0;d<npc;d++)
   printf("%d %d %d 0\n",-rv(j-1,(a<<P)|b),-ev(j,C[(a<<(2*P))|(b<<P)|d]),rv(j,(b<<P)|d));
 for(int s=0;s<NS;s++)printf("%d 0\n",-rv(w,s));
 return 0;}
