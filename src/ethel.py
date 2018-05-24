# ETHEL: a mulit-objective rule generator

from lib    import *
from config import *

THE = main(CONFIG())
DECIMALS = THE.decimals


@demo
def FORMO(): 
  "Simple start up"
  print(CONFIG()["why"])

# -------------

class Row(o):
  id = 0

  def __init__(i, x, y):
    i.x, i.y, i.dom = x, y, 0
    i._id = Row.id = Row.id + 1

  def __hash__(i):
    return i._id

  def __lt__(i, j):
    return i.dom < j.dom

  def dominates(i, j, weights, lows, highs):
    s1, s2, n, e, z = 0, 0, len(i.y), 10, 10**-32
    for a, b, w, lo, hi in zip(i.y, j.y,
                               weights, lows, highs):
      a = (a - lo) / (hi - lo + z)
      b = (b - lo) / (hi - lo + z)
      s1 -= e**(w * (a - b) / n)
      s2 -= e**(w * (b - a) / n)
    return s1 / n < s2 / n

class Table:
  def __init__(i, decs, objs):
    i.rows = []
    i._dom = False
    i.x = o(head=decs,
            nums=[n for n, x in enumerate(decs) if x[0] == '$'],
            syms=[n for n, x in enumerate(decs) if x[0] != '$'])
    i.y = o(head=objs,
            weights=[1 if x[0] == ">" else -1 for x in objs],
            lo=[10**32 for _ in objs],
            hi=[-10**32 for _ in objs])

  def row(i, decs, objs):
    def update(new, b4, f): return new if new == "?" else f(new, b4)
    i.rows += [Row(decs, objs)]
    i.y.lo = [update(now, b4, min) for now, b4 in zip(objs, i.y.lo)]
    i.y.hi = [update(now, b4, max) for now, b4 in zip(objs, i.y.hi)]

  def doms(i):
    if not i._dom:
      i._dom = True
      fastdom(i,THE.few, THE.power, THE.trivial) if THE.speed else slowdom(i)
    return i

  def splits(i):
    i.doms()
    val = {}
    for n in i.x.nums:
      tree = prune(grow(i.rows, x=lambda r: r.x[n], y=lambda r: r.dom))
      showt(tree, val=showNode)
      for u in leaves(tree):
        if u.simpler:
          key = (n, u.x.lo)
          val[key] = u.y
          u.y.key = key
    for row in i.rows:
      for n in i.x.syms:
        key = (n, row.x[n])
        tmp = val[key] if key in val else Num()
        tmp.key = key
        tmp.rows += [row]
        tmp + row.dom
        val[key] = tmp
    return val

def slowdom(t):
  "O(N)^2 dom"
  for row1 in t.rows:
    for row2 in t.rows:
      if row1.dominates(row2, t.y.weights, t.y.lo, t.y.hi):
        row1.dom += 1

def fastdom(t, few=20, power=0.5, trivial=0.05):
  "O(Nlog(N)) approximate dom"
  z   = 10**-32
  few = max(few, len(t.rows)**power)

  def dist(i, j):
    d,n = 0,z
    for a,b,lo,hi in zip(i.y, j.y, t.y.lo, t.y.hi):
      a  = (a - lo) / (hi - lo + z)
      b  = (b - lo) / (hi - lo + z)
      d += (a-b)**2
      n += 1
    return d**0.5/n**0.5

  def furthest(i, lst):
    most,out = -1,i
    for j in lst:
      d = dist(i,j)
      if d > most: most,out = d,j
    return out

  def div(lst, rank, worst=None, excellent=None):
    if len(lst) > few:
      worst     = worst     or furthest(any(lst),  lst)
      excellent = excellent or furthest(worst, lst)
      if worst.dominates(excellent, t.y.weights, t.y.lo, t.y.hi):
        return div(lst,  rank, excellent, worst)
      c   = dist(worst,excellent)
      tmp = []
      for row in lst:
        a = dist(worst, row)
        if a > trivial+c:
          return div(lst, rank,  row, worst)
        b = dist(excellent, row)
        if b > trivial+c:
          return div(lst, rank,  row, excellent)
        x    = (a*a + c*c - b*b) / (2*c + z)
        tmp += [(x,row)]
      tmp = [pair[1] for pair in sorted(tmp)]
      mid = len(lst)//2
      rank = div(lst[:mid],rank) 
      rank= div(lst[mid:], rank)
    else:
      rank += len(lst)
      for one in lst: 
        one.dom = rank
    return rank

  return div(t.rows,0)

def table(file):
  t = None
  for x, y in xy(data(rows(file))):
    if t:
      t.row(x, y)
    else:
      t = Table(x, y)
  t.doms()
  return t

