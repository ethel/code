# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "lib"

func Csv(i) {
  class(i,"Csv")
  have(i,"nums")
  have(i,"syms")
  have(i,"xs")
  have(i,"ys")
  have(i,"x","XY")
  have(i,"y","XY")
  i.klassp = "[" MORE LESS KLASS "]"
  i.nump   = "[" MORE LESS NUM "]"
  i.sep    = ","
}
func XY(i) {
  class(i,"Thing")
  have(i,"nums")  # list of indexes
  have(i,"syms")  # list of indexes
  have(i,"stats") # Num or Sym object
}

func CsvFromFile(i,file,callback,        txt,cells, line) {
  sep = sep ? sep : ","
  while((getline txt < file) > 0)  {
     gsub(/[ \t\r]*/, "", txt) # no whitespce:
     gsub(/#["*"]$/,     "", txt) # no comments
     if (txt) {
       split(txt,cells, i.sep)
       if (!line)  
         CsvFindColumnGroups(i,cells)
       line++
       CsvDivideIntoColumnGroups(i,callback,cells,line) }}
  close(file)
}
func CsvFindColumnGroups(i,cells,    j,cell) {
  for(j in cells) {
    cell = cells[j]
    if (cell !~ SKIP) {
       (cell ~ i.klassp) ? have(i.y,j,"Num")  : have(i.x,j,"Sym")
       (cell ~ i.nump)   ? i.nums[j] : i.syms[j] }}
}
func CsvDivideIntoColumnGroups(i,callback,cells,line,    x,y,z) {
   List(x)
   List(y)
   for(z in i.xs)   x[z] = cells[z]
   for(z in i.ys)   y[z] = cells[z] 
   for(z in nums) cells[z] +=0 # coercion to numbers
   @callback(i,x,y,line) 
}

func CSV_(    c) { 
  Csv(c)
  CsvFromFile(c,"____/____/data/auto__csv","CSV1") 
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

