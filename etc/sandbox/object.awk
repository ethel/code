# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

func List(i) { split("",i,"") ; return "List" }

func Object(i) { 
  List(i)
  i.id = ++AU.id
  i.ako= ako
  return "Object"
}

func class(i,kid,up)  {        
  up = up ? up : "Object"
  AU.parent[kid]=up
  @up(i) 
  i.ako = kid
}
func clasS(i,kid,up,a)         { AU.parent[kid]=up; @up(i,a); i.ako=kid }
func claSS(i,kid,up,a,b)       { AU.parent[kid]=up; @up(i,a,b); i.ako=kid }
func clASS(i,kid,up,a,b,c)     { AU.parent[kid]=up; @up(i,a,b,c); i.ako=kid }
func cLASS(i,kid,up,a,b,c,d)   { AU.parent[kid]=up; @up(i,a,b,c,d); i.ako=kid }

func have(i,key,fun) {
  i[key][0] # temp holder to make a sub-array
  split("",i[key],"")
  if (fun) @fun(i[key])
}
func havE(i,key,fun,a)         { have(i,key); @fun(i[key],a) }
func haVE(i,key,fun,a,b)       { have(i,key); @fun(i[key],a,b) }
func hAVE(i,key,fun,a,b,c)     { have(i,key); @fun(i[key],a,b,c) }
func HAVE(i,key,fun,a,b,c,d)   { have(i,key); @fun(i[key],a,b,c,d) }

func polymorphism(i,f,    class,g) {
  class=i.ako
  do { 
    g= class f
    if (g in FUNCTAB) {
      METHOD=g
      return
    }
    class = AU.parent[class]
  } while(class)
  print "#E> undefined " f " in " class 
  exit 1
}
