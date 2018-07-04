# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

#include everyone

@include "lib"
@include "num"
@include "sym"
@include "table"


func rogueLocals_(  sym, n) {
  for(sym in SYMTAB) 
    if (sym !~ /^[A-Z][A-Z]/) 
      print "W> "++n" rogue local(s) [" sym "]"
  return n > 0
}
func tests(    f,try,fail,err) {
  for(f in FUNCTAB) { 
    if (f ~ /_$/) {
      try++
      print "\n### " f "\n";
      if (@f())  {
        fail++
	      print "\n### E >>>>>>>>>>>>> " f " FAIL!!! " }}}
  print "\n### Tries=",y,
        "Failures=",n,
        "("100*int(0.5+ (fail+0)/(try+ZIP)" %)" 
}

BEGIN { print 1; tests() }