require "csv"

------------------------------
-- ## Data class
-- Holds rows of data.
-- Data columns are classified in numerous ways.
-- 
-- - Independent and depdendent columns are labelled `x,y` (respectively);
-- - `nums` and `syms` hold numeric or symbolic columns,
-- - goals to be maximized/minimized are held in `less,more`
-- - If the data has a class, that is held in `klass`. 
--
-- Note that the above categories are not mutually exclusive.
-- and many columns have multiple categories (e.g. `x.nums`,
-- `y.less`, etc).

Data = Any:new{
  name, header, klass,
  rows={}, 
  all={nums={}, syms={}, cols={}}, -- all columns
  x  ={nums={}, syms={}, cols={}}, -- all independents
  y  ={nums={}, syms={}, cols={},  -- all dependent columns
       less={}, more={}}}  

-- ### Data:csv(file: string)
-- Read data in  from `file`.
function Data:csv(file)
  for row in csv(file) do self:inc(row) end end

-- ### Data:inc(row: list)
-- If this is the first row, interpret `row` as the column headers.
-- Otherwise, read `row` as data.
function Data:inc(row)
  if   self.header then self:data(row) 
  else self.header=row; self:head(row) end end

-- ### Data:data(row: list)
-- Add `row` to `self.rows`. Increment the header statistics
-- with information from `row`'s values.
function Data:data(row) 
   self.rows[ #self.rows + 1 ] = row
   for _,thing in pairs(self.all.cols) do
     thing:inc( row[thing.pos ] ) end end

-- ### Data:header(row: list)
-- Build the data headers.
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

-------------------------------------------------
-- ## Test Stuff

function weatherOkay()   dataOkay("weather") end
function autoOkay()      dataOkay("auto") end
function auto10KOkay()   dataOkay("auto1OK") end
function auti1000KOkay() dataOkay("auto1000K") end

function dataOkay(f)
  d = Data:new()
  d:csv("../../data/".. f .. ".csv")
  for _,x in pairs(d.all.cols) do 
	  print(x:doubt()); 
	  oo(x) end end


-------------------------------------------------
-- ## Main Stuff

main{data=weatherOkay}
