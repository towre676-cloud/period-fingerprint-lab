// Independent exact finite terminal-collision census over integer partitions.
// No dependencies on the Python production search. Signature equality uses
// prime exponents of factorial denominators. Recompile and replay before
// treating any bounded minimality statement as certified.
// g++ -std=c++20 -O3 -Wall -Wextra -o terminal_scan scripts/terminal_collision_scan.cpp
// ./terminal_scan 2 51 2
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Counts {long long partitions=0,wellformed=0,terminal=0,collisions=0,different_dimension=0;};
vector<int> primes,weights,valuations;
vector<vector<int>> contribution;
unordered_map<string,vector<int>> seen;
Counts counts;
int L,K;
string first_witness;

void init_primes(int n) {
  primes.clear();
  for(int p=2;p<=n;p++) {
    bool prime=true;
    for(int d=2;d*d<=p;d++) if(p%d==0){prime=false;break;}
    if(prime) primes.push_back(p);
  }
}
int factorial_valuation(int n,int p) {
  int r=0;
  while(n){n/=p;r+=n;}
  return r;
}
void setup(int total,int prefix) {
 L=total;K=prefix;
 init_primes(K*L);
 int d=static_cast<int>(primes.size())*K;
 contribution.assign(L+1,vector<int>(d,0));
 for(int a=1;a<=L;a++)
   for(int m=1;m<=K;m++)
     for(size_t j=0;j<primes.size();j++)
       contribution[a][(m-1)*primes.size()+j]=factorial_valuation(a*m,primes[j]);
 valuations.assign(d,0);
 weights.clear();seen.clear();counts=Counts{};first_witness.clear();
}
bool wellformed(const vector<int>& w) {
 int n=static_cast<int>(w.size());
 if(n<2)return false;
 vector<int> pref(n+1,0),suf(n+1,0);
 for(int i=0;i<n;i++)pref[i+1]=gcd(pref[i],w[i]);
 for(int i=n-1;i>=0;i--)suf[i]=gcd(suf[i+1],w[i]);
 for(int i=0;i<n;i++)if(gcd(pref[i],suf[i+1])!=1)return false;
 return true;
}
bool terminal(const vector<int>& w) {
 int n=static_cast<int>(w.size());
 if(n<=3)return all_of(w.begin(),w.end(),[](int a){return a==1;});
 // Deliberately no prefilter inequality; test all relevant ages.
 for(int k=2;k<=L-2;k++) {
   int s=0;
   for(int a:w)s+=(k*a)%L;
   if(s%L)return false;
   int age=s/L;
   if(age<2||age>n-2)return false;
 }
 return true;
}
string signature() {
 string out;
 out.resize(valuations.size());
 for(size_t j=0;j<valuations.size();j++) {
   if(valuations[j]<0||valuations[j]>255)throw runtime_error("signature overflow");
   out[j]=static_cast<char>(valuations[j]);
 }
 return out;
}
string render(const vector<int>& w) {
 string result="[";
 for(size_t i=0;i<w.size();i++) {
   if(i)result+=",";
   result+=to_string(w[i]);
 }
 return result+"]";
}
void enumerate(int remaining,int minimum) {
 if(!remaining) {
   counts.partitions++;
   if(!wellformed(weights))return;
   counts.wellformed++;
   if(!terminal(weights))return;
   counts.terminal++;
   string key=signature();
   auto it=seen.find(key);
   if(it!=seen.end()) {
      counts.collisions++;
      if(it->second.size()!=weights.size())counts.different_dimension++;
      if(first_witness.empty())
        first_witness=render(it->second)+" vs "+render(weights);
   } else seen.emplace(move(key),weights);
   return;
 }
 for(int a=minimum;a<=remaining;a++) {
   weights.push_back(a);
   for(size_t j=0;j<valuations.size();j++)valuations[j]+=contribution[a][j];
   enumerate(remaining-a,a);
   for(size_t j=0;j<valuations.size();j++)valuations[j]-=contribution[a][j];
   weights.pop_back();
 }
}
int main(int argc,char**argv) {
 int lo=argc>1?atoi(argv[1]):2;
 int hi=argc>2?atoi(argv[2]):51;
 int prefix=argc>3?atoi(argv[3]):2;
 if(lo<2||hi<lo||hi>65||prefix<1||prefix>3) {
   cerr<<"usage: terminal_scan [min_sum>=2] [max_sum<=65] [prefix 1..3]\n";
   return 2;
 }
 ios::sync_with_stdio(false);
 Counts overall;
 for(int l=lo;l<=hi;l++) {
   setup(l,prefix);
   enumerate(l,1);
   cout<<"L="<<l<<" partitions="<<counts.partitions
       <<" wellformed="<<counts.wellformed<<" terminal="<<counts.terminal
       <<" collisions="<<counts.collisions
       <<" different_dimension="<<counts.different_dimension;
   if(!first_witness.empty())cout<<" witness="<<first_witness;
   cout<<"\n"<<flush;
   overall.partitions+=counts.partitions;
   overall.wellformed+=counts.wellformed;
   overall.terminal+=counts.terminal;
   overall.collisions+=counts.collisions;
   overall.different_dimension+=counts.different_dimension;
 }
 cout<<"TOTAL partitions="<<overall.partitions
     <<" wellformed="<<overall.wellformed
     <<" terminal="<<overall.terminal
     <<" collisions="<<overall.collisions
     <<" different_dimension="<<overall.different_dimension<<"\n";
 if(lo==2&&hi==51&&prefix==2) {
   if(overall.collisions!=77||overall.different_dimension!=77) {
     cerr<<"expected exactly 77 terminal collision pairs through weight 51\n";
     return 3;
   }
 }
 return 0;
}
