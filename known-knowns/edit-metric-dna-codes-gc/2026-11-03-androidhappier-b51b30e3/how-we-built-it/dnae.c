// dnae.c - orbit-graph MN/TS tabu search for Sun-type (n,d,w)_4 DNA codes (edit metric, RC + fixed GC = floor(n/2)).
// Words base-4, A=0 C=1 G=2 T=3, complement c->3-c. Group <rev, s1=(C G), s2=(A T)> (order 8) acts on valid words and
// preserves edit distance and the RC relation. Subgroup K (always containing rc) chosen by mode G:
//   0: <rc>   1: <rc,rev>   2: <rc,s1>   3: <rev,s1,s2> (full)
// Vertex = K-orbit (rc-closed) with all internal pairwise edit distances >= d; weight = |orbit|/2 codewords.
// usage: dnae n d G seed seconds outprefix [restartL] [target]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
static int n,dd,G,N4,w;
static uint64_t rs; static inline uint64_t rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
static inline int sym(int x,int i){return (x>>(2*(n-1-i)))&3;}
static int rev_(int x){int r=0;for(int i=0;i<n;i++)r=r*4+sym(x,n-1-i);return r;}
static int mapc(int x,const int*m){int r=0;for(int i=0;i<n;i++)r=r*4+m[sym(x,i)];return r;}
static const int S1[4]={0,2,1,3}, S2[4]={3,1,2,0};
static int apply(int h,int x){ // h bits: 1=rev, 2=s1, 4=s2
  if(h&2)x=mapc(x,S1); if(h&4)x=mapc(x,S2); if(h&1)x=rev_(x); return x;}
static int ed(int a,int b,int lim){ int A[16],B[16]; for(int i=0;i<n;i++){A[i]=sym(a,i);B[i]=sym(b,i);}
  int prev[16],cur[16]; for(int j=0;j<=n;j++)prev[j]=j;
  for(int i=1;i<=n;i++){cur[0]=i;int mn=i;for(int j=1;j<=n;j++){int v=prev[j-1]+(A[i-1]!=B[j-1]);if(prev[j]+1<v)v=prev[j]+1;if(cur[j-1]+1<v)v=cur[j-1]+1;cur[j]=v;if(v<mn)mn=v;}
    if(mn>lim)return lim+1; memcpy(prev,cur,sizeof(int)*(n+1));}
  return prev[n];}
