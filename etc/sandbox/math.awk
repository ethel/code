# /* vim: set ts=2 sw=2 sts=2 expandtab: */

"""

## Numbers

"""
func abs(x) { return x>0 ? x : -1*x }

func isnum(x) {
  return x=="" ? 0 : x == (0+strtonum(x))
}

