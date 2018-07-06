require "config"

-- Some shortcuts 
int   = math.floor
printf= function (s, ...) return io.write(s:format(...)) end
match = function (s,p)    return string.match(s,p) ~= nil end

-- Repeat a string, n times
function rep(s, n) return n > 0 and s .. rep(s, n-1) or "" end

-- Print substrings. Allow Python style negative indexes
function sub(s,lo,hi) 
  if lo and lo < 0 then
    return sub(s, string.len(s) + lo +1)
  else
    return string.sub(s,lo and lo or 1,hi) end end

function subOk()
  assert(sub("timm")=="timm")
  assert(sub("timm",2)=="imm")
  assert(sub("timm",2,3)=="im")
  assert(sub("timm",-1)=="m")
  assert(sub("aa",3,10)=="")
end

-- Print anything, including nested things
function oo(data) 
  local function go(data,       str,sep)  -- convert anything to a string
     if type(data) ~= "table" then 
       return tostring(data) 
     else for i, v in pairs(data) do 
        str = str .. sep .. i .. ": " .. go(v,"{","")
        sep = ", "
     end 
     return str .. '}'
  end
  print(go(data,"{","")) end end 

-- Checked for escaped local. Report number of assertion failures.
function roguesOk()
  local ignore = {
           math=true, package=true, table=true, coroutine=true, 
           os=true, io=true, bit32=true, string=true,
           arg=true, debug=true, _VERSION=true, _G=true }
  for k,v in pairs( _G ) do
    if type(v) ~= "function" and not ignore[k] then
       assert(match(k,"^[A-Z]"),"rogue local "..k) end end end

-- Run any function ending in "Ok". Report number of failures.
function tests()
  local try,fail,head=0,0,"\n"..rep("-",40).."\n"
  for k,f in pairs( _G ) do
    if type(f) == "function" and match(k,"Ok$") then
      print(head.."-- Test",k .. "?")
      local t0=os.clock()
      The=defaults()
      try = try + 1
      local passed,err = pcall(f)
      if passed then
        printf("-- passed in %.3f secs\n",os.clock() - t0)
      else
        fail = fail + 1
        print("-- E> Failure: " .. err)  end end end  
   print(head.."-- Failures: ".. 1-((try-fail)/try) .. "%") end

-- Set up base object
OID=0
Any={id=0}
function Any:new (o)
  o = o or {}   -- create object if user does not provide one
  setmetatable(o, self)
  self.__index = self
  OID=OID+1
  o.id = OID
  return o
end

