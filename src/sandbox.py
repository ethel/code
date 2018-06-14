def once(f):
  s0 = "_" + f.__name__
  def wrapped(i,*l,**k):
    d = i._cache
    s = (s0,l[0]) if l else s0
    old = d.get(s,None)
    if old: return old
    new = d[s] = f(i,*l,**k)
    return new
  return wrapped

def kwi(i): 
  return kw(i.__dict__, str(i.__class__.__name__))
def kw(d, pre=""):
  keys = lambda: sorted([x for x in d.keys()],key=lambda z:str(z))
  pairs= lambda: ['%s: %s' % (k,show(d[k])) for k in keys()]
  show = lambda x: x.__name__ if callable(x) else str(x)
  return pre+'<' + ', '.join(pairs()) + '>'

class Cache:
  def __new__(i, *l, **kw):
    tmp = super().__new__(i,*l,**kw)
    tmp._cache= {}
    return tmp

class Fred (Cache):
  def __init__(i,a=1): 
    i.a = a
    i.k = 10
  def __repr__(i): return kwi(i)
  @once
  def b(i):
    return 10 if i.a > 0.5 else 0
  @once
  def fib(i,n):
    if n<2: return n
    return i.fib(n-2) + i.fib(n-1)

x=Fred()
print(x.b())
print(x.b())
print(x.b())

print("")
x=Fred()
print(x.b())
print(x.b())
print(x.b())

for i in range(10,1,-2):
  print(i,x.fib(i))
  if i == 6:
    x.__dict__[('_fib',2)] = None
print(x)
