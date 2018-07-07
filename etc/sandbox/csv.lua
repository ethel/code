require "thing"

-------------------------------------------------------
-- ### rows(file: string)
-- Iterator. Kills comments, white space. If any line ends in `,`,
-- then we join it to the next one. Resulting lines
-- are then split on `,` and cells are converted to
-- strings or numbers as appropriate. 
-- Note that if the first row marks tha a column 
-- is to be ignored
-- (by have a column name containing `?`) then 
-- all such columns are ignored. The result
-- non-ignored rows of cells are returns, one at a time. 

function rows(file)
  io.input(file)
  local use, cache, todo = {}, {}, io.read()
  local need= function (s) return not string.find(s,"?") end
  return function ()
    if todo then
      local line= todo:gsub("[\t\r ]*",""):gsub("#.*","")
      todo= io.read()
      cache[#cache+1]= line
      if sub(line,-1) ~= ","  then
	local txt = table.concat(cache)
        print("[" ..txt.. "]")
	if string.len(txt)>0  then
          cache= {}
          local a,b = split(txt), {}
          if #use == 0 then -- find cols marked not unwanted
            for i = 1,#a do
              if need(a[i]) then use[#use+1]= i end end end
	  for i=1,#use do
            b[#b+1] = fromString( a[ use[i] ] ) end
	  return b  end end
    else
      io.input():close() 
      return nil  end end end

for row in rows("../../data/weather.csv") do
   oo(row)
end
