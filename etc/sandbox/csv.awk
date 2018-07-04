# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "lib"
@include "thing"

func Csv(i) {
  class(i,"Csv")
  have(i,"x")
  have(i,"y")
  have(i,"xy")
  have(i,"use")
  i.klassp = "[" MORE LESS KLASS "]"
  i.nump   = "[" MORE LESS NUM "]"
  i.sep    = ","
}
func Row(i) {
  class(i,"Row")
  have(i,"x")
  have(i,"y")
  i.dom  = 0
  i.best = 0
}
func RowInc(i, csv, cells) {
  for(pos in csv.use) {
    xy = csv.xy[pos]
    i[xy][pos] =  @Inc(csv[xy][pos], cells[pos]) }
}

func CsvFromFile(i,file,        txt,cells, line) {
  while((getline txt < file) > 0)  {
     gsub(/[ \t\r]*/, "", txt) # no whitespce:
     gsub(/#["*"]$/,     "", txt) # no comments
     if (txt) {
       split(txt,cells, i.sep)
       if (line++) {
         have(i.rows,line,"Row")
         RowInc(i.rows[line],i,cells)  }
       else
         CsvHeader(i,cells)  }}
  close(file)
}
func CsvHeader(i,cells,       j,txt,pos,xy,what) {
  for(j=1;j<=length(cells);j++) {
    txt = cells[j]
    if (txt !~ SKIP) {
      i.use[++pos] = j
      xy = i.xy[pos] = txt ~ i.klassp ? "y"   : "x"
      what  = txt ~ i.nump   ? "Num" : "Sym"
      haVE(i[xy],pos,what,txt,pos)
      if (txt ~ i.LESS)  i[where][pos].w= -1
      if (txt ~ i.KLASS) i.klass=pos }}
}       
func CSV_(    c) { 
  Csv(c)
  CsvFromFile(c,"____/____/data/auto__csv") 
}
func CSV1(c,x,y,line) {
  print line
 # o(x,"x")
 # o(y,"y")
 # o(c.nums,"nums")
 # o(c.syms,"syms")
 # if (line > 3) exit
}

BEGIN {if (MAIN=="csv") CSV_() }

