require "csv"

Data = Any:new{
  name, header, klass,
  rows={}, 
  all={nums={}, syms={}, cols={}}, -- all columns
  x  ={nums={}, syms={}, cols={}}, -- all independents
  y  ={nums={}, syms={}, cols={},  -- all dependent columns
       less={}, more={}}}  

function Data:csv(file)
  for row in csv(file) do self:inc(row) end end

function Data:inc(row)
  if   self.header then self:data(row) 
  else self.header=row; self:head(row) end end

function Data:data(row) 
   self.rows[ #self.rows + 1 ] = row
   for _,thing in pairs(self.all.cols) do
     thing:inc( row[thing.pos ] ) end end

function Data:head(row)
  local all,x,y=self.all, self.x, self.y
  local default= {what= Sym, weight=  1, 
                  where = {all.cols,all.syms,x.cols,x.syms}}
  local spec= {
    {when="%$", what= Num, weight=  1, 
           where= {all.cols,all.nums,x.cols,x.nums}},
    {when="<",  what= Num, weight= -1, 
           where= {all.cols,all.nums,y.cols,y.nums,y.less}},
    {when= ">", what= Num, weight=  1, 
           where= {all.cols,all.nums,y.cols,y.nums,y.more}},
    {when="!",  what= Sym, weight=  1, 
           where= {all.cols,all.syms,y.cols,y.syms}}}

  local function categorize(txt, out)
    for _,x in pairs(spec) do
      if string.find(txt,x.when)  then out = x end end
    return out end

  for pos,txt in pairs(row) do 
    local x     = categorize(txt,default)
    local thing = x.what:new{pos=pos, txt=txt, w=x.weight}
    if string.find(txt,"!") then -- add to class def
      self.klass = thing end
    for _,where in pairs(x.where) do -- add thing to many places
      where[ #where+1 ] = thing  end end  end
 
function weatherOkay()   dataOkay("weather") end
function autoOkay()      dataOkay("auto") end
function auto10KOkay()   dataOkay("auto1OK") end
function auti1000KOkay() dataOkay("auto1000K") end

function dataOkay(f)
  d = Data:new()
  d:csv("../../data/".. f .. ".csv")
  for _,x in pairs(d.all.cols) do oo(x) end end

main{data=weatherOkay}
