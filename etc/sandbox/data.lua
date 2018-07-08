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
-- Read data in  from `file`. Return `self`.
function Data:csv(file)
  for row in csv(file) do self:inc(row) end 
  return self end

-- ### Data:inc(row: list)
-- If this is the first row, interpret `row` as the column headers.
-- Otherwise, read `row` as data.
function Data:inc(row)
  push(row, self.rows)
  if   self.header then self:data(row) 
  else self.header=row; self:head(row) end end

-- ### Data:data(row: list)
-- Add `row` to `self.rows`. Increment the header statistics
-- with information from `row`'s values.
function Data:data(row) 
   push(row,self.rows, row)
   for _,thing in pairs(self.all.cols) do
     thing:inc( row[thing.pos ] ) end end

-- ### Data:header(row: list)
-- Build the data headers.
function Data:head(row)
  local done= function (z) return true                   end
  local less= function (z) push(z, self.y.less); z.w= -1 end
  local more= function (z) push(z, self.y.more);         end
  local klass=function (z) self.klass = z                end
  local all = {{" ", Sym, "x","syms", done},  -- default
               {"%$",Num, "x","nums", done},  -- others
               {"<" ,Num, "y","nums", less},
               {">" ,Num, "y","nums", more},
               {"!" ,Sym, "y","syms", klass}}
  local function what2do(pos, txt, t)
    for i=2,#all do
      if string.find(txt, all[i][1]) then t=all[i] end end
    return t[2]:new{pos=pos,txt=txt}, t[3], t[4], t[5] end

  for pos,txt in pairs(row) do 
    local thing, xy, kind, also = what2do(pos,txt, all[1])
    also(thing)
    push(thing, self.all.cols)
    push(thing, self.all[kind])
    push(thing, self[xy].cols)
    push(thing, self[xy][kind])  end end

-------------------------------------------------
-- ## Test Stuff
function autoOkay()      dataOkay("auto") end
function auto10KOkay()   dataOkay("auto10K") end
function auto1000KOkay() dataOkay("auto1000K") end
function weatherOkay()   
  local d = dataOkay("weather") 
  assert( close( d.all.syms[1]:ent(),  1.57) ) 
  assert( close( d.all.syms[2]:ent(),  0.98) )  
  assert( close( d.all.syms[3]:ent(),  0.94) )  
  assert( close( d.all.nums[1].mu,    73.57) )
  assert( close( d.all.nums[1]:sd(),   6.57) )  end

function dataOkay(f)
  roguesOkay()
  return Data:new():csv("../../data/".. f .. ".csv") end

-------------------------------------------------
-- ## Main Stuff

main{data=weatherOkay}