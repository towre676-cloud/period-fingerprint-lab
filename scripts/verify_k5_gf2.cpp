// Independently verify the five-supported-coefficient full-rank bound.
// GF(2) bitset elimination, plus a separate prime-field checker in
// scripts/verify_k5_modp.cpp. A modular dependency is NOT an integer collision.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
int parity(int n,int p){int r=0;while(n){n/=p;r^=n&1;}return r;}
vector<int> primes(int n){vector<uint8_t> b(n+1,1);b[0]=b[1]=0;for(int p=2;p*p<=n;p++)if(b[p])for(int j=p*p;j<=n;j+=p)b[j]=0;vector<int> out;for(int p=2;p<=n;p++)if(b[p])out.push_back(p);return out;}
int main(int argc,char**argv){
 const int M=argc>1?atoi(argv[1]):25627;
 const int K=argc>2?atoi(argv[2]):5;
 if(M<2||M>60000||K<1||K>6){cerr<<"bounds M=2..60000, K=1..6\n";return 2;}
 auto ps=primes(K*M);int P=ps.size(),R=1+K*P,W=(R+63)/64;
 vector<vector<uint64_t>> pivots(R);vector<uint64_t> col(W);
 int rank=0,first=0;
 for(int a=1;a<=M;a++){
  fill(col.begin(),col.end(),0);col[0]=a&1;
  for(int m=1;m<=K;m++)for(int i=0;i<P&&ps[i]<=m*a;i++)
   if(parity(m*a,ps[i])){int j=1+(m-1)*P+i;col[j>>6]|=uint64_t(1)<<(j&63);}
  bool independent=false;
  for(int word=W-1;word>=0;--word){
   while(col[word]){
    int j=word*64+63-__builtin_clzll(col[word]);
    if(pivots[j].empty()){pivots[j].assign(col.begin(),col.begin()+word+1);rank++;independent=true;goto done;}
    for(size_t k=0;k<pivots[j].size();k++)col[k]^=pivots[j][k];
   }
  }
 done:
  if(!independent){first=a;break;}
 }
 cout<<"field=F2 K="<<K<<" bound="<<M<<" rank="<<rank<<" first_modular_dependency="<<first<<"\n";
 if(K==5&&M==25627&&!(rank==25626&&first==25627))return 3;
 return 0;
}
