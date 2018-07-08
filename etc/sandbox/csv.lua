require "thing"

-------------------------------------------------------
-- ### csv(file: string)
-- Iterator. Kills comments, white space. If any line ends in `,`,
-- then we join it to the next one. Resulting lines
-- are then split on `,` and cells are converted to
-- strings or numbers as appropriate. 
-- Note that if the first row marks tha a column 
-- is to be ignored
-- (by have a column name containing `?`) then 
-- all such columns are ignored. The result
-- non-ignored rows of cells are returns, one at a time. 
function csv(file)
  io.input(file)
  local use, cache, todo = {}, {}, io.read()
  return function ()
    while todo do
      local txt = todo:gsub("[\t\r ]*","") -- no spaces
                      :gsub("#.*","") -- no comments
      todo = io.read()
      cache[ #cache+1 ] = txt -- accumulate lines until...
      if sub(txt,-1) ~= ","  then -- ... until end of row
        local txts = table.concat(cache)
        if string.len(txts) > 0 then -- non-empty lines
          cache, row, cells = {}, {}, split(txts)
          if #use==0 then -- this is our first loop
	    for i= 1,#cells do -- so get the columns we want
              if not string.find( cells[i], "?" ) 
	        then use[ #use+1 ] = i end end end
          for i= 1,#use do -- grab the columns we want
            row[ #row+1 ] = scan( cells[use[i]] ) end
          return row end end end end end 
          
function csvOkay()
  for row in csv("../../data/weather.csv") do
     print(table.concat(row,", ")) end end

main{csv=csvOkay}
