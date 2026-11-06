// Prime-field independent factorial-valuation rank checker for K=5.
// Full rank over F_65521 is a rigorous lower bound on rational rank.
// Characteristic-p dependence is NOT an integer factorial identity.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
static constexpr uint64_t MOD=65521;
uint64_t inverse(uint64_t x){uint64_t z=1,e=MOD-2;while(e){if(e&1)z=z*x%MOD;x=x*x%MOD;e>>=1;}return z;}
int val(int n,int p){int r=0;while(n){n/=p;r+=n;}return r;}
vector<int> primes(int n){vector<uint8_t>b(n+1,1);b[0]=b[1]=0;for(int p=2;p*p<=n;p++)if(b[p])for(int j=p*p;j<=n;j+=p)b[j]=0;vector<int>v;for(int p=2;p<=n;p++)if(b[p])v.push_back(p);return v;}
int main(int argc,char**argv){
 const int M=argc>1?atoi(argv[1]):25809;
 const int K=argc>2?atoi(argv[2]):5;
 if(M<2||M>26000||K<1||K>6){cerr<<"bounds M=2..26000 K=1..6\n";return 2;}
 auto ps=primes(K*M);int P=ps.size(),rows=1+K*P;
 vector<vector<uint16_t>>pivot(rows);vector<uint16_t>w(rows);
 int rank=0,first=0;
 for(int a=1;a<=M;a++){
  fill(w.begin(),w.end(),0);w[0]=a%MOD;
  for(int m=1;m<=K;m++)for(int i=0;i<P&&ps[i]<=m*a;i++)w[1+(m-1)*P+i]=val(m*a,ps[i])%MOD;
  bool independent=false;
  for(int j=rows-1;j>=0;j--){uint64_t c=w[j];if(!c)continue;
   if(pivot[j].empty()){uint64_t q=inverse(c);for(int k=0;k<=j;k++)w[k]=uint64_t(w[k])*q%MOD;pivot[j].assign(w.begin(),w.begin()+j+1);rank++;independent=true;break;}
   auto&b=pivot[j];for(int k=0;k<j;k++)w[k]=(w[k]+MOD-c*b[k]%MOD)%MOD;w[j]=0;
  }
  if(!independent&&first==0)first=a;
 }
 cout<<"field=F65521 K="<<K<<" bound="<<M<<" rank="<<rank<<" first_modular_dependency="<<first<<"\n";
 if(K==5&&M==25809&&!(rank==25808&&first==25809))return 3;
 return 0;
}
