import random,re,traceback
from config import THE

PASS=FAIL=0

def demo(f=None, act=None, show=None, all=[]):
  # Define functions we can call from command-line
  display = lambda f: re.sub(r'\n[ \t]*', "\n# ", f.__doc__ or "")
  def try1(fun):
    global PASS
    global FAIL
    print("\n-----| %s |-----------------------" % fun.__name__)
    if fun.__doc__: print("# " + display(fun))
    try:
      random.seed(THE.seed)
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


