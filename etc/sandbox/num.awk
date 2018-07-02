# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

@include "lib"

func Num(i,pos,txt) { 
  class(i,"Num") 
  i.lo=INF 
  i.hi=NINF
  i.m2 = i.mu = i.n = 0 
  if (pos) i.pos=pos
  if (txt) i.txt=txt
}
func NumInc(i,x,    d) {
  if (x==SKIP) return
  i.n++
  d     = x - i.mu
  i.mu += d/i.n
  i.m2 += d*(x - i.mu)
  i.sd  = (i.m2/(i.n - 1 + ZIP))^0.5
  if (x > i.hi) x = i.hi
  if (x < i.lo) x = i.lo
}      
func NumDec(i,x,    d) {  
  if (x==SKIP) return
  if (i.n <= 2) return
  i.n--
  d     = x - i.mu
  i.mu -=  d/i.n
  i.m2 -= d*(x- i.mu)
  i.sd  = (i.m2/(i.n - 1 + ZIP))^0.5
}
func Nums_(    n,j,a,fails,sds,mus,hi) {
  hi=split(" 4 10 15 38 54 57 62 83 100 100 174 190 215 225"\
	         " 233 250 260 270 299 300 306 333 350 375 443 475"\
           " 525 583 780 1000",a)
  Num(n)
  o(n)
  for (j=1;j<=hi;j++ ) {
    sds[n.n] = n.sd
    mus[n.n] = n.mu  
    NumInc(n, a[j])  }
  while(j-- > 0) {
    if (j in sds) {
      fails += (abs(n.mu - mus[j]) > 0.0001)  
      fails += (abs(n.sd - sds[j]) > 0.0001) } 
    NumDec(n, a[j]) }
  return fails 
}

BEGIN { if(MAIN == "num") print Nums_() }
