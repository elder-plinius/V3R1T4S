#include "heap_guard.hpp"
#include <algorithm>
#include <array>
#include <chrono>
#include <climits>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using U=uint64_t;
U plus_checked(U a,U b){if(UINT64_MAX-a<b)throw runtime_error("sum overflow");return a+b;}
U times_checked(U a,U b){if(b&&a>UINT64_MAX/b)throw runtime_error("product overflow");return a*b;}
struct Row{array<int,3> t;int co;};
vector<Row> readrows(string path,int&n){ifstream f(path);if(!f)throw runtime_error("assignment missing");vector<Row> r;string line;int mx=0;while(getline(f,line)){if(line.empty()||line[0]=='#')continue;istringstream z(line);int a,b,c;string co,extra;if(!(z>>a>>b>>c>>co)||(z>>extra)||!(1<=a&&a<b&&b<c&&c<=25)||co.size()!=3||co[1]!='N'||co[0]<'1'||co[0]>'3'||co[2]<'1'||co[2]>'3')throw runtime_error("bad row");r.push_back({{a-1,b-1,c-1},(co[0]-'1')*3+co[2]-'1'});mx=max(mx,c);}n=mx;size_t idx=0;for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++){if(idx>=r.size()||r[idx].t!=array<int,3>{a,b,c})throw runtime_error("triples missing/duplicate/out of order");idx++;}if(idx!=r.size()||n<3)throw runtime_error("wrong row count");return r;}
struct Gate{uint32_t in,out;int lit;};
struct Edge{int to;vector<int> lits;};
struct Node{uint32_t mask;vector<Edge> edges;};
struct DAG{
 int n;uint32_t full;vector<Row> rows;vector<int> alts,varrow;vector<vector<Gate>> fixed,optional;vector<Node> nodes;unordered_map<uint32_t,int> ids;vector<int> order;int nv;
 DAG(int N,vector<Row>r,vector<int>a,vector<int> vr):n(N),full((1u<<N)-1),rows(move(r)),alts(move(a)),varrow(move(vr)),fixed(N),optional(N){
  nv=varrow.size();vector<int> vi(rows.size(),-1);for(int v=0;v<nv;v++)vi[varrow[v]]=v;
  for(int t=0;t<(int)rows.size();t++){auto rr=rows[t];array<int,3>p={0,1,2};do{bool fo=p[rr.co%3]==rr.co/3,fa=vi[t]<0?fo:p[alts[t]%3]==alts[t]/3;int x=rr.t[p[1]];Gate g{1u<<rr.t[p[0]],1u<<rr.t[p[2]],-1};if(fo&&fa)fixed[x].push_back(g);else if(vi[t]>=0&&(fo||fa)){g.lit=vi[t]*2+(fa?1:0);optional[x].push_back(g);}}while(next_permutation(p.begin(),p.end()));}
  build(0);order.resize(nodes.size());iota(order.begin(),order.end(),0);sort(order.begin(),order.end(),[&](int a,int b){return nodes[a].mask<nodes[b].mask;});
 }
 int build(uint32_t s){auto it=ids.find(s);if(it!=ids.end())return it->second;int id=nodes.size();ids[s]=id;nodes.push_back({s,{}});uint32_t rem=full^s;while(rem){int x=__builtin_ctz(rem);rem&=rem-1;bool ok=true;for(auto q:fixed[x])if((s&q.in)&&!(s&q.out)){ok=false;break;}if(!ok)continue;vector<int>lits;for(auto q:optional[x])if((s&q.in)&&!(s&q.out))lits.push_back(q.lit);sort(lits.begin(),lits.end());lits.erase(unique(lits.begin(),lits.end()),lits.end());int to=build(s|1u<<x);nodes[id].edges.push_back({to,move(lits)});}return id;}
 bool active(const Edge&e,const vector<int8_t>&s){for(int l:e.lits)if(s[l/2]==l%2)return false;return true;}
 U calc(const vector<int8_t>&s,vector<array<U,2>>*loss=nullptr){vector<U>b(nodes.size()),f;if(loss){loss->assign(nv,{0,0});f.resize(nodes.size());}for(auto it=order.rbegin();it!=order.rend();it++){int k=*it;if(nodes[k].mask==full){b[k]=1;continue;}for(auto&e:nodes[k].edges)if(active(e,s))b[k]=plus_checked(b[k],b[e.to]);}
  if(loss){f[0]=1;for(int k:order)if(f[k])for(auto&e:nodes[k].edges)if(active(e,s)){f[e.to]=plus_checked(f[e.to],f[k]);if(b[e.to]){U w=times_checked(f[k],b[e.to]);for(int l:e.lits)if(s[l/2]<0)(*loss)[l/2][l%2]=plus_checked((*loss)[l/2][l%2],w);}}for(auto a:*loss)if(a[0]>b[0]||a[1]>b[0])throw runtime_error("loss exceeds bound");}
  return b[0];
 }
 void save(const string&path,vector<int8_t>s){auto candidate=rows;ofstream f(path);for(int v=0;v<nv;v++)if(s[v]==1)candidate[varrow[v]].co=alts[varrow[v]];for(auto r:candidate)f<<r.t[0]+1<<' '<<r.t[1]+1<<' '<<r.t[2]+1<<' '<<r.co/3+1<<'N'<<r.co%3+1<<'\n';}
};
int main(int argc,char**argv){try{
 if(argc<7)throw runtime_error("usage source alts threshold out nodecap mode [resume]");int n;auto rows=readrows(argv[1],n);vector<int>alts(rows.size(),-1);vector<U>val(rows.size());ifstream cf(argv[2]);string line;getline(cf,line);while(getline(cf,line)){replace(line.begin(),line.end(),',',' ');istringstream z(line);int t,a,b,c,old,co;U relax,v,inter;if(!(z>>t>>a>>b>>c>>old>>relax>>co>>v>>inter)||t<0||t>=(int)rows.size()||co<0||co>8)throw runtime_error("bad alternatives");if(alts[t]<0||v>val[t]){alts[t]=co;val[t]=v;}}
 vector<int>none;DAG base(n,rows,alts,none);vector<int8_t>empty;U baseline=base.calc(empty),th=stoull(argv[3]),best=baseline;vector<int>vr;for(int t=0;t<(int)rows.size();t++){if(alts[t]<0)throw runtime_error("missing alternative");if(val[t]>=baseline||baseline-val[t]<=th)vr.push_back(t);}DAG d(n,rows,alts,vr);vector<int8_t>root(d.nv,-1);vector<array<U,2>>loss;U upper=d.calc(root,&loss);cout<<"BASE "<<baseline<<" ROOT "<<upper<<" VARS "<<d.nv<<" STATES "<<d.nodes.size()<<endl;string out=argv[4];U nodecap=stoull(argv[5]);string mode=argv[6];ofstream marg(out+"/root-marginals.csv");marg<<"variable,row,old_loss,alt_loss\n";for(int v=0;v<d.nv;v++)marg<<v<<','<<vr[v]<<','<<loss[v][0]<<','<<loss[v][1]<<'\n';marg.close();
 if(mode=="audit"){U checks=0;for(int v=0;v<d.nv;v++)for(int c=0;c<2;c++){root[v]=c;U actual=d.calc(root);root[v]=-1;if(actual!=upper-loss[v][c])throw runtime_error("marginal mismatch");checks++;}cout<<"AUDIT_PASS exact_marginal_checks "<<checks<<endl;return 0;}
 vector<vector<int8_t>>stack{root};U nodes=0,pruned=0,leaves=0,forced=0,dominated=0;auto start=chrono::steady_clock::now();
 auto checkpoint=[&](){ofstream f(out+"/checkpoint.tmp");f<<"V1 "<<d.nv<<' '<<best<<' '<<nodes<<' '<<pruned<<' '<<leaves<<' '<<forced<<' '<<dominated<<' '<<stack.size()<<'\n';for(auto&s:stack){for(auto c:s)f<<char('0'+c+1);f<<'\n';}f.close();if(rename((out+"/checkpoint.tmp").c_str(),(out+"/checkpoint.txt").c_str()))throw runtime_error("checkpoint rename failed");};
 if(argc>7){ifstream ck(argv[7]);string tag;int nv;size_t size;if(!(ck>>tag>>nv>>best>>nodes>>pruned>>leaves>>forced>>dominated>>size)||tag!="V1"||nv!=d.nv)throw runtime_error("bad resume");stack.clear();while(size--){string s;ck>>s;if(s.size()!=size_t(nv))throw runtime_error("bad resume state");vector<int8_t>v;for(char c:s){if(c<'0'||c>'2')throw runtime_error("bad status");v.push_back(c-'0'-1);}stack.push_back(move(v));}}
 while(!stack.empty()&&nodes<nodecap){auto s=move(stack.back());stack.pop_back();nodes++;bool dead=false;U bound=0;int branch=-1;for(;;){bound=d.calc(s,&loss);if(bound<=best){pruned++;dead=true;break;}U gap=bound-best;bool changed=false;branch=-1;U minbest=0,sumbest=0;for(int v=0;v<d.nv;v++)if(s[v]<0){U a=loss[v][0],b=loss[v][1];if(a>gap&&b>gap){pruned++;dead=true;break;}if(!a||!b){s[v]=a==0?0:1;dominated++;continue;}if(a>gap||b>gap){s[v]=a>gap?1:0;forced++;changed=true;continue;}U mn=min(a,b),sm=plus_checked(a,b);if(branch<0||mn>minbest||(mn==minbest&&sm>sumbest)){branch=v;minbest=mn;sumbest=sm;}}if(dead)break;if(changed)continue;break;}
  if(!dead){if(branch<0){leaves++;if(bound>best){best=bound;d.save(out+"/candidate-"+to_string(nodes)+"-"+to_string(best)+".txt",s);cout<<"CANDIDATE node "<<nodes<<" count "<<best<<endl;}}else{int first=loss[branch][0]<=loss[branch][1]?0:1;auto other=s;other[branch]=1-first;s[branch]=first;stack.push_back(move(other));stack.push_back(move(s));}}
  if(nodes%100==0){checkpoint();cout<<"CHECK nodes "<<nodes<<" pending "<<stack.size()<<" pruned "<<pruned<<" leaves "<<leaves<<" forced "<<forced<<" dominated "<<dominated<<" best "<<best<<" sec "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;}
 }
 checkpoint();cout<<(stack.empty()?"DONE":"CAPPED")<<" nodes "<<nodes<<" pending "<<stack.size()<<" pruned "<<pruned<<" leaves "<<leaves<<" forced "<<forced<<" dominated "<<dominated<<" best "<<best<<endl;
}catch(exception&e){cerr<<"ERROR "<<e.what()<<endl;return 1;}}
