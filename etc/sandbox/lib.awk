# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

"""
System Constants
"""

@include "object.awk"

BEGIN {
  INF=10^32;  NINF= -10^32; ZIP=1/INF; 
  PI=3.14159; EE=2.719
  SKIP="?"; MORE=">"; LESS="<"; KLASS="!"; NUM="$"
  OID=1
}
function list(i) { split("",i,"") }

function obj(i,ako ) { 
  list(i)
  i.id = ++OID
  i.ako= ako
}
function has(lst,key,fun) {
  lst[key][SUBSEP]
  split("",lst[key],"")
  if (fun) @fun(lst[key])
}
function has1(lst,key,fun,a)         { has(lst,key); @fun(lst[key],a) }
function has2(lst,key,fun,a,b)       { has(lst,key); @fun(lst[key],a,b) }
function has3(lst,key,fun,a,b,c)     { has(lst,key); @fun(lst[key],a,b,c) }
function has4(lst,key,fun,a,b,c,d)   { has(lst,key); @fun(lst[key],a,b,c,d) }
function has5(lst,key,fun,a,b,c,d,e) { has(lst,key); @fun(lst[key],a,b,c,d,e) }

function abs(x) { return x>0 ? x : -1*x }

function show(l,pre) { print str(l,pre) }

function str(l,pre,   txt,x) { 
  if (pre)
     for (x in l) txt= txt pre"["x"]="l[x] " "
  else
     for (x in l) txt= txt x"="l[x] " "
  return txt 
}

function isnum(x) {
  return x=="" ? 0 : x == (0+strtonum(x))
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
