# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

@include "lib"

function Row(i) {
  class(i,"Row")
  holds(i,"x")
  holds(i,"y")
  i.dom=0
  i.best=0
}

function RowFromString(i,txt,t,   col) {
  split(txt,cells,t.sep)
  for(col in t.nums)
     i.cells[col] = i.cells.col + 0
  RowSummary(i,t)
}
function RowSummary(i,t,    col) {
  for (col in t.nums)
    NumAdd(t.nums.col, i.cells.col)
  for (col in t.syms)
    SymAdd(t.syms.col, i.cells.col)
}


