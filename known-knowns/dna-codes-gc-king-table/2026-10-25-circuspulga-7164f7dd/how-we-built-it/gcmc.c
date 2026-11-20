/* gcmc.c: min-conflicts search for constant-GC quaternary codes with a full uint8/uint16 cost table.
   Word = (gi, b): gi indexes a weight-W subset g of positions (C/G positions), b in {0,1}^N picks A/T or C/G.
   Letter at p: g_p=0,b_p=0 -> A; 0,1 -> T; 1,0 -> C; 1,1 -> G.  dist = popcount((g1^g2)|(b1^b2)).
   cost[w] = sum over code words x != w of max(0, D - dist(w,x)).
   Move: remove a random conflicting word, insert the best non-tabu word (random tie-break). Every KICKIT moves
   without a new best, re-insert KICK random words. Checkpoint of the best state every 60 s to CKPT file.
   Usage: gcmc N D M SEED SECONDS CKPT [warmfile] ; prints WORD lines on success (exit 0), else exit 1. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
static int N,D,W,MASK,NG; static int gcm[20000]; static uint64_t rs;
static inline uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static uint16_t *cost;
static void update(long x, int sign){ int gx=gcm[x>>N], bx=(int)(x&MASK);
  for(int gi=0; gi<NG; gi++){ int gd=gcm[gi]^gx; uint16_t *row=cost+((long)gi<<N);
    for(int b=0;b<=MASK;b++){ int df=D-__builtin_popcount(gd|(b^bx)); if(df>0) row[b]+=sign*df; } } }
static inline int dist(long x,long y){ return __builtin_popcount((gcm[x>>N]^gcm[y>>N])|(int)((x^y)&MASK)); }
static const char L[4]={'A','T','C','G'};
static void word(long x,char*s){ int g=gcm[x>>N], b=(int)(x&MASK); for(int p=0;p<N;p++) s[p]=L[((g>>p)&1)*2+((b>>p)&1)]; s[N]=0; }
static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec; }
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage\n");return 2;}
  N=atoi(argv[1]); D=atoi(argv[2]); int M=atoi(argv[3]); unsigned long seed=strtoul(argv[4],0,10);
  rs=seed*2654435761ULL+88172645463325252ULL; double secs=atof(argv[5]); const char*ck=argv[6];
  W=N/2; MASK=(1<<N)-1; NG=0; for(int g=0;g<(1<<N);g++) if(__builtin_popcount(g)==W) gcm[NG++]=g;
  long NW=(long)NG<<N; cost=calloc(NW,sizeof(uint16_t)); if(!cost){fprintf(stderr,"oom\n");return 2;}
  printf("# gcmc N=%d D=%d W=%d M=%d seed=%lu words=%ld\n",N,D,W,M,seed,NW); fflush(stdout);
  long code[512], best[512]; int ninit=0;
  if(argc>7){ FILE*f=fopen(argv[7],"r"); char line[128]; while(ninit<M && fgets(line,128,f)){ char*s=line; if(!strncmp(s,"WORD ",5)) s+=5; if(s[0]<'A') continue; int g=0,b=0; for(int p=0;p<N;p++){ char c=s[p]; g|=(c=='C'||c=='G')<<p; b|=(c=='T'||c=='G')<<p; } int gi=-1; for(int k=0;k<NG;k++) if(gcm[k]==g){gi=k;break;} if(gi<0){fprintf(stderr,"bad warm word\n");return 2;} code[ninit]=((long)gi<<N)|b; update(code[ninit],+1); ninit++; } fclose(f); printf("# warm start %d words\n",ninit); }
  for(int i=ninit;i<M;i++){ code[i]=(long)(rnd()%NW); update(code[i],+1); }
  int KICKIT=300, KICK=2; long tabuw[64]; long tabut[64]; int nt=0; long it=0; double t0=now(), tck=t0; int total=0, bestc=1<<30; long lastimp=0;
  for(;;){
    total=0; int conf[512], nc=0;
    for(int i=0;i<M;i++){ int c=cost[code[i]]-D; /* remove self term (dist 0 contributes D) */ total+=c; if(c>0) conf[nc++]=i; }
    total/=2;
    if(total<bestc){ bestc=total; memcpy(best,code,sizeof(long)*M); lastimp=it; }
    if(total==0) break;
    double el=now()-t0; if(el>secs) break;
    if(now()-tck>60){ FILE*f=fopen(ck,"w"); fprintf(f,"# it=%ld t=%.0f bestcost=%d M=%d\n",it,el,bestc,M); for(int a=0;a<M;a++){char s[40]; word(best[a],s); fprintf(f,"%s\n",s);} fclose(f); tck=now(); }
    if(it%500==0){ printf("# it=%ld t=%.0fs cost=%d best=%d\n",it,el,total,bestc); fflush(stdout); }
    if(it-lastimp>KICKIT && it%KICKIT==0){ for(int k=0;k<KICK;k++){ int i=(int)(rnd()%M); update(code[i],-1); code[i]=(long)(rnd()%NW); update(code[i],+1);} it++; continue; }
    int i=conf[rnd()%nc]; long old=code[i];
    update(old,-1);
    int bc=1<<30, cnt=0; long bw=-1;
    for(long w=0; w<NW; w++){ int c=cost[w]; if(c>bc) continue; if(w==old) continue;
      int tb=0; for(int t=0;t<nt;t++) if(tabuw[t]==w && tabut[t]>it){tb=1;break;} if(tb) continue;
      if(c<bc){bc=c;cnt=1;bw=w;} else { cnt++; if(rnd()%cnt==0) bw=w; } }
    code[i]=bw; update(bw,+1);
    tabuw[it%64]=old; tabut[it%64]=it+7+(long)(rnd()%5); if(nt<64) nt++;
    it++;
  }
  double el=now()-t0;
  printf("# end it=%ld t=%.1fs cost=%d best=%d size=%d\n",it,el,total,bestc,M);
  { FILE*f=fopen(ck,"w"); fprintf(f,"# final it=%ld bestcost=%d M=%d\n",it,bestc,M); for(int a=0;a<M;a++){char s[40]; word(best[a],s); fprintf(f,"%s\n",s);} fclose(f); }
  if(bestc==0){ for(int a=0;a<M;a++) for(int b=a+1;b<M;b++) if(dist(best[a],best[b])<D){ printf("# INTERNAL ERROR\n"); return 3; }
    printf("# FOUND size=%d\n",M); for(int a=0;a<M;a++){ char s[40]; word(best[a],s); printf("WORD %s\n",s);} return 0; }
  return 1;
}
