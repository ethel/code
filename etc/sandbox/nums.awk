function num(i) { 
  o(i); i.lo=INF; i.hi=NINF; i.m2 = i.m = i.n = 0 
}
# from http://people.ds.cam.ac.uk/fanf2/hermes/doc/antiforgery/stats.pdf
function num1(i,x,    b4) {
  i.n++
  b4    = i.mu
  i.mu += (x - i.mu)/i.n
  i.sd += (x-b4)*(x-i.mu)
}
function numDec(i,x,    b4) {
  i.n--
  b4 = i.mu
  i.mu -= (x-i.mu)/i.n
  i.sd -= (x-b4)(x-i.mu)
}
function _nums() {
  print(1)
}
