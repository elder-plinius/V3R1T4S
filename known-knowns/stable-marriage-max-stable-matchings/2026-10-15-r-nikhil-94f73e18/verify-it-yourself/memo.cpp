// Exact state merging extension of the pre-author-code checker.
// After arc consistency, every remaining value is compatible with each fixed
// variable. Removing fixed variables is therefore a bijection on completions.
// Equal remaining domain vectors describe identical residual binary CSPs.
// Memoization merges equal subproblems, never samples or truncates branches.
#define main independent_original_main
#include "independent.cpp"
#undef main
#include "unordered_map"
struct Hash {size_t operator()(const Domains& d) const {size_t h=0;
  for(Mask v:d) h=(h^v)*1099511628211ULL;return h;}};
struct MemoChecker:Checker {
  std::unordered_map<Domains,uint64_t,Hash> memo;
  uint64_t hits=0;
  explicit MemoChecker(const std::string& file):Checker(file) {}
  bool reduce(Domains& d,Mask pending) {
    while(pending) {int j=__builtin_ctz(pending);pending&=pending-1;
      for(int i=0;i<n;++i) if(i!=j && d[i]) {Mask keep=0,t=d[i];
        while(t) {int w=__builtin_ctz(t);t&=t-1;
          if(supports[i][w][j]&d[j]) keep|=Mask(1)<<w;}
        if(!keep)return false;
        if(keep!=d[i]) {d[i]=keep;pending|=Mask(1)<<i;}
      }
    }
    for(int i=0;i<n;++i) if(d[i] && !(d[i]&(d[i]-1)))d[i]=0;
    return true;
  }
  uint64_t solve(Domains d,Mask pending) {
    ++nodes;if(!reduce(d,pending))return 0;
    int chosen=-1,smallest=32;
    for(int i=0;i<n;++i) {int c=__builtin_popcount(d[i]);
      if(c && c<smallest) {smallest=c;chosen=i;}}
    if(chosen<0)return 1;
    auto it=memo.find(d);if(it!=memo.end()) {++hits;return it->second;}
    uint64_t total=0;Mask t=d[chosen];
    while(t) {Mask bit=t&(-t);t-=bit;Domains child=d;child[chosen]=bit;
      uint64_t v=solve(child,Mask(1)<<chosen);
      if(total>UINT64_MAX-v)throw std::runtime_error("overflow");total+=v;}
    // Deterministic eviction only changes work, never the exact recurrence.
    if(memo.size()>=1000000)memo.clear();
    memo.emplace(d,total);return total;
  }
  void run() {Domains d{};Mask all=(Mask(1)<<n)-1;
    for(int i=0;i<n;++i)d[i]=all;count=solve(d,all);}
};
int main(int argc,char**argv) {try {
  if(argc<2)throw std::runtime_error("profile arguments required");
  for(int i=1;i<argc;++i) {MemoChecker c(argv[i]);c.run();
    std::cout<<"{\"file\":\""<<argv[i]<<"\",\"n\":"<<c.n
      <<",\"count\":"<<c.count<<",\"nodes\":"<<c.nodes
      <<",\"memo_hits\":"<<c.hits<<"}"<<std::endl;}
  }catch(const std::exception&e){std::cerr<<e.what()<<std::endl;return 1;}}
