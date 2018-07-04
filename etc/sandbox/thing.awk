# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "lib"

#----------------------------------
function Thing(i,pos,txt) {
  class(i,"Thing")
  i.pos=pos
  i.txt=txt
  i.n = 0
  i.w = 1
}
function ThingPrep(i,x) { 
  return x 
}
function ThingInc(i,x) {
  if ( x==SKIP) return x
  x = @Prep(i,x)
  i.n++
  @Inc1(i,x)
  return x
}
function ThingDec(i,x) {
  if ( x==SKIP) return x
  if ( i.n < 3) return x
  x = @Prep(i,x)
  i.n--
  @Dec1(i,x) 
  return x 
}
#----------------------------------
function Sym(i,pos,txt) {
  claSS(i,"Sym","Thing",pos,txt)
  holds(i,"counts")
  i.mode = ""
  i.most = 0
  i._ent =""
  i.n = 0
}
function SymInc1(i,x,   tmp) {
  i._ent = ""
  tmp = i.counts[x] = i.counts[x] + 1 
  if(tmp > i.mode) {
    i.most = tmp
    i.mode = x }
}
function SymDec1(i,x,   tmp) {
  i._ent = ""
  i.counts[x]--
  return x
}  
function SymEnt(i,   x,p) {
  if(!i._ent)
    for(x in i.counts) {
      p = i.counts[x]/i.n
      i._ent -= p * log(p) / log(2) }
  return i._ent 
}
#----------------------------------
function Num(i,pos,txt) { 
  claSS(i,"Num","Thing",pos,txt) 
  i.lo=INF 
  i.hi=NINF
  i.m2 = i.mu = i.n = 0 
  if (pos) i.pos=pos
  if (txt) i.txt=txt
}
function NumPrep(i,x) { return x+0 }

function NumInc1(i,x,    d) {
  d     = x - i.mu
  i.mu += d/i.n
  i.m2 += d*(x - i.mu)
  i.sd  = (i.m2/(i.n - 1 + ZIP))^0.5
  if (x > i.hi) x = i.hi
  if (x < i.lo) x = i.lo
}      
function NumDec1(i,x,    d) {  
  i.n--
  d     = x - i.mu
  i.mu -=  d/i.n
  i.m2 -= d*(x- i.mu)
  i.sd  = (i.m2/(i.n - 1 + ZIP))^0.5
}
#----------------------------------
function ThingSlow_(t) {
  Num(n)
  Sym(s)
  for(j=1;j<=10^4;j++) {
	  @Inc(n,j)
          @Inc(s,"e")
  }
  print n.n, n.mu,n.sd,s.n
}
function ThingFast_(t) {
  Num(n)
  Sym(s)
  for(j=1;j<=10^4;j++) {
	  NumInc(n,j)
          SymInc(s,"e")
  }
  print n.n,n.mu, n.sd,s.n
}
function Nums_(    n,j,a,fails,sds,mus,hi) {
  hi=split(" 4 10 15 38 54 57 62 83 100 100 174 190 215 225"\
	   " 233 250 260 270 299 300 306 333 350 375 443 475"\
           " 525 583 780 1000",a)
  Num(n)
  o(n)
  for (j=1;j<=hi;j++ ) {
    sds[n.n] = n.sd
    mus[n.n] = n.mu  
    @Inc(n, a[j])  } 
  while(j-- > 0) {
    if (j in sds) {
      fails += (abs(n.mu - mus[j]) > 0.0001)  
      fails += (abs(n.sd - sds[j]) > 0.0001) } 
    @Dec(n, a[j]) }
  return fails 
}

BEGIN { if(MAIN == "thing") print Nums_() }
