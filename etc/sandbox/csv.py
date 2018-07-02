# /* vim: set ts=2 sw=2 sts=2 expandtab: */

@include "array"

"""

## csv

"""

func  csv2xy(file,f,reader,   sep,   
                  txt,cells, x,y, xs, ys, nums,syms,line,z) {
  line = 0
  sep = sep ? sep : ","
  while((getline txt < file) > 0)  {
     gsub(/[ \t\r]*/, "", txt) # no whitespce:
     gsub(/#["*"]$/,     "", txt) # no comments
     if (txt) {
       split(txt,cells,sep)
       if (line==0)  
         findDifferentKindsofColumns(cells, xs,ys,nums,syms)
       for(z in xs)   x[z] = cells[z]
       for(z in ys)   y[z] = cells[z] 
       for(z in nums) cells[z] +=0 # coercion to numbers
       @f(reader,++line,x,y,nums,syms) }}
  close(file)
}
func findDifferentKindsofColumns(cells, xs,ys,nums,syms,
                                     klassp,nump,j,cell) {
  klassp = "(" MORE "|" LESS "|" KLASS ")"
  nump   = "(" MORE "|" LESS "|" NUM ")"
  for(j=1;j<=length(cells);j++) {
    cell = cells[j]
    if (cell !~ SKIP) {
       cells[j] ~ klasssp ? xs[j]   : ys[j]
       cells[j] ~ nump    ? nums[j] : syms[j] }}
}
func CSV_() { 
  csv2xy("____/____/data/auto__csv","CSV1") 
}
func CSV1(_,line,x,y,nums,syms) {
  o(x,"x")
  o(y,"y")
  o(nums,"nums")
  o(syms,"syms")
  if (line > 3) exit
}

BEGIN {if (MAIN=="c") CSV_() }

