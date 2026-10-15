// Written before reading any author executable source.
// CLAIM.md definition: "A matching is a bijection. It is stable exactly when
// no man and woman both strictly prefer each other to their assigned partners."
// For two couples (i,w),(j,v), require w!=v and neither cross pair blocks.
// Removing an unsupported value cannot remove a stable completion. Branching
// on each value of one nonsingleton domain partitions all surviving completions.
// All leaves are independently tested against the quoted definition.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using Mask=uint32_t;
using Domains=std::array<Mask,31>;
struct Checker {
  int n;
  int mr[31][31]{}, wr[31][31]{}, mp[31][31]{};
  Mask supports[31][31][31]{};
  uint64_t count=0,nodes=0,digest=0;
  explicit Checker(const std::string& file) {
    std::ifstream f(file); if(!f) throw std::runtime_error("missing profile");
    std::vector<std::vector<int>> rows; std::string line;
    while(std::getline(f,line)) {
      line=line.substr(0,line.find('#')); std::istringstream in(line);
      std::vector<int> row; std::string token;
      while(in>>token) { size_t end; int x=std::stoi(token,&end);
        if(end!=token.size()) throw std::runtime_error("noninteger token");
        row.push_back(x-1); }
      if(!row.empty()) rows.push_back(row);
    }
    if(rows.empty()) throw std::runtime_error("empty profile");
    n=rows[0].size();
    if(n<1 || n>31 || rows.size()!=size_t(2*n)) throw std::runtime_error("shape");
    for(int i=0;i<2*n;++i) {
      auto sorted=rows[i]; std::sort(sorted.begin(),sorted.end());
      if(sorted.size()!=size_t(n)) throw std::runtime_error("row length");
      for(int k=0;k<n;++k) if(sorted[k]!=k) throw std::runtime_error("not permutation");
      for(int k=0;k<n;++k) {
        if(i<n) {mp[i][k]=rows[i][k]; mr[i][rows[i][k]]=k;}
        else wr[i-n][rows[i][k]]=k;
      }
    }
    for(int i=0;i<n;++i) for(int j=0;j<n;++j) if(i!=j)
      for(int w=0;w<n;++w) for(int v=0;v<n;++v)
        if(w!=v && !(mr[i][v]<mr[i][w] && wr[v][i]<wr[v][j])
                && !(mr[j][w]<mr[j][v] && wr[w][j]<wr[w][i]))
          supports[i][w][j]|=Mask(1)<<v;
  }
  bool propagate(Domains& d,Mask pending) const {
    while(pending) {
      int j=__builtin_ctz(pending); pending&=pending-1;
      for(int i=0;i<n;++i) if(i!=j) {
        Mask keep=0, todo=d[i];
        while(todo) {int w=__builtin_ctz(todo); todo&=todo-1;
          if(supports[i][w][j]&d[j]) keep|=Mask(1)<<w;}
        if(!keep) return false;
        if(keep!=d[i]) {d[i]=keep; pending|=Mask(1)<<i;}
      }
    }
    return true;
  }
  void search(Domains d,Mask pending) {
    if(nodes==UINT64_MAX) throw std::runtime_error("node overflow"); ++nodes;
    if(!propagate(d,pending)) return;
    int chosen=-1, smallest=32;
    for(int i=0;i<n;++i) {int c=__builtin_popcount(d[i]);
      if(c>1 && c<smallest) {smallest=c; chosen=i;}}
    if(chosen>=0) {
      Mask todo=d[chosen];
      while(todo) {Mask bit=todo&(-todo); todo-=bit;
        Domains child=d; child[chosen]=bit; search(child,Mask(1)<<chosen);}
      return;
    }
    int partner[31], husband[31]; std::fill(husband,husband+n,-1);
    for(int i=0;i<n;++i) {partner[i]=__builtin_ctz(d[i]);
      if(husband[partner[i]]!=-1) throw std::runtime_error("nonbijective leaf");
      husband[partner[i]]=i;}
    for(int i=0;i<n;++i) for(int k=0;k<mr[i][partner[i]];++k) {
      int w=mp[i][k]; if(wr[w][i]<wr[w][husband[w]])
        throw std::runtime_error("blocking leaf"); }
    if(count==UINT64_MAX) throw std::runtime_error("count overflow"); ++count;
    uint64_t h=1469598103934665603ULL;
    for(int i=0;i<n;++i) {h^=uint64_t(partner[i]+1); h*=1099511628211ULL;}
    digest+=h; // Deliberate modular checksum, not used to establish count.
  }
  void run() {Domains d{}; Mask all=(Mask(1)<<n)-1;
    for(int i=0;i<n;++i)d[i]=all; search(d,all);}
};
int main(int argc,char**argv) {
  try {if(argc<2) throw std::runtime_error("profile arguments required");
    for(int i=1;i<argc;++i) {Checker c(argv[i]);c.run();
      std::cout<<"{\"file\":\""<<argv[i]<<"\",\"n\":"<<c.n
        <<",\"count\":"<<c.count<<",\"nodes\":"<<c.nodes
        <<",\"digest\":"<<c.digest<<"}"<<std::endl;}
  } catch(const std::exception& e) {std::cerr<<e.what()<<std::endl;return 1;}
}
