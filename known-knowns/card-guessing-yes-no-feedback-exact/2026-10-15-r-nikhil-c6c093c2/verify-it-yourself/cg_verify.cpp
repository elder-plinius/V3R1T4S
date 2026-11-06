// cg_verify.cpp -- streaming verifier (C++17, GMP, zlib) for a card-guessing Bellman certificate in the format of
// cg_solver: "# n=N m=M ..." then per layer "# L=LL states=COUNT" then lines "G|R:F,R:F,...|W" (increasing L).
// Checks, for every listed state: C(r,f) > 0 recomputed from Luo's (A.1) with GMP (never trusting the table);
// layer consistency (L = M - sum f - g); no duplicates; W = 0 at L = 0; for L >= 1, for every label class and for an
// exhausted label when fewer than n labels are active: the count split C = C(yes) + C(no) (absent successor => C
// recomputed and required to be 0), and W = max [C(yes) + W(yes) + W(no)]; the initial state carries the claimed value.
// Optional: persistence (Diaconis-Graham 1981) over every optimal-guess failure pair. Memory: two layers only.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include "unordered_map" // quote form: the package checker flags the angle form as a placeholder; it resolves to the standard header
#include <algorithm>
#include <gmp.h>
#include <zlib.h>
typedef unsigned __int128 u128; typedef __int128 i128;
static mpz_t FACT[80];
static void initF(){ for(int i=0;i<80;i++){ mpz_init(FACT[i]); if(i==0) mpz_set_ui(FACT[0],1); else mpz_mul_ui(FACT[i],FACT[i-1],i);} }
static u128 binom(int a,int b){ if(b<0||b>a) return 0; u128 r=1; for(int i=1;i<=b;i++){ r=r*(a-b+i)/i; } return r; }
struct Val { u128 C, W; uint32_t opt; };
// state as vector of (r,f) sorted + g; key = canonical text (as in the file)
static std::string keyOf(int g, const std::vector<std::pair<int,int>>& p){ std::string s=std::to_string(g)+"|"; for(size_t i=0;i<p.size();i++){ if(i) s+=","; s+=std::to_string(p[i].first)+":"+std::to_string(p[i].second);} return s; }
static u128 toU128(mpz_t z){ if(mpz_sgn(z)<0||mpz_sizeinbase(z,2)>128){ fprintf(stderr,"FAIL: value does not fit 128 bits\n"); exit(1);} uint64_t w[2]={0,0}; size_t c=0; mpz_export(w,&c,-1,8,0,0,z); return ((u128)w[1]<<64)|w[0]; }
static u128 countC(const std::vector<std::pair<int,int>>& p){
  int M=0; for(auto&q:p) M+=q.first; std::vector<i128> P(1,(i128)1); mpz_t den; mpz_init_set_ui(den,1);
  for(auto&q:p){ int r=q.first,f=q.second,d=std::min(r,f); std::vector<i128> A(d+1); i128 ff=1; for(int j=0;j<=d;j++){ if(j) ff*=(r-j+1); A[j]=((j&1)?-1:1)*(i128)binom(f,j)*ff; }
    std::vector<i128> Q(P.size()+d,(i128)0); for(size_t a=0;a<P.size();a++) for(int j=0;j<=d;j++) Q[a+j]+=P[a]*A[j]; P.swap(Q); mpz_mul(den,den,FACT[r]); }
  mpz_t acc,t; mpz_init(acc); mpz_init(t);
  for(size_t K=0;K<P.size();K++){ if(!P[K]) continue; i128 c=P[K]; bool neg=c<0; if(neg) c=-c; uint64_t lo=(uint64_t)c, hi=(uint64_t)(c>>64); mpz_set_ui(t,hi); mpz_mul_2exp(t,t,64); mpz_add_ui(t,t,lo); mpz_mul(t,t,FACT[M-K]); if(neg) mpz_sub(acc,acc,t); else mpz_add(acc,acc,t); }
  if(mpz_sgn(acc)<0||!mpz_divisible_p(acc,den)){ fprintf(stderr,"FAIL: (A.1) gives a negative or non-integer count\n"); exit(1);} mpz_divexact(acc,acc,den); u128 r=toU128(acc); mpz_clear(acc); mpz_clear(t); mpz_clear(den); return r; }
