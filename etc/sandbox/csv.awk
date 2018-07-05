# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "lib"
@include "thing"

function Csv(i) {
  isa(Object(i))
  holds(i,"x")
  holds(i,"y")
  holds(i,"xy")
  holds(i,"rows")
  holds(i,"use")
  i.klassp = "[" MORE LESS KLASS "]"
  i.nump   = "[" MORE LESS NUM "]"
}
function Row(i) {
  isa(Object(i))
  holds(i,"cells")
  i.dom  = 0
  i.best = 0
}
function RowInc(i,csv,cells,   pos,xy) {
  for(pos in csv.use)  {
    xy = csv.xy[pos]
    i.cells[pos] = @Inc(csv[xy][pos], cells[pos]) }
}
function CsvFromFile(i,file,        txts,txt,cells, row) {
  while((getline txt < file) > 0)  {
     gsub(/[ \t\r]*/, "", txt) # no whitespce:
     gsub(/#["*"]$/,     "", txt) # no comments
     if (txt) {
       txts = txts txt
       if (txts !~ /,$/) {
         split(txts, cells, ",")
         txts = ""
         if (row) {
           holds(i.rows, row, "Row")
           RowInc(i.rows[row], i, cells) 
         }
         else  
           CsvHeader(i,cells) 
         row++
  }}}
  close(file)
}
function CsvHeader(i,cells,       j,txt,pos,xy,what) {
  for(j in cells) {
    txt = cells[j]
    if (txt !~ SKIP) {
      i.use[++pos] =  j
      xy    = i.xy[pos] = (txt ~ i.klassp) ? "y"   : "x"
      what  = (txt ~ i.nump)               ? "Num" : "Sym"
      holDS(i[xy],pos,what,pos,txt)
      if (txt ~ LESS)  i[xy][pos].w= -1
      if (txt ~ KLASS) i.klass=pos 
  }}
}       
function auto_() { csv1("auto") }
function weather_() { csv1("weather") }

function csv1(d,    c) { 
  Csv(c)
  CsvFromFile(c,"____/____/data/"  d "__csv") 
  o(c.x)
}

BEGIN {if (MAIN=="csv") weather_()  }

