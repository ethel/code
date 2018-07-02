# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

function _rogueLocals(  sym, n) {
  for(sym in SYMTAB) 
    if (sym !~ /^[A-Z][A-Z]/) 
      print "W> "++n" rogue local(s) [" sym "]"
  return n > 0
}
function tests(    f,y,n,err) {
  y=n=0;
  for(f in FUNCTAB) { 
    if (f ~ /^_/) {
      y++
      print "\n### " f "\n";
      if (err = @f())  {
        n += err
	      print "\n### E >>>>>>>> " f " FAIL!!! " }}}
  print "\n### Tries= "y,
        "Failures= "n,
        "( "100*int(0.5+ n/y)" %)" 
}

BEGIN { print 1; tests() }
