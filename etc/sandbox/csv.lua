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
  local cache,want,nextLine = {},nil,io.read()
    
  local function wantedCells(t,out)
    if not want then -- find cols marked as not unwanted
      want={}
      for source = 1,#t do
         if not string.find(t[source],"?") then 
           want[#want+1] = source end end 
    for i=1,#want do
      out[ #out+1 ] = fromString( t[ want[i] ] ) end
    return out end
  
  return function ()
    while nextLine do
      local line = nextLine:gsub("[\t\r ]*",""):gsub("#.*","")
      cache[#cache+1] = line
      nextLine = io.read()
      if sub(line,-1) ~= ","  then
	 local lines = table.concat(cache)
	 if string.len(lines)>0  then
           cache= {}
	   return wantedCells(split(lines), {})  end end end end  end

Data=Any:new{}

for row in rows("../../data/weather.csv") do
   print(table.concat(row,", "))
end
