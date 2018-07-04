# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "lib"
@include "thing"

function Csv(i) {
  class(i,"Csv")
  holds(i,"x")
  holds(i,"y")
  holds(i,"xy")
  holds(i,"use")
  i.klassp = "[" MORE LESS KLASS "]"
  i.nump   = "[" MORE LESS NUM "]"
}
function Row(i) {
  class(i,"Row")
  holds(i,"cells")
  i.dom  = 0
  i.best = 0
}
function RowInc(i, csv, cells) {
  for(pos in csv.use) {
    xy = csv.xy[pos]
    i[xy][pos] =  @Inc(csv[xy][pos], cells[pos]) }
}

function CsvFromFile(i,file,        txts,txt,cells, line) {
  while((getline txt < file) > 0)  {
     gsub(/[ \t\r]*/, "", txt) # no whitespce:
     gsub(/#["*"]$/,     "", txt) # no comments
     if (txt) {
       if (txt ~ /,$/)
         txts = txts txt
       else {
         split(txts,cells, ",")
         txts = ""
         if (line++) {
           holds(i.rows,line,"Row")
           RowInc(i.rows[line],i,cells)  }
         else
           CsvHeader(i,cells)  }}}
  close(file)
}
function CsvHeader(i,cells,       j,txt,pos,xy,what) {
  for(j=1;j<=length(cells);j++) {
    txt = cells[j]
    if (txt !~ SKIP) {
      i.use[++pos] = j
      xy = i.xy[pos] = txt ~ i.klassp ? "y"   : "x"
      what  = txt ~ i.nump   ? "Num" : "Sym"
      holDS(i[xy],pos,what,txt,pos)
      if (txt ~ i.LESS)  i[where][pos].w= -1
      if (txt ~ i.KLASS) i.klass=pos }}
}       
function CSV_(    c) { 
  Csv(c)
  CsvFromFile(c,"____/____/data/auto__csv") 
}
function CSV1(c,x,y,line) {
  print line
 # o(x,"x")
 # o(y,"y")
 # o(c.nums,"nums")
 # o(c.syms,"syms")
 # if (line > 3) exit
}

BEGIN {if (MAIN=="csv") CSV_() }

