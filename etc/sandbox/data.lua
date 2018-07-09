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

Row = Any:new{cells, dom=0, best=false}

-------------------------------------------------
-- ## Data Methods
--
-- ### Data:csv(file: string)
-- Read data in  from `file`. Return `self`.
function Data:csv(file)
  for row in csv(file) do self:inc(row) end 
  return self end

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
   push( Row:new{cells=row}, self.rows )
   for _,thing in pairs(self.all.cols) do
     thing:inc( row[thing.pos ] ) end end

-- ### Data:head(row: list)
-- Build the data headers.
function Data:head(columns)
  local less= function (i) push(i, self.y.less); i.w= -1 end
  local more= function (i) push(i, self.y.more) end
  local klass=function (i) self.klass = i end
  local all = {{".", Sym, "x","syms"      }, -- default
	       {"%$",Num, "x","nums"      },
               {"<" ,Num, "y","nums", less},
               {">" ,Num, "y","nums", more},
               {"!" ,Sym, "y","syms", klass}}
  local function which(txt,t)
    for _,u in pairs(all) do   --    for all header types
      if string.find(txt, u[1]) then t=u end end
    return t end

  for pos,txt in pairs(columns) do 
    local _,what,xy,ako,also = unpack( which(txt,all[1]) )
    local it = what:new{pos=pos,txt=txt}
    if also then also(it) end 
    push(it, self.all[ako]); push(it, self[xy].cols)
    push(it, self.all.cols); push(it, self[xy][ako]) 
  end end

-------------------------------------------------
-- ## Row Methods
--
function Data:dominate(i,j) 
  oo(i)
  local s1, s2, n, z = 0, 0, #self.y.nums, The.zip
  for pos,num in pairs(self.y,nums) do
    local a = i.cells[ pos ]
    local b = j.cells[ pos ]
    print(a,b,num)
    oo(num)
    a       = (a - num.lo) / (num.hi - num.lo + z)
    b       = (b - num.lo) / (num.hi - num.lo + z)
    s1      = s1 - 10^(num.w * (a - b) / n)
    s2      = s2 - 10^(num.w * (b - a) / n) end
  return s1 / n < s2 / n end

function Data:dominates()
  for _,r1 in pairs(self.rows) do
    for _,r2 in pairs(self.rows) do
      if self:dominate(r1, r2) then
	r1.dom = r1.dom + 1 end end end 
  table.sort(self.rows, 
             function (x,y) return x.dom > y.dom end)
  for i=1,#rows*The.data.best do
    self.rows[i].best = true end end
	   
-------------------------------------------------
-- ## Test Stuff
function autoOkay()      dataOkay("auto") end
function auto10KOkay()   dataOkay("auto10K") end
function auto1000KOkay() dataOkay("auto1000K") end
function weatherOkay()   
  local d = dataOkay("weather") 
  assert( close( d.all.syms[1]:ent(),  1.58, 1) ) 
  assert( close( d.all.syms[2]:ent(),  0.98, 1) )  
  assert( close( d.all.syms[3]:ent(),  0.94, 1) )  
  assert( close( d.all.nums[1].mu,    73.57, 1) )
  assert( close( d.all.nums[1]:sd(),   6.57, 1) )  end

function dataOkay(f)
  roguesOkay()
  return Data:new():csv("../../data/".. f .. ".csv") end

function domOkay()
  local d = dataOkay("auto")
  local n = #d.rows
  d:dominates() 
  hi = #d.rows
  for i=1,10     do print(i, join(d.rows[i].cells)) end
  for i=hi-10,hi do print(i, join(d.rows[i].cells)) end
end
-------------------------------------------------
-- ## Main Stuff

main{data=domOkay}