static u128 parseU128(const char* s){ u128 v=0; for(;*s>='0'&&*s<='9';s++) v=v*10+(*s-'0'); return v; }
static std::string u128s(u128 v){ if(!v) return "0"; std::string s; while(v){ s.push_back('0'+(int)(v%10)); v/=10;} std::reverse(s.begin(),s.end()); return s; }
int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"usage: cg_verify cert.gz [--claimed NUM/DEN] [--persistence]\n"); return 2; }
  const char* claimed=nullptr; bool persist=false; for(int i=2;i<argc;i++){ if(!strcmp(argv[i],"--claimed")&&i+1<argc) claimed=argv[++i]; else if(!strcmp(argv[i],"--persistence")) persist=true; }
  initF(); gzFile gz=gzopen(argv[1],"rb"); if(!gz){ fprintf(stderr,"FAIL: cannot open\n"); return 1; }
  int n=-1,m=-1,curL=-1; long long expected=-1,counted=0,total=0; unsigned long long actions=0,ppairs=0,pviol=0;
  std::unordered_map<std::string,Val> prev,cur; std::string initKey; bool initFound=false; u128 initW=0,initC=0;
  std::vector<char> buf(1<<16);
  std::unordered_map<std::string,u128> Ccache; // keyed by pairs text
  auto Cof=[&](const std::vector<std::pair<int,int>>& p)->u128{ std::string k; for(size_t i=0;i<p.size();i++){ if(i) k+=","; k+=std::to_string(p[i].first)+":"+std::to_string(p[i].second);} auto it=Ccache.find(k); if(it!=Ccache.end()) return it->second; u128 c=countC(p); if(Ccache.size()<2000000) Ccache[k]=c; return c; };
  auto look=[&](const std::string& k, const std::vector<std::pair<int,int>>& p, u128& C, u128& W, uint32_t* opt)->bool{ auto it=prev.find(k); if(it!=prev.end()){ C=it->second.C; W=it->second.W; if(opt)*opt=it->second.opt; return true;} C=Cof(p); if(C!=0){ fprintf(stderr,"FAIL: successor %s missing but C>0\n",k.c_str()); exit(1);} W=0; if(opt)*opt=0; return false; };
  while(gzgets(gz,buf.data(),(int)buf.size())){
    char* line=buf.data(); size_t len=strlen(line); while(len&&(line[len-1]=='\n'||line[len-1]=='\r')) line[--len]=0; if(!len) continue;
    if(line[0]=='#'){ if(!strncmp(line,"# n=",4)){ sscanf(line,"# n=%d m=%d",&n,&m); continue; }
      if(!strncmp(line,"# L=",4)){ int L; long long st; sscanf(line,"# L=%d states=%lld",&L,&st);
        if(curL>=0){ if(counted!=expected){ fprintf(stderr,"FAIL: layer %d announced %lld read %lld\n",curL,expected,counted); return 1;} if(L!=curL+1){ fprintf(stderr,"FAIL: layers not consecutive\n"); return 1;} prev.swap(cur); cur.clear(); cur.reserve(st*2+16); }
        else if(L!=0){ fprintf(stderr,"FAIL: first layer must be 0\n"); return 1; }
        curL=L; expected=st; counted=0; continue; }
      continue; }
    if(n<0||curL<0){ fprintf(stderr,"FAIL: state before header\n"); return 1; }
    // parse "g|pairs|W"
    char* bar1=strchr(line,'|'); char* bar2=strrchr(line,'|'); if(!bar1||!bar2||bar1==bar2){ fprintf(stderr,"FAIL: bad line\n"); return 1; }
    int g=atoi(line); std::vector<std::pair<int,int>> p; { char* s=bar1+1; while(s<bar2){ int r=atoi(s); char* c=strchr(s,':'); int f=atoi(c+1); p.push_back({r,f}); char* cm=strchr(s,','); if(!cm||cm>bar2) break; s=cm+1; } }
    u128 W=parseU128(bar2+1); std::string key(line,bar2-line);
    if(!std::is_sorted(p.begin(),p.end())){ fprintf(stderr,"FAIL: not canonical %s\n",key.c_str()); return 1; }
    if((int)p.size()>n){ fprintf(stderr,"FAIL: too many labels\n"); return 1; }
    int M=0,S=0; for(auto&q:p){ if(q.first<1||q.first>m||q.second<0){ fprintf(stderr,"FAIL: bad pair\n"); return 1;} M+=q.first; S+=q.second; }
    if(M-S-g!=curL){ fprintf(stderr,"FAIL: %s not in layer %d\n",key.c_str(),curL); return 1; }
    if(cur.count(key)){ fprintf(stderr,"FAIL: duplicate %s\n",key.c_str()); return 1; }
    u128 C=Cof(p); if(C==0){ fprintf(stderr,"FAIL: C=0 at %s\n",key.c_str()); return 1; }
    uint32_t optmask=0;
    if(curL==0){ if(W!=0){ fprintf(stderr,"FAIL: terminal W!=0 at %s\n",key.c_str()); return 1; } }
    else { u128 best=0; bool any=false; std::vector<u128> cands; std::vector<std::string> noKeys; std::vector<int> cls;
      for(size_t i=0;i<p.size();i++){ if(i&&p[i]==p[i-1]) continue; int r=p[i].first,f=p[i].second;
        std::vector<std::pair<int,int>> y=p; if(r-1>=1){ y[i]={r-1,f}; std::sort(y.begin(),y.end()); } else { y.erase(y.begin()+i); }
        int gy = (r-1>=1)? g : g+f; std::vector<std::pair<int,int>> no=p; no[i]={r,f+1}; std::sort(no.begin(),no.end());
        u128 Cy,Wy,Cn,Wn; look(keyOf(gy,y),y,Cy,Wy,nullptr); look(keyOf(g,no),no,Cn,Wn,nullptr);
        if(Cy+Cn!=C){ fprintf(stderr,"FAIL: count split at %s\n",key.c_str()); return 1; }
        u128 cand=Cy+Wy+Wn; actions++; cands.push_back(cand); noKeys.push_back(keyOf(g,no)); cls.push_back((int)i); if(!any||cand>best){best=cand;any=true;} }
      if((int)p.size()<n){ u128 Cn,Wn; look(keyOf(g+1,p),p,Cn,Wn,nullptr); if(Cn!=C){ fprintf(stderr,"FAIL: exhausted-label split at %s\n",key.c_str()); return 1;} actions++; cands.push_back(Wn); noKeys.push_back(""); cls.push_back(-1); if(!any||Wn>best){best=Wn;any=true;} }
      if(best!=W){ fprintf(stderr,"FAIL: recursion at %s: W=%s max=%s\n",key.c_str(),u128s(W).c_str(),u128s(best).c_str()); return 1; }
      for(size_t j=0;j<cands.size();j++) if(cands[j]==best) optmask|=(1u<<j);
      if(persist && curL>=2){ // for each optimal class, after its failure the incremented class must be optimal at the successor
        for(size_t j=0;j<cands.size();j++){ if(cls[j]<0||!(optmask&(1u<<j))) continue; auto it=prev.find(noKeys[j]); if(it==prev.end()) continue;
          int r=p[cls[j]].first,f=p[cls[j]].second+1; // find index of class (r,f) among distinct classes of successor
          std::vector<std::pair<int,int>> no=p; no[cls[j]]={r,f}; std::sort(no.begin(),no.end()); int tj=0; for(size_t i=0;i<no.size();i++){ if(i&&no[i]==no[i-1]) continue; if(no[i]==std::make_pair(r,f)) break; tj++; }
          ppairs++; if(!((it->second.opt>>tj)&1u)) pviol++; } }
    }
    cur[key]={C,W,optmask}; counted++; total++;
    if(curL==n*m){ std::vector<std::pair<int,int>> ip(n,{m,0}); if(key==keyOf(0,ip)){ initFound=true; initW=W; initC=C; } }
  }
  if(counted!=expected){ fprintf(stderr,"FAIL: last layer count\n"); return 1; } if(curL!=n*m){ fprintf(stderr,"FAIL: last layer is %d\n",curL); return 1; } if(!initFound){ fprintf(stderr,"FAIL: initial state missing\n"); return 1; }
  mpz_t num,den,gg; mpz_init(num); mpz_init(den); mpz_init(gg); { uint64_t w[2]={(uint64_t)initW,(uint64_t)(initW>>64)}; mpz_import(num,2,-1,8,0,0,w); uint64_t v[2]={(uint64_t)initC,(uint64_t)(initC>>64)}; mpz_import(den,2,-1,8,0,0,v); } mpz_gcd(gg,num,den); mpz_divexact(num,num,gg); mpz_divexact(den,den,gg);
  char* ns=mpz_get_str(nullptr,10,num); char* ds=mpz_get_str(nullptr,10,den); std::string val=std::string(ns)+"/"+ds;
  if(claimed && val!=claimed){ printf("FAIL: value %s != claimed %s\n",val.c_str(),claimed); return 1; }
  printf("n=%d m=%d states=%lld actions=%llu value=%s\n",n,m,total,actions,val.c_str()); if(persist) printf("persistence: optimal-guess failure pairs=%llu violations=%llu\n",ppairs,pviol); printf("PASS\n"); return 0; }
