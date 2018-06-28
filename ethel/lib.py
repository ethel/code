import random
from oks import ok
from config import THE

##################################

r = random.random

def rseed(seed=THE.seed):
  random.seed(seed)

def same(x): return x
def sym(x): return x
def first(l): return l[0]
def second(l): return l[1]
def last(l): return l[-1]

def fullLines(lines):
  return "\n".join([s for s in lines.split("\n") if s])

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

@ok
def SUBSETS():
  "Can we find enough subsets of 4 things?"
  assert len(subsets('1234')) == 16

def timeit(f):
  t1 = time.perf_counter()
  f()
  return time.perf_counter() - t1

def kv(d, keys=None):
  # print dictionary, in key sort order
  keys = keys or sorted(list(d.keys()))
  def pretty(x): 
    if callable(x):
      return x.__doc__
    else:
      return round(x, THE.decimals) if isinstance(x, float) else x
  return '{' + ', '.join(['%s: %s' % (k, pretty(d[k]))for k in keys]) + '}'


