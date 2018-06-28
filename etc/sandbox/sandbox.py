import re,os
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


def once(f):
  s0 = "_" + f.__name__
  def wrapped(i,*l,**k):
    d = i._cache
    s = (s0,l[0]) if l else s0
    old = d.get(s,None)
    if old: return old
    new = d[s] = f(i,*l,**k)
    return new
  return wrapped

def kwi(i): 
  return kw(i.__dict__, str(i.__class__.__name__))
def kw(d, pre=""):
  keys = lambda: sorted([x for x in d.keys()],key=lambda z:str(z))
  pairs= lambda: ['%s: %s' % (k,show(d[k])) for k in keys()]
  show = lambda x: x.__name__ if callable(x) else str(x)
  return pre+'<' + ', '.join(pairs()) + '>'

class Cache:
  def __new__(i, *l, **kw):
    tmp = super().__new__(i,*l,**kw)
    tmp._cache= {}
    return tmp

class Fred (Cache):
  def __init__(i,a=1): 
    i.a = a
    i.k = 10
  def __repr__(i): return kwi(i)
  @once
  def b(i):
    return 10 if i.a > 0.5 else 0
  @once
  def fib(i,n):
    if n<2: return n
    return i.fib(n-2) + i.fib(n-1)

x=Fred()
print(x.b())
print(x.b())
print(x.b())

print("")
x=Fred()
print(x.b())
print(x.b())
print(x.b())

for i in range(6,100,15):
  print(i,x.fib(i))
  if i == 6:
    x.__dict__[('_fib',2)] = None
print(x)

###############################################

class Xpect(object):
  all = {}
  def __init__(i, act=None, prompt=None, flag=None, 
                  ako=None, default=None):
    i.act,i.flag,i.ako,  i.val,i.prompt = \
     None,  flag,  ako,default,  prompt
  def ftype(i):
    return i.ako.__name__.upper()
  def bad(i,x):
    if not i.ako(x):
      return '%s is not %s' % i.ako.__name__
  @staticmethod
  def call(x):
    meta = Xpect.all[x]
    f    = meta[0]
    args = [y.val for y in meta[1:]]
    return f(*args)
  def help(x):
    meta = Xpect.all[x]
    name = meta[0].__name__
    doc  = "  "+re.sub(r'\n[ \t]*', "\n  ",meta[0].__doc__)
    args = meta[1:]
    print('%s\n\n%s\n' % (name,doc))
    show = [('--%s' % y.flag, y.ftype(), y.prompt,str(y.val)) 
            for y in args]
    lens  = [[len(one) for one in trio] for  trio in show]
    widths= ''.join(['  %%-%ss' % max(*m) for m in zip(*lens)])
    [print(widths % one) for one in show]

class Xpects(Xpect):
  def ftype(i):
    return type(i.ako[0]).__name__.upper()
  def bad(i,x):
    if x not in i.ako:
      return '%s not one of %s' % (x,i.ako)

def flags(**kw):
  def decorator(f):
    s = f.__name__
    holder = Xpect.all[s] = [f]
    for k in kw:
      maker = kw[k]
      maker.flag = k
      holder += [ maker ]
    return f
  return decorator

def filep(f) : return os.exist(f)
def posint(f): return int(f) and f >= 0

String = lambda x,y: Xpect(ako= str,   default=x,    prompt=y)
Int    = lambda x,y: Xpect(ako= int,   default=x,    prompt=y)
Float  = lambda x,y: Xpect(ako= float, default=x,    prompt=y) 
File   = lambda x,y: Xpect(ako= filep, default=x,    prompt=y)
Bool   = lambda x,y: Xpect(ako= bool,  default=x,    prompt=y)
OneOf  = lambda x,y: Xpects(ako= x,    default=x[0], prompt=y)

@flags(what    = String("world","print string"), 
       repeats = Int(3,"number of repeats"))
def hello(what, repeats):
  """documentation for this function can
   spill over many
   lines"""
  for _ in range(repeats):
     print('Hello %s' % what)

Xpect.call("hello")
Xpect.help("hello")
