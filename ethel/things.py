import math
from config import THE
from oks import ok
from obj import o
#--------------------------------------
# Things are either Nums or Syms

class Thing(o):
  def __init__(i, inits=[], f=lambda z: z):
    i.locals()
    i.rows = []
    i.n, i._f = 0, f
    [i + x for x in inits]
  def __add__(i, x):
    x = i._f(x)
    if x != '?':
      i.n += 1
      i._add(x)
  def simpler(i, j, k, undoubt=1.05):
    return i.doubt() > undoubt * (
        j.doubt() * j.n / i.n + k.doubt() * k.n / i.n)

class Num(Thing):
  def locals(i):
    i.mu = i.m2 = 0
    i.hi = -10**32
    i.lo =  10**32
  def doubt(i): return i.sd()
  def sd(i): return (i.m2 / (i.n - 1))**0.5
  def norm(i,x): 
    return (x - i.lo) / (i.hi - i.lo + 10**-32)
  def _add(i, x):
    i.hi = max(i.hi, x)
    i.lo = min(i.lo, x)
    delta = x - i.mu
    i.mu += delta / i.n
    i.m2 += delta * (x - i.mu)
  def __repr__(i):
    return 'Num' + kv(dict(lo=i.lo, hi=i.hi, mu=i.mu, sd=i.sd(), n=i.n))

@ok
def NUM():
  "Testing numeric calcs"
  n = Num([12, 15, 67, 34, 56, 12, 98, 60, 24])
  assert 29.996 == round(n.sd(),3)
  assert 9      == n.n
  assert 42     == n.mu
  
class Sym(Thing):
  def locals(i): i.seen, i._ent = {}, None
  def doubt(i): return i.ent()
  def _add(i, x):
    i.seen[x] = i.seen.get(x, 0) + 1
    i._ent = None
  def ent(i):
    if i._ent is None:
      i._ent = 0
      for _, v in i.seen.items():
        p = v / i.n
        i._ent -= p * math.log(p, 2)
    return i._ent
  def __repr__(i):
    return 'Sym' + kv(dict(seen=i.seen, ent=i.ent(), n=i.n))

@ok
def SYM():
  "Testing symbol calcs"
  s = Sym('timmenzies')
  assert 10 == s.n
  assert 2.722 == round(s.ent(),3)

