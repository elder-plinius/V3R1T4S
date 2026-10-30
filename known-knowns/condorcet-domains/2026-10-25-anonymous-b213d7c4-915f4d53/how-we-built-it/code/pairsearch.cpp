#define main structural_main
#include "structural.cpp"
#undef main
struct Solver{
 int n,v;string dir;vector<C>cs,vars;U best;uint64_t nodes=0,evals=0,leaves=0,pruned=0,dominated=0;double budget;chrono::steady_clock::time_point start;bool capped=false;
 U score(){evals++;return count(n,cs).value;}
 bool timeup(){return chrono::duration<double>(chrono::steady_clock::now()-start).count()>budget;}
 void checkpoint(){ofstream f(dir+"/checkpoint.json");f<<"{\"n\":"<<n<<",\"clone\":"<<v<<",\"best\":\""<<dec(best)<<"\",\"nodes\":"<<nodes<<",\"evaluations\":"<<evals<<",\"leaves\":"<<leaves<<",\"pruned\":"<<pruned<<",\"dominated\":"<<dominated<<",\"capped\":"<<(capped?"true":"false")<<"}";}
 void dfs(int depth,U upper){if(capped)return;if(timeup()){capped=true;checkpoint();return;}nodes++;if(nodes%1000==0){checkpoint();cout<<"progress,"<<nodes<<','<<evals<<','<<depth<<','<<dec(best)<<endl;}if(upper<=best){pruned++;return;}if(depth==(int)vars.size()){leaves++;best=upper;save(cs,dir+"/best.txt");checkpoint();cout<<"BEST,"<<dec(best)<<','<<nodes<<','<<evals<<endl;return;}
 C c=vars[depth];U children[9];for(int m=0;m<9;m++){c.i=m/3;c.j=m%3;cs.push_back(c);children[m]=score();cs.pop_back();if(timeup()){capped=true;return;}}
 // Zero-loss condition dominates every alternative choice.
 for(int m=0;m<9;m++)if(children[m]==upper){c.i=m/3;c.j=m%3;cs.push_back(c);dominated+=8;dfs(depth+1,upper);cs.pop_back();return;}
 // Recover all six triple-order weights by inclusion-exclusion of two never rules.
 U weights[6];int positions[6][3],p[3]={0,1,2};int h=0;uint32_t support=0;
 do{for(int k=0;k<3;k++)positions[h][p[k]]=k;C x=c,y=c;x.i=0;x.j=positions[h][0];y.i=1;y.j=positions[h][1];cs.push_back(x);cs.push_back(y);U joint=score();cs.pop_back();cs.pop_back();if(upper+joint<children[x.j]+children[3+y.j])throw runtime_error("inclusion exclusion underflow");weights[h]=upper+joint-children[x.j]-children[3+y.j];if(weights[h])support|=1u<<h;h++;}while(next_permutation(p,p+3));
 U total=0;for(auto w:weights)total+=w;if(total!=upper)throw runtime_error("spectrum sum mismatch");uint32_t masks[9];for(int m=0;m<9;m++){masks[m]=0;U sum=0;for(int k=0;k<6;k++)if(positions[k][m/3]!=m%3){masks[m]|=1u<<k;sum+=weights[k];}masks[m]&=support;if(sum!=children[m])throw runtime_error("spectrum child mismatch");}
 vector<int> choices;for(int m=0;m<9;m++){if(children[m]<=best){pruned++;continue;}bool dom=false;for(int k=0;k<9;k++)if(k!=m && (masks[m]&~masks[k])==0 && (masks[m]!=masks[k]||k<m)){dom=true;break;}if(dom){dominated++;continue;}choices.push_back(m);}sort(choices.begin(),choices.end(),[&](int a,int b){return children[a]>children[b];});for(int m:choices){if(children[m]<=best){pruned++;continue;}c.i=m/3;c.j=m%3;cs.push_back(c);dfs(depth+1,children[m]);cs.pop_back();if(capped)return;}
 }
};
#ifndef PAIR_LIBRARY
int main(int argc,char**argv){try{int base_n=stoi(argv[1]),v=stoi(argv[3]);auto base=readfile(argv[2],base_n);Solver s;s.n=base_n+1;s.v=v;s.dir=argv[4];s.budget=stod(argv[5]);s.best=stoull(argv[6]);s.start=chrono::steady_clock::now();auto full=clone(base,base_n,v,0);for(auto c:full)if(c.c==base_n&&(c.a==v||c.b==v))s.vars.push_back(c);else s.cs.push_back(c);
 // Rank variables by lowest best one-condition upper bound, then lexicographic; immutable deterministic order.
 vector<pair<U,C>>ranked;for(C c:s.vars){U largest=0;for(int m=0;m<9;m++){c.i=m/3;c.j=m%3;s.cs.push_back(c);largest=max(largest,s.score());s.cs.pop_back();}ranked.push_back({largest,c});}stable_sort(ranked.begin(),ranked.end(),[](auto a,auto b){return a.first<b.first;});s.vars.clear();for(auto [bound,c]:ranked){s.vars.push_back(c);cout<<"variable,"<<c.a<<','<<c.b<<','<<c.c<<','<<dec(bound)<<endl;}U root=s.score();cout<<"ROOT,"<<dec(root)<<endl;s.dfs(0,root);s.checkpoint();cout<<"DONE,"<<(s.capped?"CAPPED":"COMPLETE")<<','<<dec(s.best)<<','<<s.nodes<<','<<s.evals<<','<<s.leaves<<','<<s.pruned<<','<<s.dominated<<endl;return 0;}catch(exception&e){cerr<<e.what()<<endl;return 2;}}

#endif
