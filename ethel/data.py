import re
from oks import ok
from config import THE


def csv(file):
  for x,y in xy(  # seperate line into independent and depednent variables
              data(  # convert (some) strings to floats
                 cols(  # kill cols we are skipping
                    rows(  # kill blanks and comments
                       lines( # read lines from disk
                           THE.data))))):
    yield x,y

def lines(file):
  with open(file) as fs:
    for line in fs:
      yield line

def rows(src, doomed=r'([\n\r\t ]|#.*)', sep=","):
  # ascii file to rows of cells
  for line in src:
    line = re.sub(doomed, "", line)
    cells = line.split(sep)
    if len(cells) > 0:
      yield cells

def cols(src, skip="?"):
  use=None
  for row in src:
    use = use or [n for n, x in enumerate(row) if x[0] != skip]
    assert len(row) == len(use), 'row %s lacks %s cells' % (n, len(use))
    yield [row[n] for n in use]

def data(src, rules={"$": float, "<": float, ">": float, "_": int}):
  "rows of cells coerced to values according to the rules seen on line 1"
  changes = None
  change1 = lambda x, f: x if x[0] == "?" else f(x)
  for row in src:
    if changes:
      row = [change1(x, f) for x, f in zip(row, changes)]
    else:
      changes = [rules.get(x[0], str) for x in row]
    yield row

def xy(src, rules=['<', '>', '!']):
  "rows of values divided into independent and dependent values"
  xs, ys = None, None
  for row in src:
    xs = xs or [n for n, z in enumerate(row) if not z[0] in rules]
    ys = ys or [n for n, z in enumerate(row) if     z[0] in rules]
    yield [row[x] for x in xs], [row[y] for y in ys]

@ok
def XY():
  "demo xy import"
  for n, r in enumerate(csv(THE.data)):
    if n < 10:
      print(r)


