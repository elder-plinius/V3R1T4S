/* Independent stable-matching CSP enumeration: no rotations, ideals, or GS.
   Every pair of assigned men must use distinct women and create no blocking pair.
   Forward checking + minimum remaining values enumerate every satisfying bijection once. */
static uint32_t ic_allow[32][32][32];
static uint64_t ic_nodes,ic_total,ic_cap; static double ic_deadline; static int ic_abort,ic_n;
static void ic_dfs(uint32_t *dom,uint32_t todo){
 if(ic_abort)return;
 if(++ic_nodes>ic_cap || ((ic_nodes&16383)==0 && now_s()>ic_deadline)){ic_abort=1;return;}
 if(!todo){ic_total++;return;}
 int m=-1,small=33;
 for(uint32_t t=todo;t;t&=t-1){int k=__builtin_ctz(t),s=__builtin_popcount(dom[k]);if(s<small){m=k;small=s;}if(s==1)break;}
 uint32_t rest=todo&~(1u<<m);
 for(uint32_t choices=dom[m];choices;choices&=choices-1){
  int w=__builtin_ctz(choices),ok=1;uint32_t next[32];memcpy(next,dom,ic_n*sizeof(uint32_t));
  for(uint32_t t=rest;t;t&=t-1){int k=__builtin_ctz(t);next[k]&=ic_allow[m][w][k];if(!next[k]){ok=0;break;}}
  if(ok)ic_dfs(next,rest);
 }
}
static uint64_t independent_count(const Inst *I,double secs,uint64_t cap){
 ic_n=I->n;ic_total=ic_nodes=0;ic_abort=0;ic_cap=cap;ic_deadline=now_s()+secs;
 for(int m=0;m<ic_n;m++)for(int w=0;w<ic_n;w++)for(int k=0;k<ic_n;k++){
  uint32_t a=0;for(int v=0;v<ic_n;v++)if(w!=v && !(I->mrank[m][v]<I->mrank[m][w] && I->wrank[v][m]<I->wrank[v][k]) && !(I->mrank[k][w]<I->mrank[k][v] && I->wrank[w][k]<I->wrank[w][m]))a|=1u<<v;ic_allow[m][w][k]=a;
 }
 uint32_t dom[32];for(int i=0;i<ic_n;i++)dom[i]=(1u<<ic_n)-1;
 ic_dfs(dom,(1u<<ic_n)-1);return ic_total;
}
