require "lib"

Thing=Any:new{pos,txt, w=1, n=0}

function Thing:incs(t, f)
  f = f and f or function (z) return z end
  for _,v in pairs(t) do self:inc( f(v) ) end 
  return self
end

function Thing:inc(x)
   if x==The.ignore then return x end
   self.n = self.n + 1
   return self:inc1(x) end

function Thing:prep(x) return x end

function Thing:dec(x)
   if x==The.ignore then return x end
   if self.n < 3    then return x end
   self.n = self.n - 1
   return self:dec1(x) end

function Thing:simpler(i,j) 
  local  n = self.n
  return self.doubt() > The.ish*(i.doubt()*i.n/n + 
                                 j.doubt()*j.n/n) end

----------------------------------------
-- class Sym
Sym= Thing:new{counts={}, mode, most=0, _ent}

function Sym:doubt() return self:ent() end

function Sym:ent()
  if not self._ent then
    for _,v in pairs(self.counts) do
      p      = v/self.n
      i._ent = i._ent * p * math.log(p,2) end end
  return i._ent end

function Sym:inc1(x)
  self._ent= nil
  local old = self.count[x] 
  local new = old and old + 1 or 1
  if new > self.most then
    self.most, self.mode = new, x end end

function Sym:dec1(x)
  self._ent= nil
  i.counts[x] = i.counts - 1
  return x end

----------------------------------------
-- class Num
Num= Thing:new{lo=The.inf, hi=The.ninf, mu=0, m2=0} 

function Num:doubt() return self:sd() end

function Num:sd()
  return (self.m2/(self.n - 1 + The.zip))^0.5  end

function Num:inc1(x)
  local d = x - self.mu
  self.mu = self.mu + d/self.n
  self.m2 = self.m2 + d*(x - self.mu)
  if    x > self.hi then self.hi = x end
  if    x < self.lo then self.lo = x end
end

function Num:dec1(x)
  local d = x - self.mu
  self.mu = self.mu - d/self.n
  self.m2 = self.m2 - d*(x - self.mu)
end

function numOkay(    n) 
  n = Num:new()
  n:incs{4,10,15,38,54,57,62,83,100,100,174,190,215,225,
         233,250,260,270,299,300,306,333,350,375,443,475, 
         525,583,780,1000}
  assert(close(n.mu,   270.3,   0.001))
  assert(close(n:sd(), 231.946, 0.001))
  oo(n)
end

main{thing=numOkay}