@demo
def DOM():
  t = table(THE["DATA"])
  t.doms()
  t.rows = sorted(t.rows)
  for row in t.rows[:10]:
    print("<", row.y, row.dom)
  print()
  for row in t.rows[-10:]:
    print(">", row.y, row.dom)

@demo
def FASTDOM():
  seed(1)
  t = table(THE["DATA"])
  t.doms()
  fastdom(t,THE.few, THE.power, THE.trivial)
  t.rows = sorted(t.rows)
  for row in t.rows: print("<", row.y, row.dom, row.dom1)

@demo
def SPLITS(file=THE["DATA"]):
  t = table(file)
  val = t.splits()
  lst = sorted(val.values(), key=lambda z: z.mu, reverse=True)
  for x in lst:
    print(x.key, x, len(x.rows))
  out = []
  for sub in subsets(lst[:THE.elite]):
    one =  combine(sub, THE.least)
    if one:
      keys, some, cardinality = one
      out += [(keys, Num(some, f=lambda r: r.dom), cardinality)]
  out = sorted(out, key=lambda z:len(z[0]))
  best = -1
  for a,b,c in out: 
    if b.mu > best:
      best = b.mu
      print(int(b.mu), b.n, a)

def combine(ranges, few):
  ors, keys = {}, {}
  for r in ranges:
    col, val = r.key
    ors[col] = set(r.rows) | ors.get(col, set())
    keys[col] = keys.get(col, []) + [val]
  ands = None
  for one in ors.values():
    ands = ands & one if ands else one
  if ands and len(ands) > few:
    return keys, ands, len(ranges)

def grow(lst, epsilon=None, few=None, x=same, y=same, klass=Num):
  "returns nil if nothing"
  def makeNode(lst, lvl=0, up=None):
    tmp = o(x=Num(lst, f=x), y=klass(lst, f=y),
            level=lvl,
            _up=up,
            simpler=False, left=None, right=None)
    tmp.y.rows = lst
    return tmp

  def X(j): return notNull(x(lst[j]))

  def notNull(x): return -10**32 if x is '?' else x

  def mid(lo, hi):
    m = m1 = m2 = int(lo + (hi - lo) / 2)
    while m1 < hi - 1 and X(m1 - 1) == X(m1):
      m1 += 1
    while m2 > 0 and X(m2) == X(m2 - 1):
      m2 -= 1
    m = m2 if (m - m2) < (m1 - m) else m
    return m

  def recurse(lo=0, hi=len(lst), up=None, lvl=0):
    node = makeNode(lst[lo:hi], lvl=lvl, up=up) if lvl else up
    m = mid(lo, hi)
    if hi - m > few:
      if m - lo > few:
        if X(m) - X(lo) > epsilon:
          if X(hi - 1) - X(m) > epsilon:
            node.left = recurse(lo=lo, hi=m, up=node, lvl=lvl + 1)
            node.right = recurse(lo=m, hi=hi, up=node, lvl=lvl + 1)
    return node
  lst = sorted(lst, key=lambda row: notNull(x(row)))
  root = makeNode(lst)
  epsilon = epsilon or root.x.sd() * THE.cohen
  few = max(few or len(lst)**THE.power, THE.few)
  print(dict(epsilon=epsilon, few=few))
  return recurse(up=root)

def showNode(z):
  f = plain if z.simpler else red
  f('%s y=%6.3g sd=%6.3g  when %6.3g <= x <= %6.3g [%5s]' % (
    "\u2714" if z.simpler else "\u2717",
    z.y.mu, z.y.sd(), z.x.lo, z.x.hi, z.y.n))

def _grow(X=same, Y=same, N=10000):
  def flats(y):
    if 33 < y < 66:
      return y
    return 0

  def show(z): return [X(z), flats(z)]
  seed(1)
  print("\n--------------------------")
  tree = grow([show(int(100 * r())) for _ in range(N)],
              x=first,
              y=last)
  prune(tree)
  showt(tree, val=showNode)
  print([u.x.lo for u in leaves(tree) if u.simpler])
  return tree

def prune(t):
  for u in subtree(t):
    # if not u.simpler:
    if u.left and u.right:
      if u.y.simpler(u.left.y, u.right.y, THE.undoubt):
        for v in supertree(u.left):
          v.simpler = True
        for w in supertree(u.right):
          w.simpler = True
  return t

@demo
def GROW0(): _grow(N=4096)

@demo
def GROW1(): _grow(X=lambda x: 0 if x < 40 else x, N=64)

@demo
def GROW2():
  def xx(x):
    if x < 10: return x
    if x < 40: return 40
    if x < 70: return x
    return 70
  _grow(X=xx, N=256)

def globs():  
  for k,v in globals().items():
     if callable(v):
         print(k, v.__module__)

if __name__ == '__main__':
  demo(act=THE.MAIN)
  globs()

