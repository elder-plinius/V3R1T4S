/* X2 imported Hurwitz/circuit rewrite search. Counter credited to lane A.
   A word of man transpositions creates strict chronological men/reverse chronological women
   preferences if no man visits the same woman twice. Unvisited pairs go last on both sides.
   Mutations are Hurwitz transformations st -> t(tst) or (sts)s, commuting swaps,
   and occasional insertion/deletion/replacement. These correlate many preference-list edits. */
#define main smcount_main_unused
#include "smcount3_copy.c"
#undef main
#include <unistd.h>
#include "word_ideals.h"
typedef struct {int a,b;} Gate;
typedef struct {int len;Gate g[MAXR];} Word;
static int nn,initial[MAXN];static Inst ordering;
static int make_inst(const Word*W,Inst*I){int M[MAXN],nm[MAXN]={0},nw[MAXN]={0};unsigned used[MAXN]={0};I->n=nn;memcpy(M,initial,sizeof M);
 for(int m=0;m<nn;m++){int w=M[m];I->mpref[m][nm[m]++]=w;I->wpref[w][nw[w]++]=m;used[m]|=1u<<w;}
 for(int k=0;k<W->len;k++){int a=W->g[k].a,b=W->g[k].b,wa=M[a],wb=M[b];if((used[a]>>wb&1)||(used[b]>>wa&1))return 0;used[a]|=1u<<wb;used[b]|=1u<<wa;M[a]=wb;M[b]=wa;I->mpref[a][nm[a]++]=wb;I->mpref[b][nm[b]++]=wa;I->wpref[wb][nw[wb]++]=a;I->wpref[wa][nw[wa]++]=b;}
 for(int m=0;m<nn;m++)for(int p=0;p<nn;p++){int w=ordering.mpref[m][p];if(!(used[m]>>w&1))I->mpref[m][nm[m]++]=w;}
 for(int w=0;w<nn;w++){for(int a=0,b=nw[w]-1;a<b;a++,b--){int t=I->wpref[w][a];I->wpref[w][a]=I->wpref[w][b];I->wpref[w][b]=t;}for(int p=0;p<nn;p++){int m=ordering.wpref[w][p];if(!(used[m]>>w&1))I->wpref[w][nw[w]++]=m;}}
 build_ranks(I);return check_perms(I);
}
static int disjoint(Gate a,Gate b){return a.a!=b.a&&a.a!=b.b&&a.b!=b.a&&a.b!=b.b;}
#include "square_trade.inc"
static int square_rate=15;
static int swap_label(int x,Gate t){return x==t.a?t.b:x==t.b?t.a:x;}
static int local_mutate(Word*W){if(rndint(100)<square_rate&&square_trade(W))return 1;int type=W->len?rndint(100):90;if(type<85 && W->len>1){int k=rndint(W->len-1);Gate s=W->g[k],t=W->g[k+1];if(disjoint(s,t)){W->g[k]=t;W->g[k+1]=s;return 2;}
 if(rndint(2)){W->g[k]=t;W->g[k+1]=(Gate){swap_label(s.a,t),swap_label(s.b,t)};}else{W->g[k]=(Gate){swap_label(t.a,s),swap_label(t.b,s)};W->g[k+1]=s;}return 1;
 }if(type<94 && W->len<MAXR-1){int k=rndint(W->len+1),a=rndint(nn),b=rndint(nn-1);if(b>=a)b++;memmove(W->g+k+1,W->g+k,(W->len-k)*sizeof(Gate));W->g[k]=(Gate){a,b};W->len++;return 1;}
 if(type<97&&W->len){int k=rndint(W->len);memmove(W->g+k,W->g+k+1,(W->len-k-1)*sizeof(Gate));W->len--;return 1;}
 int k=rndint(W->len),a=rndint(nn),b=rndint(nn-1);if(b>=a)b++;W->g[k]=(Gate){a,b};return 1;}
/* Nonlocal circuit move: slide one crossing across a whole interval using
   Hurwitz conjugation. Validate only the complete result, allowing temporary
   repeated encounters inside the algebraic rewrite. Endpoint permutation is
   preserved by every braid identity. This differs from sequential-valid moves. */
