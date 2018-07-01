from config import THE
from random import choice as any

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


