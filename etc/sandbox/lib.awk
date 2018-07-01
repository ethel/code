"""
system Constants
"""

BEGIN {
  INF=10^32;  NINF= -10^32
  PI=3.14159; EE=2.719
  SKIP="?"; MORE=">"; LESS="<"; KLASS="!"; NUM="$"
}
function o(i)   { split("",i,"") }

function show(l,str,    x) { 
  for (x in l) str= x"="l[x]
  return str 
}
BEGIN {print 10}
