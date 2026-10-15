/* Arbitrary cyclic chronological construction, 2026-10-15.
   Actual preference evaluator credited to V3R1T4S lane A; swap-word reference lane X2.
   New: arbitrary cycle merge/fission, directed-cycle graft, long-cycle transport.
   Never uses a cycle-ideal bijection for acceptance. */
#define main reference_main_unused
#include "../reference/smcount3_copy.c"
#undef main
#include <unistd.h>
#include <signal.h>
#include "independent.h"
typedef struct {int k,a[MAXN];} Cycle;
typedef struct {int len;Cycle g[MAXR];} Word;
static int nn,initial[MAXN]; static Inst ordering;
static volatile sig_atomic_t stopping;
static void stopped(int s){(void)s;stopping=1;}
static int arities(const Word *W){int k=0;for(int i=0;i<W->len;i++)k+=W->g[i].k>2;return k;}
static int make_inst(const Word*W,Inst*I){
 int M[MAXN],nm[MAXN]={0},nw[MAXN]={0};unsigned used[MAXN]={0};I->n=nn;memcpy(M,initial,sizeof M);
 for(int m=0;m<nn;m++){int w=M[m];I->mpref[m][nm[m]++]=w;I->wpref[w][nw[w]++]=m;used[m]|=1u<<w;}
 for(int t=0;t<W->len;t++){
  const Cycle *c=&W->g[t];int dest[MAXN];unsigned men=0;
  if(c->k<2||c->k>nn)return 0;
  for(int j=0;j<c->k;j++){int a=c->a[j];if(a<0||a>=nn||(men>>a&1))return 0;men|=1u<<a;dest[j]=M[c->a[(j+1)%c->k]];if(used[a]>>dest[j]&1)return 0;}
  for(int j=0;j<c->k;j++){int a=c->a[j],w=dest[j];used[a]|=1u<<w;M[a]=w;I->mpref[a][nm[a]++]=w;I->wpref[w][nw[w]++]=a;}
 }
 for(int m=0;m<nn;m++)for(int p=0;p<nn;p++){int w=ordering.mpref[m][p];if(!(used[m]>>w&1))I->mpref[m][nm[m]++]=w;}
 for(int w=0;w<nn;w++){for(int a=0,b=nw[w]-1;a<b;a++,b--){int t=I->wpref[w][a];I->wpref[w][a]=I->wpref[w][b];I->wpref[w][b]=t;}for(int p=0;p<nn;p++){int m=ordering.wpref[w][p];if(!(used[m]>>w&1))I->wpref[w][nw[w]++]=m;}}
 build_ranks(I);return check_perms(I);
}
static void mapping(Cycle c,int *p){for(int i=0;i<nn;i++)p[i]=i;for(int i=0;i<c.k;i++)p[c.a[i]]=c.a[(i+1)%c.k];}
static int overlap(Cycle a,Cycle b){for(int i=0;i<a.k;i++)for(int j=0;j<b.k;j++)if(a.a[i]==b.a[j])return 1;return 0;}
static int merge_at(Word *W,int at){
 if(at<0||at+1>=W->len||!overlap(W->g[at],W->g[at+1]))return 0;
 int p[MAXN],q[MAXN],r[MAXN],seen[MAXN]={0};Cycle out[MAXN];int z=0;
 mapping(W->g[at],p);mapping(W->g[at+1],q);for(int i=0;i<nn;i++)r[i]=p[q[i]];
 for(int i=0;i<nn;i++)if(!seen[i]&&r[i]!=i){Cycle c={0};int j=i;do{seen[j]=1;c.a[c.k++]=j;j=r[j];}while(j!=i);out[z++]=c;}
 if(z>2||!z)return 0;
 int haslong=0;for(int i=0;i<z;i++)haslong|=out[i].k>=3;if(!haslong)return 0;
 memmove(W->g+at+z,W->g+at+2,(W->len-at-2)*sizeof(Cycle));for(int i=0;i<z;i++)W->g[at+i]=out[i];W->len+=z-2;return 1;
}
static int split_at(Word *W,int at){
 Cycle c=W->g[at];if(c.k<3||W->len>=MAXR-2)return 0;
 int pivot=rndint(c.k),cut=1+rndint(c.k-2);Cycle a={0},b={0};
 b.a[b.k++]=c.a[pivot];for(int j=cut+1;j<c.k;j++)b.a[b.k++]=c.a[(pivot+j)%c.k];
 for(int j=0;j<=cut;j++)a.a[a.k++]=c.a[(pivot+j)%c.k];
 memmove(W->g+at+2,W->g+at+1,(W->len-at-1)*sizeof(Cycle));W->g[at]=b;W->g[at+1]=a;W->len++;return 1;
}
/* Transport s right past t: s,t -> t,t^{-1}s t as maps on positions.
   Product map is s(t(x)); conjugate map t^{-1}(s(t(x))) relabels s by t^{-1}. */
