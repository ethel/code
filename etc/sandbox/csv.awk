# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "lib"

func Csv(i) {
  class(i,"Csv")
  have(i,"nums")
  have(i,"syms")
  have(i,"x")
  have(i,"y")
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

func CsvFromFile(i,file,        txt,cells, line) {
  line=0
  sep = sep ? sep : ","
  while((getline txt < file) > 0)  {
     gsub(/[ \t\r]*/, "", txt) # no whitespce:
     gsub(/#["*"]$/,     "", txt) # no comments
     if (txt) {
       split(txt,cells, i.sep)
       if (line=0)  
         CsvHeader(i,cells)
       CsvInc(i,cells,++line) }}
  close(file)
}
func CsvHeader(i,cells,    j,z) {
  for(j in cells) {
    z = cells[j]
    if (z !~ SKIP)  
      z ~ i.klassp ? head1(i.y,j,z, z~i.nump) : head1(i.x,j,z,z~i.nump)
}}
func head1(a,j,txt,nump) {
  have(a,j, nump ? "Num" : "Sym")
  a[j].txt = txt
  a[j].pos = j
}
func CsvRow(i,callback,cells,line,    x,y,z) {
   List(x)
   List(y)
   for(z in i.x)   x[z.pos] = cells[z.pos]
   for(z in i.ys)   y[z.pos] = cells[z.pos] 
   for(z in nums) cells[z] +=0 # coercion to numbers
   #XXX make sym num compile string
   @callback(i,x,y,line) 
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

