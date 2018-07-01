function _rogues(  sym) {
  for(sym in SYMTAB) 
    if (sym !~ /^[A-Z][A-Z]/) print("W> rogue local", sym)
}
function tests(    f) {
  for(f in FUNCTAB) 
    if (f ~ /^_/) {
      print "\n# " f;
      @f()
  }
}
