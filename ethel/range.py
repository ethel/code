from obj    import Pretty
from config import THE

class Range(Pretty):
  def __init__(i, col=None, rows=None,head=None):
     i.col, i._rows, i.head = col, rows or [],   head
  def __add__(i,row):
     i._rows += [row]

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
