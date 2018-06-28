from lib import *
from oks import ok

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

@ok
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


