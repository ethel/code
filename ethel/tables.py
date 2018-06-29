from obj    import o,Pretty
from data   import csv, fromFile, fromString
from things import Num
from config import THE
from oks    import ok
from tree   import *
from lib    import *
from random import choice as any
from range  import NumRange,SymRange

class Row(Pretty):
  id = 0
  def __init__(i, x, y):
    i.x, i.y, i.dom = x, y, 0
    i._id = Row.id = Row.id + 1
  def __hash__(i):
    return i._id
  def __lt__(i, j):
    return i.dom < j.dom
  def dominates(i, j, weights, nums):
    s1, s2, n, e, z = 0, 0, len(i.y), 10, 10**-32
    for a, b, w, num in zip(i.y, j.y, weights, nums):
      a   = (a - num.lo) / (num.hi - num.lo + z)
      b   = (b - num.lo) / (num.hi - num.lo + z)
      s1 -= e**(w * (a - b) / n)
      s2 -= e**(w * (b - a) / n)
    return s1 / n < s2 / n

class Table(Pretty):
  def __init__(i, decs, objs):
    i.rows = []
    i._dom = False
    print(decs,objs)
    i.x = o(head=decs,
            nums= [n for n, x in enumerate(decs) if x[0] == '$'],
            syms= [n for n, x in enumerate(decs) if x[0] != '$'])
    i.y = o(head=objs,
            weights= [1 if x[0] == ">" else -1 for x in objs],
            stats =    [Num() for _ in objs])
  def row(i, decs, objs):
    i.rows += [Row(decs, objs)]
    [ num + x for num,x in zip(i.y.stats, objs) ]
  def doms(i):
    if not i._dom:
      i._dom = True
      fastdom(i,THE.few, THE.power, THE.trivial) if THE.speed else slowdom(i)
    return i
  def splits(i):
    i.doms()
    ranges=[]
    for pos,n in enumerate(i.x.nums):
      tree = prune(grow(i.rows, 
                        x=lambda r: r.x[n], 
                        y=lambda r: r.dom))
      #showt(tree, val=showNode)
      ranges += [NumRange(lo=u.x.lo, hi=u.x.hi, col=pos, rows=u.rows, head=i.x.head[n]) 
                 for u in leaves(tree) if u.useful]
    for pos,n in enumerate(i.x.syms):
      seen = {}
      print(n)
      for row in i.rows:
         key = row.x[n]
         if key not in seen:
            seen[key] = range1 = SymRange(has=key,col=n, head=i.x.head[n])
            ranges += [range1]
         seen[key] + row
    print(ranges)
    print(i.x)
#
def table(src):
  t = None
  for x, y in csv(src):
    if t: t.row(x, y)
    else: t = Table(x, y)
  t.doms()
  return t

def prune(t):
  for u in subtree(t):
    if u.left and u.right:
      if u.y.simpler(u.left.y, u.right.y, THE.undoubt):
        for v in supertree(u.left):  v.useful = True
        for w in supertree(u.right): w.useful = True
  return t

class DecisionNode(Node):
  def __init__(i,x,y,level,rows,left=None,right=None,_up=None):
    i.x,i.y,i.level = x,y,level
    i.rows = rows
    i.useful = False
    super().__init__(left=left,right=right,_up=_up)

def grow(lst, epsilon=None, few=None, x=same, y=same, klass=Num):
  "returns nil if nothing"
  def node0(lst, lvl=0, up=None):
    return  DecisionNode(Num(lst, f=x), klass(lst, f=y), lvl, lst, _up=up)

  notNull = lambda x: -10**32 if x is '?' else x
  X       = lambda j: notNull(x(lst[j]))

  def mid(lo, hi):
    m = m1 = m2 = int(lo + (hi - lo) / 2)
    while m1 < hi - 1 and X(m1 - 1) == X(m1): m1 += 1
    while m2 > 0 and X(m2) == X(m2 - 1):      m2 -= 1
    m = m2 if (m - m2) < (m1 - m) else m1
    return m

  def recurse(lo=0, hi=len(lst), up=None, lvl=0):
    node = node0(lst[lo:hi], lvl=lvl, up=up) if lvl else up
    m = mid(lo, hi)
    if hi - m > few:
      if m - lo > few:
        if X(m) - X(lo) > epsilon:
          if X(hi - 1) - X(m) > epsilon:
            node.left  = recurse(lo=lo, hi=m, up=node, lvl=lvl + 1)
            node.right = recurse(lo=m, hi=hi, up=node, lvl=lvl + 1)
    return node
  # --- main -------
  lst     = sorted(lst, key=lambda row: notNull(x(row)))
  root    = node0(lst)
  epsilon = epsilon or root.x.sd() * THE.cohen
  few     = max(few or len(lst)**THE.power, THE.few)
  print(dict(epsilon=epsilon, few=few))
  return recurse(up=root)

