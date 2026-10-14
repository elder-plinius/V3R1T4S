// Blocker-guided exact neighborhood exchanges with bounded neutral transport.
// The independent acceptance checker is check_code.py, not this search engine.
#define main standalone_scan_main
#include "scan.cpp"
#undef main
#include <array>
#include <bitset>
#include <random>
#include <sstream>
#include <unordered_map>
struct Candidate {U word;vector<int>b;};
struct Pool {vector<Candidate>p; vector<vector<int>> inv; vector<long long>hist;long long visited=0;};
Pool census(const vector<U>&code,int n,int w,int t,int cap){
 auto sub=combinations(w,t);vector<int>owner(C[n][t],-1),support(w),seen(code.size());
 for(int i=0;i<(int)code.size();i++){U x=code[i];int j=0;while(x){support[j++]=__builtin_ctzll(x);x&=x-1;}for(auto&z:sub){int r=0;for(int k=0;k<t;k++)r+=C[support[z[k]]][k+1];if(owner[r]>=0)throw runtime_error("invalid incumbent");owner[r]=i;}}
 unordered_set<U>in(code.begin(),code.end());Pool out;out.inv.resize(code.size());out.hist.resize(cap+2);int stamp=0;vector<int>b;
 for(U x=(1ULL<<w)-1;x<(1ULL<<n);){out.visited++;if(!in.count(x)){
  ++stamp;U y=x;int j=0;while(y){support[j++]=__builtin_ctzll(y);y&=y-1;}b.clear();
  for(auto&z:sub){int r=0;if(t==4)r=C[support[z[0]]][1]+C[support[z[1]]][2]+C[support[z[2]]][3]+C[support[z[3]]][4];else for(int k=0;k<t;k++)r+=C[support[z[k]]][k+1];int a=owner[r];if(a>=0&&seen[a]!=stamp){seen[a]=stamp;b.push_back(a);if((int)b.size()>cap)break;}}
  out.hist[min((int)b.size(),cap+1)]++;if((int)b.size()<=cap){sort(b.begin(),b.end());int k=out.p.size();out.p.push_back({x,b});for(int a:b)out.inv[a].push_back(k);}
 }U low=x&-x,up=x+low;x=up+(((up^x)/low)>>2);}
 return out;
}
struct Clique {
 vector<U>ws;vector<vector<unsigned char>>adj;vector<int>answer,stack;int target;long long nodes=0,limit=150000;
 bool expand(vector<int>p){
  if(++nodes>limit)return false;
  if((int)stack.size()+(int)p.size()<target)return false;
  if((int)stack.size()>=target){answer=stack;return true;}
  vector<int>order,bounds,remain=p;int color=0;
  while(!remain.empty()){color++;vector<int>cls,next;for(int v:remain){bool ok=true;for(int u:cls)if(adj[u][v]){ok=false;break;}if(ok){cls.push_back(v);order.push_back(v);bounds.push_back(color);}else next.push_back(v);}remain.swap(next);}
  for(int i=(int)order.size()-1;i>=0;i--){
   if((int)stack.size()+bounds[i]<target)return false;
   int v=order[i];stack.push_back(v);
   if((int)stack.size()>=target){answer=stack;return true;}
   vector<int>q;for(int j=0;j<i;j++)if(adj[v][order[j]])q.push_back(order[j]);
   if(!q.empty()&&expand(q))return true;
   stack.pop_back();if(nodes>limit)return false;
  }return false;
 }
 bool solve(const vector<U>&w,int t,int goal,int force=-1){ws=w;target=goal;nodes=0;answer.clear();stack.clear();int s=w.size();adj.assign(s,vector<unsigned char>(s));for(int i=0;i<s;i++)for(int j=0;j<i;j++)adj[i][j]=adj[j][i]=(__builtin_popcountll(w[i]&w[j])<t);vector<int>p;
  if(force>=0){stack.push_back(force);for(int i=0;i<s;i++)if(adj[force][i])p.push_back(i);}else{p.resize(s);iota(p.begin(),p.end(),0);}
  return expand(p);
 }
};
void save_code(vector<U> c,int n,const string&p){sort(c.begin(),c.end());ofstream f(p);if(!f)throw runtime_error("cannot save code");for(U x:c){for(int i=n-1;i>=0;i--)f<<((x>>i)&1);f<<'\n';}}
struct SetHash{size_t operator()(const vector<int>&v)const{size_t h=0;for(int x:v)h=(h*1000003)^size_t(x+1);return h;}};
int main(int argc,char**argv){try{
 if(argc!=11)throw runtime_error("usage: engine seed n w t cap maxremove rng rounds seconds prefix");
 string path=argv[1],prefix=argv[10];int n=stoi(argv[2]),w=stoi(argv[3]),t=stoi(argv[4]),cap=stoi(argv[5]),maxr=stoi(argv[6]),seed=stoi(argv[7]),rounds=stoi(argv[8]);double budget=stod(argv[9]);
 if(n>=63||w>=16||n<w||t>w||cap<1||maxr<1)throw runtime_error("unsupported parameters");choose_init();vector<U>code=read_code(path,n,w);const int initial=code.size();mt19937 rng(seed);auto start=chrono::steady_clock::now();auto elapsed=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};ofstream logs(prefix+".jsonl");long long totaltrials=0,totalnodes=0;int neutral_total=0;
 for(int round=0;round<rounds&&elapsed()<budget;round++){
  Pool pool=census(code,n,w,t,cap);logs<<"{\"event\":\"census\",\"round\":"<<round<<",\"size\":"<<code.size()<<",\"pool\":"<<pool.p.size()<<",\"hist\":[";for(int k=0;k<(int)pool.hist.size();k++){if(k)logs<<',';logs<<pool.hist[k];}logs<<"],\"seconds\":"<<elapsed()<<"}\n";logs.flush();
  cout<<"round="<<round<<" pool="<<pool.p.size()<<" size="<<code.size()<<" secs="<<elapsed()<<endl;
  for(auto&c:pool.p)if(c.b.empty()){code.push_back(c.word);save_code(code,n,prefix+"_candidate.txt");logs<<"{\"event\":\"gain\",\"kind\":\"direct\",\"size\":"<<code.size()<<"}\n";return 0;}
  vector<vector<int>>removal;unordered_set<vector<int>,SetHash>dedup;
  auto addR=[&](vector<int>r){sort(r.begin(),r.end());r.erase(unique(r.begin(),r.end()),r.end());if(!r.empty()&&(int)r.size()<=maxr&&dedup.insert(r).second)removal.push_back(r);};
  for(auto&c:pool.p)if((int)c.b.size()<=min(cap,4))addR(c.b);
  shuffle(removal.begin(),removal.end(),rng);
  // Shared-blocker unions and short random hypergraph walks, not random removal.
  for(int k=0;k<45000&&!pool.p.empty();k++){
   int ci=rng()%pool.p.size();auto r=pool.p[ci].b;int steps=1+(rng()%3);
   for(int j=0;j<steps&&!r.empty();j++){int pivot=r[rng()%r.size()];auto&list=pool.inv[pivot];int other=list[rng()%list.size()];if(__builtin_popcountll(pool.p[ci].word&pool.p[other].word)>=t)continue;vector<int>z=r;z.insert(z.end(),pool.p[other].b.begin(),pool.p[other].b.end());sort(z.begin(),z.end());z.erase(unique(z.begin(),z.end()),z.end());if((int)z.size()<=maxr)r=z;}
   addR(r);
  }
  vector<int>mark(code.size(),0),seen(pool.p.size(),0);int stamp=0;vector<int>neutralR;vector<U>neutralW;int neutral_options=0;long long trials=0,nodec=0,capped=0;
  for(auto&r:removal){if(elapsed()>=budget)break;++stamp;for(int v:r)mark[v]=stamp;vector<U>local;for(int v:r)local.push_back(code[v]);
   for(int v:r)for(int k:pool.inv[v])if(seen[k]!=stamp){seen[k]=stamp;bool ok=true;for(int a:pool.p[k].b)if(mark[a]!=stamp){ok=false;break;}if(ok)local.push_back(pool.p[k].word);}
   if(local.size()<=r.size()||local.size()>160)continue;
   Clique solver;trials++;bool gain=solver.solve(local,t,r.size()+1);nodec+=solver.nodes;if(solver.nodes>solver.limit)capped++;
   if(gain){vector<U>updated;for(int i=0;i<(int)code.size();i++)if(mark[i]!=stamp)updated.push_back(code[i]);for(int k:solver.answer)updated.push_back(local[k]);
    save_code(updated,n,prefix+"_candidate.txt");ofstream ex(prefix+"_exchange.json");ex<<"{\"round\":"<<round<<",\"removed\":[";for(int j=0;j<(int)r.size();j++){if(j)ex<<',';ex<<code[r[j]];}ex<<"],\"inserted\":[";for(int j=0;j<(int)solver.answer.size();j++){if(j)ex<<',';ex<<local[solver.answer[j]];}ex<<"],\"size\":"<<updated.size()<<"}\n";
    logs<<"{\"event\":\"gain\",\"round\":"<<round<<",\"size\":"<<updated.size()<<",\"trials\":"<<totaltrials+trials<<",\"nodes\":"<<totalnodes+nodec<<",\"seconds\":"<<elapsed()<<"}\n";cout<<"GAIN "<<initial<<" -> "<<updated.size()<<" at "<<elapsed()<<" seconds"<<endl;return 0;
   }
   if(rounds>1&&neutral_options<25&&r.size()<=8&&local.size()>r.size()+1){int force=r.size()+rng()%(local.size()-r.size());if(solver.solve(local,t,r.size(),force)){neutral_options++;if(neutralR.empty()||rng()%neutral_options==0){neutralR=r;neutralW.clear();for(int k:solver.answer)neutralW.push_back(local[k]);}}}
  }
  totaltrials+=trials;totalnodes+=nodec;
  logs<<"{\"event\":\"neighborhood_end\",\"round\":"<<round<<",\"removal_sets_generated\":"<<removal.size()<<",\"trials\":"<<trials<<",\"clique_nodes\":"<<nodec<<",\"node_capped\":"<<capped<<",\"seconds\":"<<elapsed()<<"}\n";logs.flush();
  if(rounds==1||elapsed()>=budget)break;
  int transported=0;
  if(!neutralR.empty()){
   unordered_set<int>drop(neutralR.begin(),neutralR.end());vector<U>next;for(int i=0;i<(int)code.size();i++)if(!drop.count(i))next.push_back(code[i]);next.insert(next.end(),neutralW.begin(),neutralW.end());code=next;transported++;
  }
  // Valid sequential single-word plateau exchanges. Check against CURRENT code.
  vector<int>order(pool.p.size());iota(order.begin(),order.end(),0);shuffle(order.begin(),order.end(),rng);
  for(int k:order){if(pool.p[k].b.size()>2)continue;U x=pool.p[k].word;int one=-1,count=0;bool duplicate=false;for(int i=0;i<(int)code.size();i++){if(x==code[i]){duplicate=true;break;}if(__builtin_popcountll(x&code[i])>=t){one=i;if(++count>1)break;}}
   if(!duplicate&&count==1){code[one]=x;transported++;if(transported>=30)break;}
  }
  neutral_total+=transported;save_code(code,n,prefix+"_checkpoint_"+to_string(round)+".txt");logs<<"{\"event\":\"neutral_transport\",\"round\":"<<round<<",\"moves\":"<<transported<<",\"seconds\":"<<elapsed()<<"}\n";logs.flush();
  if(!transported){cout<<"No neutral transport available in this pool"<<endl;break;}
 }
 save_code(code,n,prefix+"_incumbent.txt");logs<<"{\"event\":\"end\",\"size\":"<<code.size()<<",\"trials\":"<<totaltrials<<",\"clique_nodes\":"<<totalnodes<<",\"neutral_moves\":"<<neutral_total<<",\"seconds\":"<<elapsed()<<"}\n";
 cout<<"NO_GAIN size="<<code.size()<<" trials="<<totaltrials<<" secs="<<elapsed()<<endl;return 2;
 }catch(exception&e){cerr<<e.what()<<endl;return 1;}}
