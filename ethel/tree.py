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

def left(t, up=None):
  return left(t.left,t) if t else up

def right(t, up=None):
  return right(t.right,t) if t else up

def showt(t, tab="|.. ", pre="", lvl=0, val=lambda z: ""):
  if t:
    if lvl == 0: print("")
    val(t)
    print(' ' + tab * lvl + pre)
    showt(t.left,  tab, "< ", lvl + 1, val)
    showt(t.right, tab, "> ", lvl + 1, val)
