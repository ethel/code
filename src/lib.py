from config import CONFIG

import getopt
import math
import os
import re
import sys
import time
import traceback
from random import random as r, choice as any, seed as seed
from colorama import Fore, Style
from contextlib import contextmanager

# Globals

DECIMALS = 3
PASS = FAIL = 0

# Standard Library Functions


def demo(f=None, act=None, all=[]):
  # Define functions we can call from command-line
  def try1(fun):
    global PASS
    global FAIL
    print("\n-----| %s |-----------------------" % fun.__name__)
    if fun.__doc__:
      print("# " + re.sub(r'\n[ \t]*', "\n# ", fun.__doc__))
    try:
      fun()
      PASS = PASS+1
    except Exception as e:
      FAIL = FAIL+1
      print(traceback.format_exc())

  if f:
    all += [f]
  elif act:
    for fun in all:
      if fun.__name__ == act:
        return try1(fun)
    print("unknown %s" % act)
  else:
    print(all)
    [try1(fun) for fun in all]
    print("\n# PASS= %s FAIL= %s %%PASS = %s%%" % (
          PASS, FAIL, int(round(PASS * 100 / (PASS + FAIL + 0.001)))))
  return f

# Low-level utilities


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

# Coloring


class Highlight:
  def __init__(i, clazz, color):
    i.color = color
    i.clazz = clazz

  def __enter__(i):
    print(i.color, end="")

  def __exit__(i, type, value, traceback):
    if i.clazz == Fore:
      print(Fore.RESET, end="")
    else:
      assert i.clazz == Style
      print(Style.RESET_ALL, end="")
    sys.stdout.flush()


def plain(s): print(s, end="")


def red(s):
  with Highlight(Fore, Fore.RED):
    print(s, end="")


def the(b4):
  # Tool for creating our global 'THE'
  now = o()

  def options(x): return x if isinstance(x, list) else [x]
  for k in b4["what"].keys():
    now[k] = options(b4["what"][k]["what"])[0]
  return now

def kv(d, keys=None):
  # print dictionary, in key sort order
  keys = keys or sorted(list(d.keys()))
  def pretty(x): return round(x, DECIMALS) if isinstance(x, float) else x
  return '{' + ', '.join(['%s: %s' % (k, pretty(d[k]))for k in keys]) + '}'

# Command line option manager


def main(about, argv=None):
  # Configure command line parser from keys of dictonary 'd'
  d = the(about)
  argv = argv or sys.argv[1:]
  keys = sorted([k for k in about["what"].keys()])
  mark = lambda k: "" if isinstance(d[k], bool) else ":"
  opts = 'hC%s' % ''.join(['%s%s' % (k[0], mark(k)) for k in keys])
  oops = lambda x, y=2: print(x) or sys.exit(y)

  def one(d, slot, opt, arg):
    what = slot["what"]
    if isinstance(what, bool):
      return not what
    want = slot["want"]
    arg = (slot.get("make", want))(arg)
    if not want(arg):
      oops("%s: %s is not %s" % (opt, arg, want.__name__))
    if isinstance(what, list):
      if arg not in what:
        oops("%s: %s is not one of %s" % (opt, arg, what))
    return arg

  def oneLine():
    print(about["why"], "\n", '(c) ', about["when"], ", ", about["who"], sep="")

  def usage():
    oneLine()
    print('\nUSAGE: ',
          about["how"], " -", ''.join([s for s in opts if s != ':']),
          sep="", end="\n\n")
    for k in keys:
      print("  -%s\t%-10s\t%s    (default=%s)" % (
          k[0], k, about["what"][k]["why"], d[k]))
    print("  -h\t%-10s\tshow help" % '')
    oops("  -C\t%-10s\tshow copright" % '', 0)

  def copyrite():
    oneLine()
    oops(about["copyright"], 0)

  try:
    com, args = getopt.getopt(argv, opts)
    for opt, arg in com:
      if opt == '-h':
        usage()
      elif opt == '-C':
        copyrite()
      else:
        for k in keys:
          if opt[1] == k[0]:
            try:
              d[k] = one(d, about["what"][k], opt, arg)
            except Exception as err:
              oops(err)
  except getopt.GetoptError as err:
    oops(err)
  return d

def rows(file, doomed=r'([\n\r\t]|#.*)', sep=",", skip="?"):
  # ascii file to rows of cells
  use = None
  with open(file) as fs:
    for n, line in enumerate(fs):
      line = re.sub(doomed, "", line)
      cells = [z.strip() for z in line.split(sep)]
      if len(cells) > 0:
        use = use or [n for n, x in enumerate(cells) if x[0] != skip]
        assert len(cells) == len(use), 'row %s lacks %s cells' % (n, len(use))
        yield [cells[n] for n in use]

def data(src, rules={"$": float, "<": float, ">": float}):
  "rows of cells coerced to values according to the rules seen on line 1"
  changes = None

  def change1(x, f): return x if x[0] == "?" else f(x)
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

@demo
def CSV():
  for n, r in enumerate(data(rows(THE["DATA"]))):
    if n < 10:
      print(r)

#-----------------------------

def tree(t):
  if t:
    yield t
    for u in tree(t.left):
      yield u
    for v in tree(t.right):
      yield v

def supertree(t):
  if t:
    yield t
    if t._up:
      for u in supertree(t._up):
        yield u

def subtree(t):
  if t:
    for u in subtree(t.left):
      yield u
    for v in subtree(t.right):
      yield v
    yield t

def leaves(t):
  for u in subtree(t):
    if not u.left and not u.right:
      yield u

def showt(t, tab="|.. ", pre="", lvl=0, val=lambda z: ""):
  if t:
    if lvl == 0:
      print("")
    val(t)
    print(' ' + tab * lvl + pre)
    if t.left:
      showt(t.left, tab, "< ", lvl + 1, val)
    if t.right:
      showt(t.right, tab, "> ", lvl + 1, val)

#--------------------------------------

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
    i.lo = 10**32

  def doubt(i):
    return i.sd()

  def _add(i, x):
    i.hi = max(i.hi, x)
    i.lo = min(i.lo, x)
    delta = x - i.mu
    i.mu += delta / i.n
    i.m2 += delta * (x - i.mu)

  def sd(i):
    return (i.m2 / (i.n - 1))**0.5

  def __repr__(i):
    return 'Num' + kv(dict(lo=i.lo, hi=i.hi, mu=i.mu, sd=i.sd(), n=i.n))


class Sym(Thing):
  def locals(i): i.seen, i._ent = {}, None

  def doubt(i):
    return i.ent()

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


