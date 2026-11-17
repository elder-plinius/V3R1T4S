/* Deterministic bounded exhaustive simple directed-cycle suffix extension.
   All arities 3..n; optional subsequent swaps after a genuine long cycle.
   Actual preference counts at every node. */
#define CYCLE_LIBRARY
#include "cycle_search.c"
static uint64_t bestc,bar;static Word bestword;static const char*out;
static long nodes,cycle_paths,maxnodes;static double deadline;static int maxdepth,cutoff;
static void extend(Word*,int);
static void found(Word*W,Cycle c,int depth){
 if(nodes>=maxnodes||now_s()>deadline){cutoff=1;return;}W->g[W->len++]=c;Inst I;
 if(!make_inst(W,&I)){puts("INTERNAL invalid suffix");exit(5);}nodes++;uint64_t v=count_poset(&I);
 if(v>bestc){bestc=v;bestword=*W;snapshot(out,W,v,"best");printf("NEWBEST count=%llu depth=%d arity=%d nodes=%ld long=%d\n",(unsigned long long)v,depth,c.k,nodes,arities(W));fflush(stdout);
  if(v>bar){char tag[128],base[1200],p[1300];snprintf(tag,sizeof tag,"n%d.c%llu",nn,(unsigned long long)v);snapshot(out,W,v,tag);snprintf(base,sizeof base,"%s.%s",out,tag);snprintf(p,sizeof p,"%s.repro",base);FILE*f=fopen(p,"w");fprintf(f,"algorithm=deterministic_suffix_cycles nodes=%ld paths=%ld depth=%d maxdepth=%d maxnodes=%ld\n",nodes,cycle_paths,depth,maxdepth,maxnodes);fclose(f);receipt(base,&I,v);}
 }
 if(depth<maxdepth&&!cutoff)extend(W,depth+1);W->len--;
}
static void walk(Word*W,int depth,const unsigned*edge,Cycle *c,unsigned taken,int first){
 if(cutoff)return;if(++cycle_paths>maxnodes*100||now_s()>deadline){cutoff=1;return;}
 unsigned next=edge[c->a[c->k-1]];
 if((next>>first&1)&&c->k>=(depth==1?3:2))found(W,*c,depth);
 for(int b=first+1;b<nn;b++)if((next>>b&1)&&!(taken>>b&1)){c->a[c->k++]=b;walk(W,depth,edge,c,taken|(1u<<b),first);c->k--;if(cutoff)return;}
}
static void extend(Word*W,int depth){
 int M[MAXN];unsigned seen[MAXN],edge[MAXN]={0};memcpy(M,initial,sizeof M);for(int m=0;m<nn;m++)seen[m]=1u<<M[m];
 for(int t=0;t<W->len;t++){Cycle c=W->g[t];int dest[MAXN];for(int j=0;j<c.k;j++)dest[j]=M[c.a[(j+1)%c.k]];for(int j=0;j<c.k;j++){M[c.a[j]]=dest[j];seen[c.a[j]]|=1u<<dest[j];}}
 for(int a=0;a<nn;a++)for(int b=0;b<nn;b++)if(a!=b&&!(seen[a]>>M[b]&1))edge[a]|=1u<<b;
 for(int first=0;first<nn;first++){Cycle c={.k=1,.a={first}};walk(W,depth,edge,&c,1u<<first,first);if(cutoff)return;}
}
int main(int argc,char**argv){
 if(argc<7){puts("suffix_cycles INPUT OUTPREFIX SECONDS MAXNODES MAXDEPTH STARTWORD|-");return 1;}
 memo_max=1u<<20;if(!read_prefs(argv[1],&ordering))return 2;nn=ordering.n;if(nn!=13&&nn!=15&&nn!=17)return 2;out=argv[2];deadline=now_s()+atof(argv[3]);maxnodes=atol(argv[4]);maxdepth=atoi(argv[5]);Word w;
 bestc=count_poset(&ordering);w.len=nrot;for(int r=0;r<nrot;r++){w.g[r].k=rots[r].r;memcpy(w.g[r].a,rots[r].men,rots[r].r*sizeof(int));}gale_shapley(nn,ordering.mpref,ordering.wrank,initial);
 if(strcmp(argv[6],"-")&&!loadword(argv[6],&w))return 2;Inst I;if(!make_inst(&w,&I))return 3;bestc=count_poset(&I);bar=nn==13?9796:nn==15?38986:289548;bestword=w;snapshot(out,&w,bestc,"best");char p[1200];snprintf(p,sizeof p,"%s.tail.prefs",out);write_prefs(p,&ordering,"tail ordering template");
 printf("start n=%d count=%llu events=%d maxdepth=%d maxnodes=%ld seconds=%s\n",nn,(unsigned long long)bestc,w.len,maxdepth,maxnodes,argv[3]);fflush(stdout);extend(&w,1);
 printf("end n=%d best=%llu evaluated=%ld cycle_paths=%ld cutoff=%d\n",nn,(unsigned long long)bestc,nodes,cycle_paths,cutoff);return 0;
}
