def once(f):
  s = "_" + f.__name__
  def g(i,*l,**k):
    d = i.__dict__
    x = d[s] = d[s] if s in d else f(i,*l,**k)
    return x
  return g

def kw(i,bad="_"):
  keys = lambda d: sorted([x for x in d.keys() if x[0] is not bad])
  pairs= lambda d: ['%s: %s' % (k,show(d[k])) for k in keys(d)]
  show = lambda x: x.__name__ if callable(x) else x
  return i.__class__.__name__+'<'+', '.join(pairs(i.__dict__)) +'>'

class Fred:
  def __init__(i,a=1): 
    i.a = a
    i.k = 10
  def __repr__(i): return kw(i)
  @once
  def b(i):
    return 10 if i.a > 0.5 else 0

x=Fred()
print(x.b())
print(x.b())
print(x.b())

print("")
x=Fred()
print(x.b())
print(x.b())
print(x.b())
print(x)