static int slide_mutate(Word*W){
 if(W->len<2||rndint(100)>=65)return local_mutate(W);
 int a=rndint(W->len),b=rndint(W->len);if(a==b)return 2;
 if(a<b){for(int k=a;k<b;k++){Gate s=W->g[k],t=W->g[k+1];W->g[k]=t;W->g[k+1]=(Gate){swap_label(s.a,t),swap_label(s.b,t)};}}
 else{for(int k=a;k>b;k--){Gate s=W->g[k-1],t=W->g[k];W->g[k-1]=(Gate){swap_label(t.a,s),swap_label(t.b,s)};W->g[k]=s;}}
 return 1;
}
/* Ruin/recreate from routing: insert or replace a crossing, replay tokens,
   drop downstream encounters that would repeat a man-woman pair, then fill.
   Only the repaired final word is scored. */
static int repair_word(Word*W){
 int cur[MAXN];unsigned seen[MAXN]={0};memcpy(cur,initial,sizeof cur);
 for(int m=0;m<nn;m++)seen[m]=1u<<cur[m];int L=0;
 for(int k=0;k<W->len;k++){int a=W->g[k].a,b=W->g[k].b,wa=cur[a],wb=cur[b];
  if(a==b||(seen[a]>>wb&1)||(seen[b]>>wa&1))continue;
  W->g[L++]=W->g[k];cur[a]=wb;cur[b]=wa;seen[a]|=1u<<wb;seen[b]|=1u<<wa;}
 W->len=L;return 1;
}
static int mutate(Word*W){
 if(rndint(100)>=20)return slide_mutate(W);
 int k=rndint(W->len+1),a=rndint(nn),b=rndint(nn-1);if(b>=a)b++;
 if(k==W->len||rndint(2)){if(W->len>=MAXR-1)return 2;memmove(W->g+k+1,W->g+k,(W->len-k)*sizeof(Gate));W->len++;}
 W->g[k]=(Gate){a,b};repair_word(W);
 Inst I;
 for(int t=0;t<80;t++){Word X=*W;int j=rndint(X.len+1),c=rndint(nn),d=rndint(nn-1);if(d>=c)d++;
  if(X.len>=MAXR-1)break;memmove(X.g+j+1,X.g+j,(X.len-j)*sizeof(Gate));X.g[j]=(Gate){c,d};X.len++;
  if(make_inst(&X,&I))*W=X;
 }
 return 1;
}
static void saveword(const char*p,const Word*W){FILE*f=fopen(p,"w");fprintf(f,"%d %d\n",nn,W->len);for(int m=0;m<nn;m++)fprintf(f,"%d%c",initial[m],m==nn-1?'\n':' ');for(int k=0;k<W->len;k++)fprintf(f,"%d %d\n",W->g[k].a,W->g[k].b);fclose(f);}
static int loadword(const char*p,Word*W){FILE*f=fopen(p,"r");if(!f)return 0;int n;fscanf(f,"%d %d",&n,&W->len);if(n!=nn)return 0;for(int m=0;m<nn;m++)fscanf(f,"%d",initial+m);for(int k=0;k<W->len;k++)fscanf(f,"%d %d",&W->g[k].a,&W->g[k].b);fclose(f);return 1;}
static void save(const char*out,const Word*cur,const Word*best,long evals,long proposed,long valid,long acc,uint64_t cc,uint64_t bc){char p[1200],cm[300];Inst I;snprintf(p,sizeof p,"%s.current.word",out);saveword(p,cur);snprintf(p,sizeof p,"%s.best.word",out);saveword(p,best);make_inst(best,&I);snprintf(p,sizeof p,"%s.best.prefs",out);snprintf(cm,sizeof cm,"swapword best count=%llu rotations=%d",(unsigned long long)bc,best->len);write_prefs(p,&I,cm);snprintf(p,sizeof p,"%s.n%d.c%llu.prefs",out,nn,(unsigned long long)bc);write_prefs(p,&I,cm);snprintf(p,sizeof p,"%s.state",out);FILE*f=fopen(p,"w");fprintf(f,"%llu %ld %ld %ld %ld\n",(unsigned long long)rs,evals,proposed,valid,acc);fclose(f);}
int main(int argc,char**argv){if(argc<5){puts("usage swapword INPUT PREFPREFIX SECONDS RNGSEED");return 1;}char stop_path[1200];snprintf(stop_path,sizeof stop_path,"%s.stop",argv[2]);if(access(stop_path,F_OK)==0){puts("book stopped at checkpoint");return 99;}if(!read_prefs(argv[1],&ordering))return 2;nn=ordering.n;memo_max=1u<<22;square_rate=getenv("WORD_SQUARE")?atoi(getenv("WORD_SQUARE")):15;const char*out=argv[2];double secs=atof(argv[3]),temp=getenv("WORD_TEMP")?atof(getenv("WORD_TEMP")):0;rs=strtoull(argv[4],0,10);if(!rs)rs=1;
 Word cur,best,cand;count_poset(&ordering);cur.len=nrot;for(int r=0;r<nrot;r++){if(rots[r].r!=2){printf("non-transposition rotation length=%d\n",rots[r].r);return 3;}cur.g[r]=(Gate){rots[r].men[0],rots[r].men[1]};}gale_shapley(nn,ordering.mpref,ordering.wrank,initial);best=cur;
 long evals=0,proposed=0,valid=0,acc=0;char p[1200];snprintf(p,sizeof p,"%s.state",out);FILE*f=fopen(p,"r");if(f){unsigned long long s;fscanf(f,"%llu %ld %ld %ld %ld",&s,&evals,&proposed,&valid,&acc);fclose(f);rs=s;snprintf(p,sizeof p,"%s.current.word",out);if(!loadword(p,&cur))return 2;snprintf(p,sizeof p,"%s.best.word",out);if(!loadword(p,&best))return 2;}
 Inst I; if(!make_inst(&cur,&I))return 3;uint64_t cc=count_poset(&I);if(!make_inst(&best,&I))return 3;uint64_t bc=count_poset(&I);long e0=evals,p0=proposed,v0=valid;double t0=now_s(),last=t0;printf("start pid=%d n=%d current=%llu best=%llu wordlen=%d temp=%g evals=%ld proposed=%ld valid=%ld\n",getpid(),nn,(unsigned long long)cc,(unsigned long long)bc,cur.len,temp,evals,proposed,valid);fflush(stdout);
 while(now_s()-t0<secs && (!getenv("MAX_PROPOSALS") || proposed<atol(getenv("MAX_PROPOSALS")))){cand=cur;proposed++;int mt=mutate(&cand);if(mt==2){cur=cand;continue;}if(!make_inst(&cand,&I))continue;valid++;int flat[2*MAXR];for(int k=0;k<cand.len;k++){flat[2*k]=cand.g[k].a;flat[2*k+1]=cand.g[k].b;}uint64_t c=wi_count(nn,cand.len,initial,flat);if(wi_error){printf("WORD_ERROR %d\n",wi_error);return 6;}evals++;if((evals&1023)==0&&count_poset(&I)!=c){puts("WORD_POSET_MISMATCH");return 7;}int accept=c>=cc||(temp>0&&log((double)c/cc)>-30*temp&&(double)(rnd()>>11)/9007199254740992.0<exp(log((double)c/cc)/temp));if(accept){cur=cand;cc=c;acc++;if(c>bc){if(count_poset(&I)!=c){puts("NEWBEST_WORD_POSET_MISMATCH");return 7;}long L=nn<=16?count_lattice(&I,1):-1;if(L>=0&&(uint64_t)L!=c){printf("MISMATCH %llu %ld\n",(unsigned long long)c,L);return 5;}best=cur;bc=c;printf("NEWBEST count=%llu lattice=%ld wordlen=%d evals=%ld proposed=%ld\n",(unsigned long long)c,L,cur.len,evals,proposed);fflush(stdout);save(out,&cur,&best,evals,proposed,valid,acc,cc,bc);}}
 if(now_s()-last>10){last=now_s();save(out,&cur,&best,evals,proposed,valid,acc,cc,bc);printf("checkpoint elapsed=%.1f current=%llu best=%llu wordlen=%d evals=%ld proposed=%ld valid=%ld\n",last-t0,(unsigned long long)cc,(unsigned long long)bc,cur.len,evals,proposed,valid);fflush(stdout);}}
 save(out,&cur,&best,evals,proposed,valid,acc,cc,bc);printf("end elapsed=%.2f current=%llu best=%llu wordlen=%d evals=%ld proposed=%ld valid=%ld delta_evals=%ld delta_proposed=%ld delta_valid=%ld\n",now_s()-t0,(unsigned long long)cc,(unsigned long long)bc,cur.len,evals,proposed,valid,evals-e0,proposed-p0,valid-v0);return 0;}
