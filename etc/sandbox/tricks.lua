require "the"
require "lib"

Thing=Any:new()

function Thing:withdraw (v)
      if v > self.balance then error"insufficient funds" end
      self.balance = self.balance - v
end

tests()
