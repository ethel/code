# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

function List(i) { split("",i,"") }

function Object(i) { 
  List(i)
  i.id = ++AU.id
  i.ako= ako
}
function class(i,kid,up)  {        
  up = up ? up : "Object"
  AU.parent[kid]=up
  @up(i) 
  i.ako = kid
}
function clasS(i,kid,up,a)         { AU.parent[kid]=up; @up(i,a); i.ako=kid }
function claSS(i,kid,up,a,b)       { AU.parent[kid]=up; @up(i,a,b); i.ako=kid }
function clASS(i,kid,up,a,b,c)     { AU.parent[kid]=up; @up(i,a,b,c); i.ako=kid }
function cLASS(i,kid,up,a,b,c,d)   { AU.parent[kid]=up; @up(i,a,b,c,d); i.ako=kid }

function holds(i,key,fun) {
  i[key][0] # temp holder to make a sub-array
  split("",i[key],"")
  if (fun) @fun(i[key])
}
function holdS(i,key,fun,a)         { holds(i,key); @fun(i[key],a) }
function holDS(i,key,fun,a,b)       { holds(i,key); @fun(i[key],a,b) }
function hoLDS(i,key,fun,a,b,c)     { holds(i,key); @fun(i[key],a,b,c) }
function hOLDS(i,key,fun,a,b,c,d)   { holds(i,key); @fun(i[key],a,b,c,d) }

function polymorphism(i,f,    class,g) {
  class=i.ako
  do { 
    g= class f
    if (g in FUNCTAB) {
      METHOD= g
      return
    }
    class = AU.parent[class]
  } while(class)
  print "#E> undefined " f " in " class 
  exit 1
}
