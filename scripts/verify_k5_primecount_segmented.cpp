// Independent SEGMENTED prime sieve for exact K=5 row-count certificate.
// Unlike the Python dual full/odd sieves, this never stores flags for
// the whole 14,335,000 range. No prime-counting theorem is assumed.
// g++ -O3 -std=c++20 -Wall -Wextra -o /tmp/k5_primes scripts/verify_k5_primecount_segmented.cpp
// /tmp/k5_primes
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
int main(){
 constexpr int M=2867000;
 constexpr int K=5, MAX=K*M, SEGMENT=65536;
 constexpr array<int,K> expected={207927,395799,577502,755330,930416};
 int root=static_cast<int>(sqrt(MAX));
 vector<bool> small(root+1,true);
 small[0]=false;small[1]=false;
 for(int p=2;p*p<=root;p++)
   if(small[p])
     for(int k=p*p;k<=root;k+=p)
       small[k]=false;
 vector<int> base;
 for(int p=2;p<=root;p++)if(small[p])base.push_back(p);
 long long total=0;
 array<int,K> counts{};
 int next=0;
 for(int lo=0;lo<=MAX;lo+=SEGMENT){
   int hi=min(MAX,lo+SEGMENT-1);
   vector<uint8_t> prime(hi-lo+1,1);
   if(lo==0) {prime[0]=0;if(hi>=1)prime[1]=0;}
   if(lo==1)prime[0]=0;
   for(int p:base){
     if(1LL*p*p>hi)break;
     int first=max(p*p,((lo+p-1)/p)*p);
     for(int x=first;x<=hi;x+=p)
       prime[x-lo]=0;
   }
   for(int x=lo;x<=hi;x++){
     if(prime[x-lo])total++;
     if(next<K&&x==(next+1)*M)counts[next++]=total;
   }
 }
 if(next!=K||counts!=expected){
   cerr<<"Prime census mismatch or missing endpoint\n";
   for(int x:counts)cerr<<x<<" ";
   cerr<<"\n";
   return 2;
 }
 const long long valuation_rows=accumulate(counts.begin(),counts.end(),0LL);
 const long long rows=valuation_rows+1;
 if(rows!=2866975||rows>=M||rows+1>=M)return 3;
 cout<<"SEGMENTED_SIEVE_PASS K=5 M="<<M<<" pi=";
 for(int i=0;i<K;i++)cout<<(i?",":"")<<counts[i];
 cout<<" rows="<<rows<<" nullity_at_least="<<(M-rows)
     <<" same_dimension_nullity_at_least="<<(M-rows-1)<<"\n";
 return 0;
}
