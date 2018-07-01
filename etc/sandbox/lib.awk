"""
system Constants
"""

BEGIN {
  INF=10^32;  NINF= -10^32; ZIP=1/INF; 
  PI=3.14159; EE=2.719
  SKIP="?"; MORE=">"; LESS="<"; KLASS="!"; NUM="$"
}
function o(i)   { split("",i,"") }

function str(l,pre,   txt,x) { 
  if (pre)
     for (x in l) txt= txt pre"["x"]="l[x] " "
  else
     for (x in l) txt= txt x"="l[x] " "
  return txt 
}
function show(l,pre) { print str(l,pre) }
