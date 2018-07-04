# /* vim: set ts=2 sw=2 sts=2 expandtab: */

"""

## Numbers

"""
function abs(x) { return x>0 ? x : -1*x }

function isnum(x) {
  return x=="" ? 0 : x == (0+strtonum(x))
}

