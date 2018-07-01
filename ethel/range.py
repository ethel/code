from obj    import Pretty
from config import THE

class Range(Pretty):
  def __init__(i, rows=[], col=None, ,head=None,stats=Num,
                  score= lambda z: z.y[-1]):
     i.col, i._rows, i.head = col, rows,   head
     i.stats=stats()
     [i + row for row in i.rows]
  def __add__(i,row):
     i._rows += [row]
     i.stats + i.score(row)
  def __lt__(i,j):
    return i.stats.mu > j.stats.mu

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

class Rule(Pretty):
  def __init__(i,ranges=None):
    i.ors, i.keys = {},{}