static int V; static int *ow; static int **orbW; static int *orbSz; static int *vorb;
static uint64_t *adj; static int W64;
static int *tight; static long long *sid,*sid2; static char *inS; static long long *tabu;
static int *Sl,*Sp,ns; static int *Al,*Ap,na; static int *Bl,*Bp,nb_;
static void setins(int *l,int *p,int *cntp,int v){p[v]=*cntp;l[(*cntp)++]=v;}
static void setdel(int *l,int *p,int *cntp,int v){int i=p[v];int last=l[--(*cntp)];l[i]=last;p[last]=i;p[v]=-1;}
static void reclass(int v,int oldt,long long oldsid,long long oldsid2){ // update A/B membership
  (void)oldsid;(void)oldsid2;
  if(inS[v])return;
  int inA=Ap[v]>=0,inB=Bp[v]>=0; int t=tight[v];
  int wantA=(t==0); int wantB=0; if(t>0){ long long u=sid[v]/t; wantB=(u*t==sid[v]&&sid2[v]==(long long)t*u*u);} 
  if(inA&&!wantA)setdel(Al,Ap,&na,v); if(!inA&&wantA)setins(Al,Ap,&na,v);
  if(inB&&!wantB)setdel(Bl,Bp,&nb_,v); if(!inB&&wantB)setins(Bl,Bp,&nb_,v);
}
static long long curw=0;
static void upd(int x,int sign){ long long id=x+1;
  if(sign>0){ if(Ap[x]>=0)setdel(Al,Ap,&na,x); if(Bp[x]>=0)setdel(Bl,Bp,&nb_,x); inS[x]=1; setins(Sl,Sp,&ns,x); curw+=ow[x]; }
  else { inS[x]=0; setdel(Sl,Sp,&ns,x); curw-=ow[x]; }
  uint64_t *row=adj+(size_t)x*W64;
  for(int wi=0;wi<W64;wi++){uint64_t b=row[wi];while(b){int z=wi*64+__builtin_ctzll(b);b&=b-1;
      tight[z]+=sign; sid[z]+=sign*id; sid2[z]+=sign*id*id; reclass(z,0,0,0);}}
  if(sign<0) reclass(x,0,0,0);
}
int main(int argc,char**argv){
  n=atoi(argv[1]);dd=atoi(argv[2]);G=atoi(argv[3]);rs=atoll(argv[4])*2654435761ULL+88172645463325252ULL;double tl=atof(argv[5]);const char*out=argv[6];
  long long RL=argc>7?atoll(argv[7]):4000; int target=argc>8?atoi(argv[8]):1<<30;
  N4=1<<(2*n); w=n/2; const int RC=7;
  int *vid=malloc(sizeof(int)*N4); int nv=0; int *words=malloc(sizeof(int)*N4);
  for(int x=0;x<N4;x++){vid[x]=-1;int g=0;for(int i=0;i<n;i++){int s=sym(x,i);g+=(s==1||s==2);} if(g!=w)continue; if(ed(x,apply(RC,x),dd)<dd)continue; vid[x]=nv;words[nv++]=x;}
  // full-group reps
  int *rep=malloc(sizeof(int)*nv),*rh=malloc(sizeof(int)*nv); for(int i=0;i<nv;i++)rep[i]=-1;
  int *reps=malloc(sizeof(int)*nv),nr=0;
  for(int i=0;i<nv;i++){ if(rep[i]>=0)continue; int x=words[i]; for(int h=0;h<8;h++){int y=vid[apply(h,x)]; if(rep[y]<0){rep[y]=nr;rh[y]=h;}} reps[nr++]=i; }
  // neighbour lists of reps (edit distance < dd, excluding itself)
  int **nb=malloc(sizeof(int*)*nr),*nbc=calloc(nr,sizeof(int)); int *tmp=malloc(sizeof(int)*nv); long long totnb=0;
  for(int r=0;r<nr;r++){int x=words[reps[r]];int c=0;for(int j=0;j<nv;j++){if(j==reps[r])continue;if(ed(x,words[j],dd-1)<dd)tmp[c++]=j;} nb[r]=malloc(sizeof(int)*(c+1));memcpy(nb[r],tmp,sizeof(int)*c);nbc[r]=c;totnb+=c;}
  fprintf(stderr,"n=%d d=%d w=%d valid=%d fullreps=%d avgdeg=%.1f\n",n,dd,w,nv,nr,(double)totnb/nr);
  // K orbits
  int gens[8],ng=0; if(G==0){gens[ng++]=0;gens[ng++]=RC;} else if(G==1){int h[4]={0,RC,1,RC^1};for(int i=0;i<4;i++)gens[ng++]=h[i];}
  else if(G==2){int h[4]={0,RC,2,RC^2};for(int i=0;i<4;i++)gens[ng++]=h[i];} else {for(int h=0;h<8;h++)gens[ng++]=h;}
  int *ko=malloc(sizeof(int)*nv);for(int i=0;i<nv;i++)ko[i]=-1; int nko=0; orbW=malloc(sizeof(int*)*nv);orbSz=malloc(sizeof(int)*nv);
  for(int i=0;i<nv;i++){if(ko[i]>=0)continue;int el[8],ne=0;for(int g=0;g<ng;g++){int y=vid[apply(gens[g],words[i])];int dup=0;for(int k=0;k<ne;k++)if(el[k]==y)dup=1;if(!dup)el[ne++]=y;}
    orbW[nko]=malloc(sizeof(int)*ne);memcpy(orbW[nko],el,sizeof(int)*ne);orbSz[nko]=ne;for(int k=0;k<ne;k++)ko[el[k]]=nko;nko++;}
  int *kv=malloc(sizeof(int)*nko); V=0; vorb=malloc(sizeof(int)*nko);
  for(int o=0;o<nko;o++){int ok=1;for(int a=0;a<orbSz[o]&&ok;a++)for(int b=a+1;b<orbSz[o];b++)if(ed(words[orbW[o][a]],words[orbW[o][b]],dd)<dd){ok=0;break;} kv[o]=ok?V:-1; if(ok){vorb[V]=o;V++;}}
  W64=(V+63)/64; adj=calloc((size_t)V*W64,8); ow=malloc(sizeof(int)*V); for(int v=0;v<V;v++)ow[v]=orbSz[vorb[v]]/2;
  for(int i=0;i<nv;i++){int vi=kv[ko[i]]; if(vi<0)continue; int r=rep[i],h=rh[i]; uint64_t*row=adj+(size_t)vi*W64;
    for(int k=0;k<nbc[r];k++){int y=vid[apply(h,words[nb[r][k]])]; int vy=kv[ko[y]]; if(vy>=0&&vy!=vi)row[vy>>6]|=1ULL<<(vy&63);}}
  fprintf(stderr,"G=%d Korbits=%d admissible=%d\n",G,nko,V); fflush(stderr);
  tight=calloc(V,sizeof(int));sid=calloc(V,8);sid2=calloc(V,8);inS=calloc(V,1);tabu=calloc(V,8);
  Sl=malloc(sizeof(int)*V);Sp=malloc(sizeof(int)*V);Al=malloc(sizeof(int)*V);Ap=malloc(sizeof(int)*V);Bl=malloc(sizeof(int)*V);Bp=malloc(sizeof(int)*V);
  ns=na=nb_=0; for(int v=0;v<V;v++){Sp[v]=Bp[v]=-1;setins(Al,Ap,&na,v);}
  double t0=now();long long it=0,lastimp=0,restarts=0;long long best=0;
  while(now()-t0<tl && best<target){
    it++;
    int moved=0;
    if(na>0){ for(int tr=0;tr<64&&!moved;tr++){int v=Al[rnd()%na]; if(tabu[v]<=it){upd(v,1);moved=1;}} 
      if(!moved){ for(int i=0;i<na;i++){int v=Al[i]; if(tabu[v]<=it||curw+ow[v]>best){upd(v,1);moved=1;break;}}}}
    if(!moved && nb_>0){ int bv=-1,bu=-1,bg=-1000000,ties=0;
      for(int i=0;i<nb_;i++){int v=Bl[i]; int u=(int)(sid[v]/tight[v])-1; int g=ow[v]-ow[u]; int asp=(curw+g>best);
        if(tabu[v]>it && !asp) continue; if(g>bg){bg=g;bv=v;bu=u;ties=1;} else if(g==bg){ties++; if(rnd()%ties==0){bv=v;bu=u;}} }
      if(bv>=0){ upd(bu,-1); upd(bv,1); tabu[bu]=it+7+rnd()%(nb_<10?nb_+1:10); moved=1; } }
    if(!moved && ns>0){ int u=Sl[rnd()%ns]; upd(u,-1); tabu[u]=it+7; }
    if(curw>best){best=curw;lastimp=it;char fn[512];sprintf(fn,"%s_n%d_d%d_G%d_k%lld.txt",out,n,dd,G,best);FILE*f=fopen(fn,"w");
      for(int i=0;i<ns;i++){int o=vorb[Sl[i]];int used[8],nu=0;for(int j=0;j<orbSz[o];j++){int x=words[orbW[o][j]];int skip=0;for(int k=0;k<nu;k++)if(used[k]==apply(RC,x))skip=1;if(skip)continue;used[nu++]=x;for(int p=0;p<n;p++)fputc("ACGT"[sym(x,p)],f);fputc('\n',f);}}fclose(f);
      fprintf(stderr,"FOUND k=%lld it=%lld t=%.1f restarts=%lld\n",best,it,now()-t0,restarts);fflush(stderr);}
    if(it-lastimp>RL){restarts++; while(ns>0)upd(Sl[0],-1); for(int v=0;v<V;v++)tabu[v]=0; lastimp=it;}
  }
  printf("BEST %lld its=%lld restarts=%lld t=%.1f\n",best,it,restarts,now()-t0);return 0;}
