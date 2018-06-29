from __init__ import *

if THE.tests:
  ok(show=True)
elif THE.act:
  ok(act=THE.act)
else:
  ok() if THE.check else print(fullLines(THE.HELLO))
