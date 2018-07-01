@include "lib.awk"

function num(i) { 
  o(i); i.lo=INF; i.hi=NINF; i.m2 = i.mu = i.n = 0 
}
# from http://people.ds.cam.ac.uk/fanf2/hermes/doc/antiforgery/stats.pdf
function all(f,i,a) { for(j in a) @f(i, a[j]) }

function num1(i,x,    d) {
  i.n++
  d     = x - i.mu
  i.mu += d/i.n
  i.m2 += d*(x - i.mu)
  i.sd  = (i.m2/(i.n - 1 + ZIP))^0.5
}
function numDec(i,x,    d) {
  if (i.n <= 2) return
  i.n--
  d     = x - i.mu
  i.mu -=  d/i.n
  i.m2 -= d*(x- i.mu)
  i.sd  = (i.m2/(i.n - 1 + ZIP))^0.5
}
function _nums( n,j,a) {
  split("4 10 15 38 54 57 62 83 100 100 174 190 215 225 "\
	"233 250 260 270 299 "\
        "300 306 333 350 375 443 475 525 583 780 1000",a)
  num(n)
  for (j=1;j<=length(a);j++) {
    num1(n, a[j])
    if ( j%2==0) print "+",n.n, n.mu, n.sd  }
  for (j=length(a);j>=0;j--) {
    numDec(n, a[j])
    if ((j-1)%2==0) print "-",n.n, n.mu, n.sd }
  
}

BEGIN { if (MAIN == "nums") _nums() }
