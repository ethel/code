# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "math"

"""

## Lists

"""

function show(l,pre) { 
  print str(l,pre) 
}
function str(l,pre,   txt,x) { 
  if (pre)
     for (x in l) txt= txt pre"["x"]="l[x] " "
  else
     for (x in l) txt= txt x"="l[x] " "
  return txt 
}
function o(l,prefix,order,       indent,old,i) {
  old = PROCINFO["sorted_in"]
  prefix=prefix == "" ? "o " : prefix
  if(! isarray(l)) {
    print "not array",prefix,l
    return 0}
  if(!order)
    for(i in l) {
      if (isnum(i))
        order = "@ind_num_asc"
      else
        order = "@ind_str_asc"
      break
    }
   PROCINFO["sorted_in"]= order
   for(i in l)
     if (isarray(l[i])) {
       print prefix  indent "[" i "]"
       o(l[i],prefix,order, indent ":   ")
     } else
       print prefix  indent "[" i"]  = (" l[i] ")"
   PROCINFO["sorted_in"]  = old
}



