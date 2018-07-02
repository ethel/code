# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

@include "lib"

# sym : utilities

@include "lib"

func Sym(i) {
  class(i,"Syms")
  have(i,"counts")
  i.mode = ""
  i.most = 0
  i._ent =""
  i.n = 0
}
func SymInc(i,x,   tmp) {
  if( x == SKIP ) return x
  i.n++
  i._ent = ""
  tmp = i.counts[x] = i.counts[x] + 1
  if(tmp > i.mode) {
    i.most = tmp
    i.mode = x }
  return x
}
func SymDec(i,x,   tmp) {
  if( x == SKIP ) return x
  i.n--
  i._ent = ""
  i.counts[x]--
  return x
}
func SymEnt(i,   x,p) {
  if(!i._ent)
    for(x in i.counts) {
      p = i.counts[x]/i.n
      i._ent -= p * log(p) / log(2) }
  return i._ent
}
func SYM() {
  "Testing symbol calcs"
  split("timmenzies",a,"")

 # assert 10 == s.n
  #assert 2.722 == round(s.ent(),3)
}
#BEGIN { if(MAIN == "sym") print Sym_() }


