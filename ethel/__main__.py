#!/usr/bin/env python3
import argparse, getopt, math ,os , re, sys, time, traceback
from random     import random as r, choice as any, seed as ranseed
from contextlib import contextmanager

def help(): return [
"""ETHEL v0.1.0 multi-objective rule generator
(c) 2018: Tim Menzies timm@ieee.org, MIT license, v2""",
"""
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
  ["general",
      elp("start up action",                         main= ""),
      elp("random number seed",                      seed= 1),
      elp("define small change",                     cohen= [0.2, 0.1,0.3,0.5]),
      elp("input data svs file",                     data= "data/auto.csv"),
      elp("trace all calls",                         verbose= False),
      elp("decimals to display floats",              decimals= 3),
      elp("list unit tests",                         tests= False),
      elp("run unit tests",                          check= False)
  ],["top-down clustering",
      elp("min bin size = max(few, N^power)",        few= 10),
      elp("min bin size = max(few, N^power)",        power= 0.5),
      elp("enable heuristic comination",             speed= False),
      elp("in speed mode, min distance for retries", trivial= 0.05)
  ],["bottom-up pruning",
      elp("doubt reduction must be over x*unboubt",  undoubt= 0.05)
  ],["rule generation",
      elp("min supprot for acceptable rules",        least= 20),
      elp("build rules from top 'elite' ranges",     elite= 10)
  ]]

# command-line opionts

def elp(h, **d):
  def elp1():
    if val is False :
          return dict(help=h, action="store_true")
    elif isinstance(val,list):
          return dict(help=h+(";e.g. %s" % val[0]), choices=val,          
                      default=default, metavar=m ,type=t)
    else: 
          return dict(help=h + ("; e.g. %s" % val), 
                      default=default, metavar=m, type=t)
  key,val = list(d.items())[0]
  default = val[0] if isinstance(val,list) else val
  m,t = "S",str
  if isinstance(default,int)  : m,t= "I",int
  if isinstance(default,float): m,t= "F",float
  return  key, elp1()

def options(before, after, *lst):
  parser = argparse.ArgumentParser(epilog=after, description = before, 
                                   add_help=False,
              formatter_class = argparse.RawDescriptionHelpFormatter)
  seen=["h"]
  for group in lst:
      sub = parser.add_argument_group(group[0])
      for key, rest in group[1:]:
        flag = key[0]
        if flag in seen:
           sub.add_argument("--"+key,**rest)
        else:
           sub.add_argument("-" + flag, "--"+key,**rest)
           seen += [flag]
      if group[0]=="general":
        sub.add_argument("-h", "--help", action="help", 
                          help="show this help message and exit")
  return parser.parse_args()

THE = options(*help())
ranseed(THE.seed)

##################################
# Standard Library Functions
def rseed(seed=THE.seed):
  ranseed(seed)

PASS = FAIL = 0

def demo(f=None, act=None, show=None, all=[]):
  # Define functions we can call from command-line
  display = lambda f: re.sub(r'\n[ \t]*', "\n# ", f.__doc__ or "")
  def try1(fun):
    global PASS
    global FAIL
    print("\n-----| %s |-----------------------" % fun.__name__)
    if fun.__doc__: print("# " + display(fun))
    try:
      rseed()
      fun()
      PASS = PASS+1
    except Exception as e:
      FAIL = FAIL+1
      print(traceback.format_exc())
  if f:
    all += [f]
  elif show:
    for fun in all:
        print("%12s : %s" % (fun.__name__, display(fun)))
  elif act:
    for fun in all:
      if fun.__name__ == act:
        return try1(fun)
    print("unknown %s" % act)
  else:
    [try1(fun) for fun in all]
    print("\n# PASS= %s FAIL= %s %%PASS = %s%%" % (
          PASS, FAIL, int(round(PASS * 100 / (PASS + FAIL + 0.001)))))
  return f

# Low-level utilities

def same(x): return x
def sym(x): return x
def first(l): return l[0]
def second(l): return l[1]
def last(l): return l[-1]

def subsets(lst):
  if lst is None:
    return None
  subsets = [[]]
  lst1 = []
  for n in lst:
    for s in subsets:
      lst1.append(s + [n])
    subsets += lst1
    lst1 = []
  return subsets

@demo
def SUBSETS():
  "Can we find enough subsets of 4 things?"
  assert len(subsets('1234')) == 16

def timeit(f):
  t1 = time.perf_counter()
  f()
  return time.perf_counter() - t1

# JavaScript Envy

class o(object):
  # Javascript envy. Now 'o' is like a JS object.
  def __init__(i, **kv): i.__dict__.update(kv)
  def __setitem__(i, k, v): i.__dict__[k] = v
  def __getitem__(i, k): return i.__dict__[k]
  def __repr__(i): return i.__class__.__name__ + kv(i.__dict__, i._has())
  def __len__(i): return len(i.__dict__)
  def _has(i): return [k for k in sorted(i.__dict__.keys()) if k[0] != "_"]
  def keys(i): return i.__dict__.keys()

@demo
def OBJECT():
  "do we have something like a JS object?"
  x = o(name='alan', age=58)
  x["name"] = 'bill'
  assert x.name == 'bill'
  x.name = "clara"
  assert x.name == "clara"
  assert len(x) == 2
  x.age += 10
  x.age -= 1
  assert x.age == 67

def kv(d, keys=None):
  # print dictionary, in key sort order
  keys = keys or sorted(list(d.keys()))
  def pretty(x): 
    if callable(x):
      return x.__doc__
    else:
      return round(x, THE.decimals) if isinstance(x, float) else x
  return '{' + ', '.join(['%s: %s' % (k, pretty(d[k]))for k in keys]) + '}'

#-----------------------------
# tree routines

class Node(object):
  def __init__(i, left=None,right=None,_up=None):
    i.left, i.right, i._up = left, right, _up

def tree(t):
  if t:
    yield t
    for u in tree(t.left):  yield u
    for v in tree(t.right): yield v

def supertree(t):
  if t:
    yield t
    for u in supertree(t._up): yield u

def subtree(t):
  if t:
    for u in subtree(t.left):  yield u
    for v in subtree(t.right): yield v
    yield t

def leaves(t):
  for u in subtree(t):
    if not u.left and not u.right: yield u

def showt(t, tab="|.. ", pre="", lvl=0, val=lambda z: ""):
  if t:
    if lvl == 0: print("")
    val(t)
    print(' ' + tab * lvl + pre)
    if t.left:  showt(t.left, tab, "< ", lvl + 1, val)
    if t.right: showt(t.right, tab, "> ", lvl + 1, val)

#-----------------------------
def lines(file):
  with open(file) as fs:
    for line in fs:
      yield line

def rows(src, doomed=r'([\n\r\t ]|#.*)', sep=","):
  # ascii file to rows of cells
  for line in src:
    line = re.sub(doomed, "", line)
    cells = line.split(sep)
    if len(cells) > 0:
      yield cells

def cols(src, skip="?"):
  use=None
  for row in src:
    use = use or [n for n, x in enumerate(row) if x[0] != skip]
    assert len(row) == len(use), 'row %s lacks %s cells' % (n, len(use))
    yield [row[n] for n in use]

def data(src, rules={"$": float, "<": float, ">": float}):
  "rows of cells coerced to values according to the rules seen on line 1"
  changes = None
  change1 = lambda x, f: x if x[0] == "?" else f(x)
  for row in src:
    if changes:
      row = [change1(x, f) for x, f in zip(row, changes)]
    else:
      changes = [rules.get(x[0], lambda z:z) for x in row]
    yield row

def xy(src, rules=['<', '>']):
  "rows of values divided into independent and dependent values"
  xs, ys = None, None
  for row in src:
    xs = xs or [n for n, z in enumerate(row) if not z[0] in rules]
    ys = ys or [n for n, z in enumerate(row) if     z[0] in rules]
    yield [row[x] for x in xs], [row[y] for y in ys]

def csv(file):
  for row in xy(data(cols(rows(lines(THE.data))))):
    yield row

@demo
def XY():
  "demo xy import"
  for n, r in enumerate(csv(THE.data)):
    if n < 10:
      print(r)

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

@demo
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

@demo
def SYM():
  "Testing symbol calcs"
  s = Sym('timmenzies')
  assert 10 == s.n
  assert 2.722 == round(s.ent(),3)
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
  def dominates(i, j, weights, nums):
    s1, s2, n, e, z = 0, 0, len(i.y), 10, 10**-32
    for a, b, w, num in zip(i.y, j.y, weights, nums):
      a   = (a - num.lo) / (num.hi - num.lo + z)
      b   = (b - num.lo) / (num.hi - num.lo + z)
      s1 -= e**(w * (a - b) / n)
      s2 -= e**(w * (b - a) / n)
    return s1 / n < s2 / n

class Table:
  def __init__(i, decs, objs):
    i.rows = []
    i._dom = False
    i.x = o(head=decs,
            nums= [n for n, x in enumerate(decs) if x[0] == '$'],
            syms= [n for n, x in enumerate(decs) if x[0] != '$'])
    i.y = o(head=objs,
            weights= [1 if x[0] == ">" else -1 for x in objs],
            nums=    [Num() for _ in objs])
  def row(i, decs, objs):
    i.rows += [Row(decs, objs)]
    [ num + x for num,x in zip(i.y.nums, objs) ]
  def doms(i):
    if not i._dom:
      i._dom = True
      fastdom(i,THE.few, THE.power, THE.trivial) if THE.speed else slowdom(i)
    return i
  def splits(i):
    i.doms()
    val = {}
    for n in i.x.nums:
      tree = prune(grow(i.rows, 
                        x=lambda r: r.x[n], 
                        y=lambda r: r.dom))
      showt(tree, val=showNode)
      for u in leaves(tree):
        if u.useful:
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
  print("SLOWDOM")
  for row1 in t.rows:
    for row2 in t.rows:
      if row1.dominates(row2, t.y.weights, t.y.nums):
        row1.dom += 1

def fastdom(t, few=20, power=0.5, trivial=0.05):
  "O(Nlog(N)) approximate dom"
  print("FASTDOM")
  z   = 10**-32
  few = max(few, len(t.rows)**power)
  def dist(i, j):
    d,n = 0,z
    for a,b,num in zip(i.y, j.y, t.y.nums):
      a  = (a - num.lo) / (num.hi - num.lo + z)
      b  = (b - num.lo) / (num.hi - num.lo + z)
      d += (a-b)**2
      n += 1
    return d**0.5/n**0.5
  def furthest(i, lst):
    return sorted([(dist(i,j),j) for j in lst])[-1][1]
  def div(lst, rank, worst=None, excellent=None):
    if len(lst) > few:
      worst     = worst     or furthest(any(lst),  lst)
      excellent = excellent or furthest(worst, lst)
      if worst.dominates(excellent, t.y.weights, t.y.nums):
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

def table(file):
  t = None
  for x, y in csv(file):
    if t: t.row(x, y)
    else: t = Table(x, y)
  t.doms()
  return t

@demo
def DOM():
  "demo multi-objective domination"
  t = table(THE.data)
  t.doms()
  t.rows = sorted(t.rows)
  for row in t.rows[:10]: print("<", row.y, row.dom)
  print()
  for row in t.rows[-10:]: print(">", row.y, row.dom)

@demo
def FASTDOM():
  "demo multi-objective domination using an O(N) method"
  t = table(THE.data)
  fastdom(t,THE.few, THE.power, THE.trivial)
  t.rows = sorted(t.rows)
  for row in t.rows[:10]: print("<", row.y, row.dom)
  print()
  for row in t.rows[-10:]: print(">", row.y, row.dom)

class Range(object):
  def __init__(i, col, name, rows, lo, hi=None):
    if hi == None: hi = lo
    i.col,i.name,i.rows,i.lo,i.hi = col,name,rows,lo,hi
  
@demo
def SPLITS(file=THE.data):
  "show the trees"
  t = table(file)
  val = t.splits()
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

class DecisionNode(Node):
  def __init__(i,x,y,level,left=None,right=None,_up=None):
    i.x,i.y,i.level = x,y,level
    i.useful = False
    super().__init__(left=left,right=right,_up=_up)

def grow(lst, epsilon=None, few=None, x=same, y=same, klass=Num):
  "returns nil if nothing"
  def makeNode(lst, lvl=0, up=None):
    tmp = DecisionNode(x=Num(lst, f=x), y=klass(lst, f=y), level=lvl, _up=up)
    tmp.y.rows = lst
    return tmp

  def X(j): return notNull(x(lst[j]))

  def notNull(x): return -10**32 if x is '?' else x

  def mid(lo, hi):
    m = m1 = m2 = int(lo + (hi - lo) / 2)
    while m1 < hi - 1 and X(m1 - 1) == X(m1): m1 += 1
    while m2 > 0 and X(m2) == X(m2 - 1):      m2 -= 1
    m = m2 if (m - m2) < (m1 - m) else m1
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
  print('%s y=%6.3g sd=%6.3g  when %6.3g <= x <= %6.3g [%5s]' % (
    "\u2714" if z.useful else "\u2717",
    z.y.mu, z.y.sd(), z.x.lo, z.x.hi, z.y.n),end="")

def prune(t):
  for u in subtree(t):
    if u.left and u.right:
      if u.y.simpler(u.left.y, u.right.y, THE.undoubt):
        for v in supertree(u.left):  v.useful = True
        for w in supertree(u.right): w.useful = True
  return t

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

def HELLO(): 
  "Simple start up"
  print(help()[0])


if __name__ == '__main__':
  if THE.tests:
    demo(show=True)
  elif THE.main:
    demo(act=THE.main)
  else:
    demo() if THE.check else HELLO()