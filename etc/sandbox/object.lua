-- /* vim: set ts=2 sw=2 sts=2 expandtab: */

require "config"
requure "tricks"

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
  print(go(data,"{",""))
end

function rogues()
  for k,v in ipairs(_G) do
    if type(v) ~= "function" then 
      if not match(sub(k,1,2),'[A-Z][A-Z]*') then
        print("rogue " .. k) end end end        
----------------------
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

oo(Any:new())
oo(Any:new())
x=Any:new()
x.y=Any:new()
oo(x)

rogues()
Thing=Any:new()

function Account:withdraw (v)
      if v > self.balance then error"insufficient funds" end
      self.balance = self.balance - v
    end

