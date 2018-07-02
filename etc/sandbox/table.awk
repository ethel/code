# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

@include "lib.awk"
@include "num.awk"
@include "sym.awk"
@include "row.awk"

function Table(i) {
  class(i,"Table")
  have(i,"X","XY")
  have(i,"Y","XY")
  have(i,"rows")
  i.n = 0
  i.sep = ","
}
function XY(i) {
  class(i,"Part")
  have(i,"head")
  have(i,"nums")
  have(i,"syms")
  have(i,"stats")
  have(i,"w")
} 
function TableFromFile(i,file,    row,txt) {
  row=0
  while((getline txt < file) > 0) {
    gsub(/[ \t\r]*/, "", txt) # no whitespce:
    gsub(/#["*"]$/,     "", txt) # no comments
    if (txt)                  # if anything left
      if (row) {
        has(i.rows, ++i.n, "Row")
        RowFromString(i.rows.n, txt, i) 
      } else {
        TableHeader(i,txt)
        row++
}}}

function _Table(   t) { 
  Table(t)
  o(t,"t")
}

BEGIN { if (MAIN == "table") _Table() }