static void transport_right(Word *W,int at){Cycle s=W->g[at],t=W->g[at+1];int p[MAXN],inv[MAXN];mapping(t,p);for(int i=0;i<nn;i++)inv[p[i]]=i;for(int i=0;i<s.k;i++)s.a[i]=inv[s.a[i]];W->g[at]=t;W->g[at+1]=s;}
static int bridge(Word *W){
 if(!W->len)return 0;
 if(rndint(100)<52){for(int tries=0;tries<20;tries++){int at=rndint(W->len);if(split_at(W,at))return 1;}return 0;}
 int at=rndint(W->len-1);return merge_at(W,at);
}
static int transport(Word *W){
 if(W->len<3)return 0;int at=-1;
 for(int t=0;t<20;t++){int j=rndint(W->len-1);if(W->g[j].k>=3){at=j;break;}}
 if(at<0){at=rndint(W->len-1);if(!merge_at(W,at))return 0;}
 int steps=1+rndint(12);for(int j=0;j<steps&&at+1<W->len;j++,at++)transport_right(W,at);
 if(rndint(2)&&at+1<W->len)merge_at(W,at);
 if(rndint(3)==0)split_at(W,at);return 1;
}
static int graft(Word *W){
 if(W->len>=MAXR-2)return 0;int at=rndint(W->len+1),M[MAXN],end[MAXN];unsigned seen[MAXN]={0};memcpy(M,initial,sizeof M);
 for(int m=0;m<nn;m++)seen[m]=1u<<M[m];
 for(int t=0;t<W->len;t++){if(t==at)memcpy(end,M,sizeof end);Cycle c=W->g[t];int d[MAXN];for(int j=0;j<c.k;j++)d[j]=M[c.a[(j+1)%c.k]];for(int j=0;j<c.k;j++){M[c.a[j]]=d[j];seen[c.a[j]]|=1u<<d[j];}}
 if(at==W->len)memcpy(end,M,sizeof end);
 int k=3+rndint(nn<6?nn-2:4);Cycle c={.k=k};
 for(int attempt=0;attempt<30;attempt++){
  unsigned taken=0;int ok=1;c.a[0]=rndint(nn);taken|=1u<<c.a[0];
  for(int j=1;j<k;j++){int choices[MAXN],z=0;for(int b=0;b<nn;b++)if(!(taken>>b&1)&&!(seen[c.a[j-1]]>>end[b]&1))choices[z++]=b;if(!z){ok=0;break;}c.a[j]=choices[rndint(z)];taken|=1u<<c.a[j];}
  if(!ok||(seen[c.a[k-1]]>>end[c.a[0]]&1))continue;
  memmove(W->g+at+1,W->g+at,(W->len-at)*sizeof(Cycle));W->g[at]=c;W->len++;return 1;
 }return 0;
}
static int mutate(Word *W,int mode){
 int r=rndint(100);
 if(mode==1)return r<85?bridge(W):transport(W);
 if(mode==2)return r<65?graft(W):bridge(W);
 if(mode==3)return r<70?transport(W):bridge(W);
 if(r<50)return bridge(W);if(r<80)return transport(W);return graft(W);
}
static void saveword(const char *p,const Word *W){FILE*f=fopen(p,"w");fprintf(f,"%d %d\n",nn,W->len);for(int i=0;i<nn;i++)fprintf(f,"%d%c",initial[i],i==nn-1?'\n':' ');for(int t=0;t<W->len;t++){fprintf(f,"%d",W->g[t].k);for(int j=0;j<W->g[t].k;j++)fprintf(f," %d",W->g[t].a[j]);fprintf(f,"\n");}fclose(f);}
static int loadword(const char *p,Word*W){FILE*f=fopen(p,"r");if(!f)return 0;int n;fscanf(f,"%d %d",&n,&W->len);if(n!=nn||W->len<0||W->len>=MAXR){fclose(f);return 0;}for(int i=0;i<nn;i++)fscanf(f,"%d",initial+i);for(int t=0;t<W->len;t++){fscanf(f,"%d",&W->g[t].k);if(W->g[t].k<2||W->g[t].k>nn){fclose(f);return 0;}for(int j=0;j<W->g[t].k;j++)fscanf(f,"%d",&W->g[t].a[j]);}fclose(f);return 1;}
static void snapshot(const char*out,const Word*W,uint64_t c,const char *tag){char p[1200],cm[256];Inst I;snprintf(p,sizeof p,"%s.%s.word",out,tag);saveword(p,W);if(!make_inst(W,&I))exit(8);snprintf(p,sizeof p,"%s.%s.prefs",out,tag);snprintf(cm,sizeof cm,"cycle construction count=%llu long_cycles=%d",(unsigned long long)c,arities(W));write_prefs(p,&I,cm);}
static void receipt(const char*out,const Inst*I,uint64_t c){char p[1200];snprintf(p,sizeof p,"%s.receipt",out);FILE*f=fopen(p,"w");double t=now_s();uint64_t x=independent_count(I,25,100000000);fprintf(f,"actual_preference_poset=%llu\nindependent_CSP=%llu\ncomplete=%d\nnodes=%llu\nseconds=%.6f\n",(unsigned long long)c,(unsigned long long)x,!ic_abort,(unsigned long long)ic_nodes,now_s()-t);fflush(f);if(ic_abort){long l=I->n<=16?count_lattice(I,1):count_lattice25(I,1);fprintf(f,"verified_lattice=%ld\nagree=%d\n",l,(uint64_t)l==c);if((uint64_t)l!=c)exit(7);}else{fprintf(f,"agree=%d\n",x==c);if(x!=c)exit(7);}fclose(f);}
#ifndef CYCLE_LIBRARY
int main(int argc,char**argv){
 signal(SIGTERM,stopped);memo_max=1u<<20;
 if(argc>=3&&!strcmp(argv[1],"verify")){Inst I;if(!read_prefs(argv[2],&I))return 2;double t=now_s();uint64_t c=count_poset(&I),x=independent_count(&I,argc>3?atof(argv[3]):25,100000000);printf("n=%d poset=%llu independent_CSP=%llu complete=%d nodes=%llu seconds=%.4f agree=%d\n",I.n,(unsigned long long)c,(unsigned long long)x,!ic_abort,(unsigned long long)ic_nodes,now_s()-t,!ic_abort&&c==x);return ic_abort?9:c!=x;}
 if(argc<7){puts("usage: cycle_search INPUT OUTPREFIX SECONDS SEED MODE TEMP [STARTWORD] [MAXPROPOSALS]");return 1;}
 if(!read_prefs(argv[1],&ordering))return 2;nn=ordering.n;if(nn!=13&&nn!=15&&nn!=17){puts("target domain forbidden");return 2;}
 rs=strtoull(argv[4],0,10);if(!rs)rs=1;int mode=atoi(argv[5]);double temp=atof(argv[6]),secs=atof(argv[3]);const char*out=argv[2];long maxp=argc>8?atol(argv[8]):10000000;
 Word cur,best,cand;uint64_t original=count_poset(&ordering);cur.len=nrot;for(int r=0;r<nrot;r++){cur.g[r].k=rots[r].r;memcpy(cur.g[r].a,rots[r].men,rots[r].r*sizeof(int));}gale_shapley(nn,ordering.mpref,ordering.wrank,initial);
 if(argc>7&&strcmp(argv[7],"-")){if(!loadword(argv[7],&cur))return 2;}
 Inst I;if(!make_inst(&cur,&I))return 3;uint64_t cc=count_poset(&I),bc=cc;best=cur;uint64_t bar=nn==13?9796:nn==15?38986:289548;
 snapshot(out,&best,bc,"best");char p[1200];snprintf(p,sizeof p,"%s.tail.prefs",out);write_prefs(p,&ordering,"unused pair ordering template");
 printf("start pid=%d n=%d original=%llu initial=%llu len=%d long=%d seed=%s mode=%d temp=%g seconds=%g maxproposals=%ld\n",getpid(),nn,(unsigned long long)original,(unsigned long long)cc,cur.len,arities(&cur),argv[4],mode,temp,secs,maxp);fflush(stdout);
 long proposed=0,changed=0,valid=0,acc=0,longvalid=0,worse=0;double t0=now_s(),last=t0;int epoch=0;
 while(!stopping&&proposed<maxp&&now_s()-t0<secs){
  /* deterministic 5000-valid-evaluation cooling cycles, restart at incumbent. */
  int e=(int)(valid/5000);if(e!=epoch){epoch=e;cur=best;cc=bc;}
  double T=temp*pow(0.03,(valid%5000)/5000.0);
  cand=cur;proposed++;if(!mutate(&cand,mode))continue;changed++;if(!make_inst(&cand,&I))continue;valid++;longvalid+=arities(&cand)>0;
  uint64_t c=count_poset(&I);int accept=c>=cc||(T>0&&log((double)c/cc)/T>-40&&(double)(rnd()>>11)/9007199254740992.0<exp(log((double)c/cc)/T));
  if(accept){worse+=c<cc;cur=cand;cc=c;acc++;if(c>bc){best=cur;bc=c;snapshot(out,&best,bc,"best");printf("NEWBEST count=%llu len=%d long=%d proposed=%ld valid=%ld rng=%llu\n",(unsigned long long)c,cur.len,arities(&cur),proposed,valid,(unsigned long long)rs);fflush(stdout);if(c>bar){char tag[100],base[1200];snprintf(tag,sizeof tag,"n%d.c%llu",nn,(unsigned long long)c);snapshot(out,&best,bc,tag);snprintf(base,sizeof base,"%s.%s",out,tag);char state[1300];snprintf(state,sizeof state,"%s.repro",base);FILE*f=fopen(state,"w");fprintf(f,"seed=%s mode=%d temp=%.17g proposal=%ld valid=%ld rng=%llu input=%s\n",argv[4],mode,temp,proposed,valid,(unsigned long long)rs,argv[1]);fclose(f);receipt(base,&I,c);}}}
  if(now_s()-last>=10){last=now_s();snapshot(out,&cur,cc,"current");snprintf(p,sizeof p,"%s.state",out);FILE*f=fopen(p,"w");fprintf(f,"rng=%llu proposed=%ld changed=%ld valid=%ld accepted=%ld longvalid=%ld worse=%ld current=%llu best=%llu epoch=%d\n",(unsigned long long)rs,proposed,changed,valid,acc,longvalid,worse,(unsigned long long)cc,(unsigned long long)bc,epoch);fclose(f);printf("checkpoint elapsed=%.2f proposed=%ld changed=%ld valid=%ld accepted=%ld longvalid=%ld worse=%ld current=%llu best=%llu len=%d long=%d\n",last-t0,proposed,changed,valid,acc,longvalid,worse,(unsigned long long)cc,(unsigned long long)bc,cur.len,arities(&cur));fflush(stdout);}
 }
 snapshot(out,&cur,cc,"current");snapshot(out,&best,bc,"best");snprintf(p,sizeof p,"%s.state",out);FILE*f=fopen(p,"w");fprintf(f,"rng=%llu proposed=%ld changed=%ld valid=%ld accepted=%ld longvalid=%ld worse=%ld current=%llu best=%llu epoch=%d\n",(unsigned long long)rs,proposed,changed,valid,acc,longvalid,worse,(unsigned long long)cc,(unsigned long long)bc,epoch);fclose(f);
 printf("end elapsed=%.3f proposed=%ld changed=%ld valid=%ld accepted=%ld longvalid=%ld worse=%ld current=%llu best=%llu len=%d long=%d\n",now_s()-t0,proposed,changed,valid,acc,longvalid,worse,(unsigned long long)cc,(unsigned long long)bc,cur.len,arities(&cur));return 0;
}
#endif
