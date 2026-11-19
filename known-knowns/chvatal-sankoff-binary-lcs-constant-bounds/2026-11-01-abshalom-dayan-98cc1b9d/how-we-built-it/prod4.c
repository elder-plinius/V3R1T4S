// prod4.c: certificate producer, any N up to 18, from an estimator table for window M. Decisions as in prod2.c (not shipped).
// LEAN mode (default for N >= 17, or env LEAN=1): V spilled to disk during pruning; values from the previous round held as int16 offsets from the estimator (resolution 1/2048) during the search only.
// usage: prod4 N M VMfile outprefix rounds sweeps impevery timecap_s maxstates xs
// Env: THETA, MEMCAP_MB, COUNT_ONLY=r (stop after the search of round r), POLISH=sweeps, POLISH_CAP=s, NEWFMT=1 (forced for N >= 17).
#include "lean4.h"
static int M; static u64 MM; static int16_t*VM; static int lean=0;
static inline float vhat(u64 s){u64 h=s&MN,b=s>>N;float best=-1e30f;int pc=0;for(int o=0;o<=N-M;o++){u64 hh=(h>>o)&MM,bb=(b>>o)&MM;if((bb>>(M-1))&1)bb=(~bb)&MM;float v=(float)pc+VM[hh|(bb<<M)]/2048.0f;if(v>best)best=v;pc+=(h>>o)&1;}return best;}
static double theta[8]={0,0,0,0,0,0,0,0};
static Set S,P; static int haveP=0; static i32*V=NULL,*PV=NULL; static int16_t*PD=NULL; static unsigned char*pol=NULL; static u64 n=0; static const char*pre; static u64 bits; static char tmpf[1024];
static void prune(double t0){
 if(lean){sp_write(tmpf,V,n);xfree(V);V=NULL;}
 Set R;set_init(&R,bits);u64 proc=1;
 for(u64 b=0;b<(1ULL<<(N-1));b++)set_add(&R,b<<N);
 while(proc){proc=0;for(u64 sl=0;sl<R.slots;sl++){u32 id=R.idx[sl];if(!id||!R.dirty[id-1])continue;R.dirty[id-1]=0;for(int w=0;w<CW;w++){u64 x=R.pool[(u64)(id-1)*CW+w];while(x){int t=__builtin_ctzll(x);x&=x-1;u64 s=(sl<<CBITS)|((u64)w<<6)|t;proc++;u64 i=set_rank(&S,s);int r;if(PBIT(pol,i)){set_add(&R,rowst(s,0));set_add(&R,rowst(s,1));}else{set_add(&R,shf(s,0,&r));set_add(&R,shf(s,1,&r));}}}}}
 set_build(&R);printf("pruned closed set: %llu of %llu chunks=%llu maxrss_MB=%.0f t=%.1f\n",(unsigned long long)R.cnt,(unsigned long long)n,(unsigned long long)R.nch,maxrss_mb(),now()-t0);fflush(stdout);memcheck("prune");
 if(lean){V=xalloc(R.cnt*4);}
 u64 j=0,i=0;SET_FOR(&S,s,if(set_has(&R,s)){int pb=PBIT(pol,i);V[j]=lean?sp_get(i):V[i];if(pb)pol[j>>3]|=1<<(j&7);else pol[j>>3]&=~(1<<(j&7));j++;}i++;);
 if(lean)sp_close();
 set_free(&S);S=R;n=R.cnt;printf(" compacted maxrss_MB=%.0f\n",maxrss_mb());fflush(stdout);memcheck("compact");
}
int main(int ac,char**av){N=atoi(av[1]);M=atoi(av[2]);MN=(1ULL<<N)-1;MM=(1ULL<<M)-1;const char*vf=av[3];pre=av[4];int rounds=atoi(av[5]);int sweeps=atoi(av[6]);int imp=atoi(av[7]);double cap=atof(av[8]);double t0=now();double maxs=atof(av[9]);int xs=atoi(av[10]);
 if(getenv("MEMCAP_MB"))memcap=(u64)atoll(getenv("MEMCAP_MB"))*1000000ULL;
 lean=(N>=17)||(getenv("LEAN")&&atoi(getenv("LEAN")));int newfmt=(N>=17)||(getenv("NEWFMT")&&atoi(getenv("NEWFMT")));
 u64 nm=1ULL<<(2*M-1);VM=xalloc(nm*2);FILE*f=fopen(vf,"rb");if(fread(VM,2,nm,f)!=nm){printf("VM read fail\n");return 1;}fclose(f);
 if(getenv("THETA")){char*e=strdup(getenv("THETA"));int ti=0;for(char*p=strtok(e,",");p&&ti<8;p=strtok(NULL,","))theta[ti++]=atof(p);if(ti>0)for(;ti<8;ti++)theta[ti]=theta[ti-1];}
 bits=1ULL<<(2*N-1);
 snprintf(tmpf,sizeof tmpf,"%s.pvtmp",pre);
 for(int rd=0;rd<rounds;rd++){
  if(!VM){VM=xalloc(nm*2);FILE*fq=fopen(vf,"rb");if(fread(VM,2,nm,fq)!=nm){printf("VM read fail\n");return 1;}fclose(fq);}
  if(haveP&&lean){ // previous-round values as int16 offsets from the estimator; exact values stay on disk
   sp_write(tmpf,V,P.cnt);PD=xalloc(P.cnt*2);u64 i=0;SET_FOR(&P,s,double d=((double)V[i]/K-vhat(s))*2048.0;if(d>32767)d=32767;if(d<-32767)d=-32767;PD[i]=(int16_t)d;i++;);xfree(V);V=NULL;printf(" offsets built maxrss_MB=%.0f t=%.1f\n",maxrss_mb(),now()-t0);fflush(stdout);memcheck("offsets");}
  set_init(&S,bits);u64 proc=1;
  for(u64 b=0;b<(1ULL<<(N-1));b++)set_add(&S,b<<N);
  #define PVAL(id,t) (lean?(double)vhat(t)+PD[id]/2048.0:(double)PV[id]/K)
  #define VAL(t) ((haveP&&set_has(&P,t))?PVAL(set_rank(&P,t),t):(double)vhat(t)+d0)
  while(proc){proc=0;for(u64 sl=0;sl<S.slots;sl++){u32 id=S.idx[sl];if(!id||!S.dirty[id-1])continue;S.dirty[id-1]=0;for(int w=0;w<CW;w++){u64 x_=S.pool[(u64)(id-1)*CW+w];while(x_){int t_=__builtin_ctzll(x_);x_&=x_-1;u64 s=(sl<<CBITS)|((u64)w<<6)|t_;proc++;u64 r0=rowst(s,0),r1=rowst(s,1);int r;u64 x0=shf(s,0,&r),x1=shf(s,1,&r);double A,B;
    double d0=0;if(haveP&&set_has(&P,s))d0=PVAL(set_rank(&P,s),s)-vhat(s);
    A=VAL(r0)+VAL(r1);B=VAL(x0)+VAL(x1)+2.0*r;
    double thn=theta[rd<8?rd:7]*2; if(A>B-thn){set_add(&S,r0);set_add(&S,r1);} if(B>A-thn||!(A>B-thn)){set_add(&S,x0);set_add(&S,x1);}
  }}}printf(" search pass expanded %llu chunks=%llu maxrss_MB=%.0f t=%.1f\n",(unsigned long long)proc,(unsigned long long)S.nch,maxrss_mb(),now()-t0);fflush(stdout);memcheck("search");}
  set_build(&S);n=S.cnt;printf("round %d: states=%llu chunks=%llu chunk_MB=%.0f maxrss_MB=%.0f t=%.1f\n",rd,(unsigned long long)n,(unsigned long long)S.nch,S.nch*64/1e6,maxrss_mb(),now()-t0);fflush(stdout);
  if(getenv("COUNT_ONLY")&&atoi(getenv("COUNT_ONLY"))==rd+1)return 0;
  if((double)n>maxs){printf("state cap exceeded, abort\n");return 2;}
  FILE*pf=NULL;static i32 pbuf[1<<16];u64 pb0=1,pb1=0;
  if(haveP&&lean){xfree(PD);PD=NULL;}
  if(haveP&&!lean){pf=fopen(tmpf,"wb");fwrite(PV,4,P.cnt,pf);fclose(pf);xfree(PV);PV=NULL;pf=fopen(tmpf,"rb");}
  pol=xalloc(n/8+1);
  if(lean){ // write the start potential to disk in pieces, with no V in memory while P and the estimator table are held
   char fo[1100];int pc=0;FILE*fw=NULL;u64 j=0;
   SET_FOR(&S,s,
     if(j%SP_ITEMS==0){if(fw)fclose(fw);snprintf(fo,sizeof fo,"%s.vo%d",tmpf,pc++);fw=fopen(fo,"wb");setvbuf(fw,NULL,_IOFBF,1<<20);}
     i32 v0;if(haveP&&set_has(&P,s))v0=sp_get(set_rank(&P,s));else v0=(i32)(vhat(s)*(float)K);fwrite(&v0,4,1,fw);
     u64 r0=rowst(s,0),r1=rowst(s,1);int r;u64 x0=shf(s,0,&r),x1=shf(s,1,&r);int ra=set_has(&S,r0)&&set_has(&S,r1);int sa=set_has(&S,x0)&&set_has(&S,x1);
     if(!ra&&!sa){printf("not closed?\n");return 3;}
     int act;if(ra&&sa){double A=(double)vhat(r0)+vhat(r1);double B=(double)vhat(x0)+vhat(x1)+2.0*r;act=A>B;}else act=ra;
     if(act)pol[j>>3]|=1<<(j&7);j++;);
   if(fw)fclose(fw);
   if(haveP){sp_close();set_free(&P);haveP=0;}
   xfree(VM);VM=NULL;
   V=xalloc(n*4);u64 got=0;for(int k=0;k<pc;k++){snprintf(fo,sizeof fo,"%s.vo%d",tmpf,k);FILE*fr=fopen(fo,"rb");got+=fread(V+got,4,SP_ITEMS,fr);fclose(fr);remove(fo);}
   if(got!=n){printf("start potential read back %llu of %llu\n",(unsigned long long)got,(unsigned long long)n);return 5;}
  }else{
  V=xalloc(n*4);
  u64 i=0;SET_FOR(&S,s,
     if(haveP&&set_has(&P,s)){u64 id=set_rank(&P,s);{if(id<pb0||id>=pb1){fseeko(pf,(off_t)id*4,SEEK_SET);size_t g=fread(pbuf,4,1<<16,pf);pb0=id;pb1=id+g;}V[i]=pbuf[id-pb0];}}else V[i]=(i32)(vhat(s)*(float)K);
     u64 r0=rowst(s,0),r1=rowst(s,1);int r;u64 x0=shf(s,0,&r),x1=shf(s,1,&r);int ra=set_has(&S,r0)&&set_has(&S,r1);int sa=set_has(&S,x0)&&set_has(&S,x1);
     if(!ra&&!sa){printf("not closed?\n");return 3;}
     int act;if(ra&&sa){double A=(double)vhat(r0)+vhat(r1);double B=(double)vhat(x0)+vhat(x1)+2.0*r;act=A>B;}else act=ra;
     if(act)pol[i>>3]|=1<<(i&7);i++;);
  if(haveP){fclose(pf);remove(tmpf);set_free(&P);haveP=0;}
  xfree(VM);VM=NULL;}
  u64 i;printf(" init maxrss_MB=%.0f t=%.1f\n",maxrss_mb(),now()-t0);fflush(stdout);memcheck("init");
  double rho=0.39*K;
  for(int sw=0;sw<sweeps;sw++){int doimp=(imp>0&&sw%imp==0);i64 mn=INT64_MAX,mx=INT64_MIN;double sumd=0;u64 changes=0;
   i=0;SET_FOR(&S,s,
     int act=PBIT(pol,i);i64 T=0;int r;
     if(doimp){u64 r0=rowst(s,0),r1=rowst(s,1),x0=shf(s,0,&r),x1=shf(s,1,&r);int ra=set_has(&S,r0)&&set_has(&S,r1);int sa=set_has(&S,x0)&&set_has(&S,x1);
       i64 A=INT64_MIN,B=INT64_MIN;if(ra)A=(i64)V[set_rank(&S,r0)]+V[set_rank(&S,r1)];if(sa)B=(i64)V[set_rank(&S,x0)]+V[set_rank(&S,x1)]+2*K*r;
       int na=A>B;if(na!=act){changes++;if(na)pol[i>>3]|=1<<(i&7);else pol[i>>3]&=~(1<<(i&7));act=na;}T=(act?A:B);}
     else if(act){u64 r0=rowst(s,0),r1=rowst(s,1);T=(i64)V[set_rank(&S,r0)]+V[set_rank(&S,r1)];}
     else{u64 x0=shf(s,0,&r),x1=shf(s,1,&r);T=(i64)V[set_rank(&S,x0)]+V[set_rank(&S,x1)]+2*K*r;}
     i64 d=T-2*(i64)V[i];if(d<mn)mn=d;if(d>mx)mx=d;sumd+=d;V[i]=(i32)(V[i]+(d-(i64)(2*rho))/4);i++;);
   rho=sumd/n/2;printf(" sweep %d mean %.7f gs-lo %.7f gs-hi %.7f chg=%llu maxrss_MB=%.0f t=%.1f\n",sw,rho/K,(double)mn/(2.0*K),(double)mx/(2.0*K),(unsigned long long)changes,maxrss_mb(),now()-t0);fflush(stdout);memcheck("sweep");
   if(now()-t0>cap){printf("time cap\n");break;}
  }
  prune(t0);
  if(rd<rounds-1){P=S;haveP=1;if(!lean){PV=V;V=NULL;}xfree(pol);pol=NULL;memset(&S,0,sizeof S);}
  if(now()-t0>cap&&rd<rounds-1){printf("ERROR no time for more rounds\n");return 4;}
 }
 double rho=0.39*K;
 for(int sw=0;sw<xs;sw++){i64 mn=INT64_MAX,mx=INT64_MIN;double sumd=0;u64 i=0;SET_FOR(&S,s,int r;i64 T;if(PBIT(pol,i)){T=(i64)V[set_rank(&S,rowst(s,0))]+V[set_rank(&S,rowst(s,1))];}else{u64 x0=shf(s,0,&r),x1=shf(s,1,&r);T=(i64)V[set_rank(&S,x0)]+V[set_rank(&S,x1)]+2*K*r;}i64 d=T-2*(i64)V[i];if(d<mn)mn=d;if(d>mx)mx=d;sumd+=d;V[i]=(i32)(V[i]+(d-(i64)(2*rho))/4);i++;);rho=sumd/n/2;printf(" final sweep %d mean %.7f lo %.7f hi %.7f t=%.1f\n",sw,rho/K,(double)mn/(2.0*K),(double)mx/(2.0*K),now()-t0);fflush(stdout);if(now()-t0>cap+120)break;}
 i64 mn=INT64_MAX,mx=INT64_MIN;{u64 i=0;SET_FOR(&S,s,int r;i64 T;if(PBIT(pol,i)){T=(i64)V[set_rank(&S,rowst(s,0))]+V[set_rank(&S,rowst(s,1))];}else{u64 x0=shf(s,0,&r),x1=shf(s,1,&r);T=(i64)V[set_rank(&S,x0)]+V[set_rank(&S,x1)]+2*K*r;}i64 d=T-2*(i64)V[i];if(d<mn)mn=d;if(d>mx)mx=d;i++;);}
 printf("FINAL N=%d states=%llu chunks=%llu E_min=%lld E_max=%lld K=%lld certified L=E_min/K=%.9f upper-ish=%.9f maxrss_MB=%.0f t=%.1f\n",N,(unsigned long long)n,(unsigned long long)S.nch,(long long)mn,(long long)mx,(long long)K,(double)mn/K,(double)mx/K,maxrss_mb(),now()-t0);fflush(stdout);
 if(getenv("POLISH")){int ms=atoi(getenv("POLISH"));double pc=getenv("POLISH_CAP")?atof(getenv("POLISH_CAP")):1e9;double t1=now();double rh=0.396*K;i64 mn2=0,mx2=0;
  for(int sw=0;sw<=ms;sw++){int frozen=(sw==ms||now()-t1>pc);mn2=INT64_MAX;mx2=INT64_MIN;double sum=0;u64 i=0;
   SET_FOR(&S,s,i64 T;int r;if(PBIT(pol,i)){T=(i64)V[set_rank(&S,rowst(s,0))]+V[set_rank(&S,rowst(s,1))];}else{u64 x0=shf(s,0,&r),x1=shf(s,1,&r);T=(i64)V[set_rank(&S,x0)]+V[set_rank(&S,x1)]+2*K*r;}i64 d=T-2*(i64)V[i];if(d<mn2)mn2=d;if(d>mx2)mx2=d;sum+=d;if(!frozen)V[i]=(i32)(V[i]+(d-(i64)(2*rh))/4);i++;);
   rh=sum/n/2;printf(" polish %d mean %.7f lo %.7f hi %.7f frozen=%d t=%.1f\n",sw,rh/K,(double)mn2/(2.0*K),(double)mx2/(2.0*K),frozen,now()-t0);fflush(stdout);if(frozen)break;}
  printf("POLISHED N=%d states=%llu E_min=%lld E_max=%lld certified L=%.9f upper-ish=%.9f maxrss_MB=%.0f t=%.1f\n",N,(unsigned long long)n,(long long)mn2,(long long)mx2,(double)mn2/K,(double)mx2/K,maxrss_mb(),now()-t0);fflush(stdout);}
 write_cert(pre,&S,pol,V,n,newfmt);
 return 0;}