def showNode(z):
  print('%s y=%6.3g sd=%6.3g  when %6.3g <= x <= %6.3g [%5s]' % (
    "\u2714" if z.useful else "\u2717",
    z.y.mu, z.y.sd(), z.x.lo, z.x.hi, z.y.n),end="")

@ok
def SPLITS(file=THE.data):
  "show the trees"
  t = table(fromFile(file))
  val = t.splits()
  return 1
  lst = sorted(val.values(), key=lambda z: z.mu, reverse=True)
  out = []
  print("lst ",lst[0].key, len(lst[0].rows))
  print(t.x.head)
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
      print(int(b.mu), b.n, printRange(t,a))

def printRange(t,d):
   return {t.x.head[k]:d[k] for k in d}

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


def _grow(X=same, Y=same, N=10000):
  def flats(y):
    if 33 < y < 66:
      return y
    return 0

  def show(z): return [X(z), flats(z)]
  print("\n--------------------------")
  tree = grow([show(int(100 * r())) for _ in range(N)],
              x=first,
              y=last)
  prune(tree)
  showt(tree, val=showNode)
  print([u.x.lo for u in leaves(tree) if u.useful])
  return tree


@ok
def GROW0(): _grow(N=4096)

@ok
def GROW1(): _grow(X=lambda x: 0 if x < 40 else x, N=64)

@ok
def GROW2():
  def xx(x):
    if x < 10: return x
    if x < 40: return 40
    if x < 70: return x
    return 70
  _grow(X=xx, N=256)

def slowdom(t):
  "O(N)^2 dom"
  print("SLOWDOM")
  for row1 in t.rows:
    for row2 in t.rows:
      if row1.dominates(row2, t.y.weights, t.y.stats):
        row1.dom += 1

def fastdom(t, few=20, power=0.5, trivial=0.05):
  "O(Nlog(N)) approximate dom"
  print("FASTDOM")
  z   = 10**-32
  few = max(few, len(t.rows)**power)
  def dist(i, j):
    d,n = 0,z
    for a,b,num in zip(i.y, j.y, t.y.stats):
      a  = (a - num.lo) / (num.hi - num.lo + z)
      b  = (b - num.lo) / (num.hi - num.lo + z)
      d += (a-b)**2
      n += 1
    return d**0.5/n**0.5
  def furthest(i, lst):
    return sorted([(dist(i,j),j) for j in lst])[-1][1]
  def div(lst, rank, worst=None, excellent=None):
    if len(lst) > few:
      if worst     == None: worst     = furthest(any(lst),  lst)
      if excellent == None: excellent = furthest(worst, lst)
      if worst.dominates(excellent, t.y.weights, t.y.stats):
        return div(lst, rank, excellent, worst)
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
      rank= div(lst[:mid], rank) 
      rank= div(lst[mid:], rank)
    else:
      rank += len(lst)
      for one in lst: 
        one.dom = rank
    return rank
  #-- main
  return div(t.rows,0)

@ok
def DOM():
  "demo multi-objective domination"
  t = table(fromFile(THE.data))
  t.doms()
  t.rows = sorted(t.rows)
  for row in t.rows[:10]: print("<", row.y, row.dom)
  print()
  for row in t.rows[-10:]: print(">", row.y, row.dom)

@ok
def FASTDOM():
  "demo multi-objective domination using an O(N) method"
  t = table(fromFile(THE.data))
  fastdom(t,THE.few, THE.power, THE.trivial)
  t.rows = sorted(t.rows)
  for row in t.rows[:10]: print("<", row.y, row.dom)
  print()
  for row in t.rows[-10:]: print(">", row.y, row.dom)
