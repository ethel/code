# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

@include "lib"
@include "num"
@include "sym"
@include "row"

func Table(i) {
  class(i,"Table")
  have(i,"X","XY")
  have(i,"Y","XY")
  have(i,"rows")
  i.n = 0
  i.sep = ","
}
func XY(i) {
  class(i,"Part")
  have(i,"nums")
  have(i,"syms")
  have(i,"w")
} 
func TableRow(i,values,    j,w,value) {
  j = length(i.rows) + 1
  has(i.rows, j, "Row")
  for(w in i.rw) {
    value = values[ i.rw[w] ]
    if (w in i.nums)
       value = NumInc(i.cols[w], value)
     else
       value = SymInc(i.cols[w], value);
    i.rows[j].raw[w] = value
}}

func Table_(   t) { 
  Table(t)
  o(t,"t")
}

BEGIN { if(MAIN == "table")   Table_() }
