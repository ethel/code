# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "lib"

func Csv(i) {
  class(i,"Csv")
  have(i,"nums")
  have(i,"syms")
  have(i,"xs")
  have(i,"ys")
  i.klassp = "/[" MORE LESS KLASS "]/"
  i.nump   = "/[" MORE LESS "\\" NUM "]/"
}

func csv2xy(file,callback,      sep,   
            txt,cells, c,line) {
  Csv(c)
  sep = sep ? sep : ","
  while((getline txt < file) > 0)  {
     gsub(/[ \t\r]*/, "", txt) # no whitespce:
     gsub(/#["*"]$/,     "", txt) # no comments
     if (txt) {
       split(txt,cells,sep)
       if (!line)  
         CsvFindColumnGroups(c,cells)
       line++
       CsvDivideIntoColumnGroups(c,callback,cells,line) }}
  close(file)
}
func CsvFindColumnGroups(c,cells,    j,cell) {
  for(j in cells) {
    cell = cells[j]
    if (cell !~ SKIP) {
       cell ~ c.klasssp ? c.xs[j]   : c.ys[j]
       cell ~ c.nump    ? c.nums[j] : c.syms[j] }}
}
func CsvDivideIntoColumnGroups(c,callback,cells,line,
			       x,y,z) {
   List(x)
   List(y)
   for(z in c.xs)   x[z] = cells[z]
   for(z in c.ys)   y[z] = cells[z] 
   for(z in nums) cells[z] +=0 # coercion to numbers
   @callback(c,x,y,line) 
}

func CSV_() { 
  csv2xy("____/____/data/auto__csv","CSV1") 
}
func CSV1(c,x,y,line) {
  o(x,"x")
  o(y,"y")
  o(c.nums,"nums")
  o(c.syms,"syms")
  if (line > 3) exit
}

BEGIN {if (MAIN=="csv") CSV_() }

