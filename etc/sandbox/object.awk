# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

func List(i) { split("",i,"") }

func Object(i) { 
  class(i, "Object", "List")
  i.id = ++AU.id
  i.ako= ako
}

func class(i,kid,up)  {        
  up = up ? up : "Object"
  AU.parent[kid]=up
  @up(i) 
  i.ako = kid
}
func clasS(i,kid,up,a)         { AU.parent[kid]=up; @up(i,a) }
func claSS(i,kid,up,a,b)       { AU.parent[kid]=up; @up(i,a,b) }
func clASS(i,kid,up,a,b,c)     { AU.parent[kid]=up; @up(i,a,b,c) }
func cLASS(i,kid,up,a,b,c,d)   { AU.parent[kid]=up; @up(i,a,b,c,d) }

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
  while (class)  {
    g= class f
    if (f in FUNCTAB)
      return f
    class = AU.parent[class]
  }
  print "#E> undefined " f " in " class 
  exit 1
}
