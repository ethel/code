# /* vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: */

@include "lib.awk"
@include "num.awk"

function table(i) {
  obj(i,"table")
  has(i,"rows")
  i.n = 0
  i.sep = ","
}

function TableFromFile(i,file,    row,txt) {
  while((getline txt < file) > 0) {
    gsub(/[ \t\r]*/, "", txt) # no whitespce:
    gsub(/#["*"]$/,     "", txt) # no comments
    if (txt)                  # if anything left
      if (row) {
        has(i.rows, ++i.n, "row")
        RowFromString(i.rows.n, txt, i) 
      } else {
        TableHeader(i,txt)
        row++
}}}

function _table(   t) { 
  table(t)
  o(t,"t")
}

BEGIN {  if (MAIN == "table") _table() }
