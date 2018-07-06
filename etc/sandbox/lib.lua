require "the"

-------------------------------------------------------------
-- ## Misc  Stuff 

int   = math.floor
printf= function (s, ...) return io.write(s:format(...)) end
match = function (s,p)    return string.match(s,p) ~= nil end

-------------------------------------------------------------
-- ## String  Stuff

-- ### rep(s: string, n: int)
-- Repeat a string, n times
function rep(s, n) return n > 0 and s .. rep(s, n-1) or "" end

-- ### sub(s: string, [lo : int], [hi : int])
-- Print substrings. Allow Python style negative indexes
function sub(s,lo,hi) 
  if lo and lo < 0 then
    return sub(s, string.len(s) + lo +1)
  else
    return string.sub(s,lo and lo or 1,hi) end end

function subOkay()
  assert(sub("timm")=="timm")
  assert(sub("timm",2)=="imm")
  assert(sub("timm",2,3)=="im")
  assert(sub("timm",-1)=="m")
  assert(sub("aa",3,10)=="")
end

-- ### oo(x : anything)
-- Print anything, including nested things
function oo(data) 
  local function go(x,       str,sep)  -- convert anything to a string
     if type(x) ~= "table" then 
       return tostring(x)  end
     for i, v in pairs(x) do 
        str = str .. sep .. i .. ": " .. go(v,"{","")
        sep = ", "
     end 
     return str .. '}'
  end 
  print(go(data,"{","")) end  

-------------------------------------------------------------
-- ## Meta  Stuff

-- ## rogesOkay()
-- Checked for escaped local. Report number of assertion failures.
function roguesOkay()
  local ignore = {
           math=true, package=true, table=true, coroutine=true, 
           os=true, io=true, bit32=true, string=true,
           arg=true, debug=true, _VERSION=true, _G=true }
  for k,v in pairs( _G ) do
    if type(v) ~= "function" and not ignore[k] then
       assert(match(k,"^[A-Z]"),"rogue local "..k) end end end

-------------------------------------------------------------
-- ## Unit Test  Stuff

-- ### tests()
-- Run any function ending in "Ok". Report number of failures.
function tests()
  local try,fail=0,0
  local function go(goal)
    for k,f in pairs( _G ) do
      if type(f) == "function" and match(k,goal .. "$") then
        print("-- Test",k .. "?")
        The=defaults()
        try = try + 1
        local passed,err = pcall(f)
        if not passed then 
          fail = fail + 1
          print("-- E> Failure: " .. err)  end end end end
   for _,v in pairs{"Okay", "OkaY", "OkAY", "OKAY"} do 
     go(v) end
   print("-- Failures: ".. 1-((try-fail)/try) .. "%") end


-------------------------------------------------------------
-- ## Object Stuff

-- ### Any:new(o)
-- Create the `any` base object

Any={id=0}
function Any:new (o)
  o = o or {}   -- create object if user does not provide one
  setmetatable(o, self)
  if not self.oid then self.oid=0 end
  self.oid = self.oid+1
  self.__index = self
  o.id = self.oid
  return o
end

function anyOkay()
  local x,y = Any:new(), Any:new()
  x.sub = y
  y.seb = Any:new()
  oo(x)
end


