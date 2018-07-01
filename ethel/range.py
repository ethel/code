from obj    import Pretty
from config import THE

class Range(Pretty):
  def __init__(i, rows=[], col=None, ,head=None,about=Num,
                  score= lambda z: z.y[-1]):
     i.col, i._rows, i.head = col, rows,   head
     i.about  = lambda: about(f=score)
     i._stats = None
     [i + row for row in i.rows]
  def __add__(i,row):
     i._rows += [row]
     i._stats=None
  def stats(i):
     if not i._stats:
       i._stats = i.about()
       [i._stats + i.score(row) for row in i.rows]
     return i._stats
  def __lt__(i,j):
    return i.stats().mu > j.stats().mu
  def __eq__(i,j):
    return set([row.id for row in i.rows]) == set([row.id for row in j.rows])

class NumRange(Range):
   def __init__(i, lo=None,hi=None,**kw):
     i.lo, i.hi = lo, hi
     super().__init__(**kw)
   def __repr__(i):
     fmt = '%%s = [%%8.%sf .. %%8.%sf)' % (THE.decimals, THE.decimals)
     return fmt % ( i.head, i.lo,i.hi) 
    
class SymRange(Range):
   def __init__(i, has=None,**kw):
     i.has= has
     super().__init__(**kw)
   def __repr__(i):
     return ' %s=%s' % (i.head, i.has)

class Ranges(Pretty):
  def __init__(i,ranges=None,elite=THE.elite,least=THE.least):
    ranges = sorted(ranges)[:elite]
    i.ors, i.keys = {},{}
  def learn(i):
    for _ in range(10):
      new = sorted(old)[:elite]
      new = [one for one in one if len(one._rows) >= least]
      if new <= old: return new
      new = old
      
