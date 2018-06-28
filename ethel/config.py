from cli import elp,options
import random

def help(): return [
"""ETHEL v0.1.0 multi-objective rule generator
(c) 2018: Tim Menzies timm@ieee.org, MIT license, v2""",
"""
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
  ["general",
      elp("start up action",                         main= ""),
      elp("random number seed",                      seed= 1),
      elp("define small change",                     cohen= [0.2, 0.1,0.3,0.5]),
      elp("input data svs file",                     data= "data/auto.csv"),
      elp("trace all calls",                         verbose= False),
      elp("decimals to display floats",              decimals= 3),
      elp("list unit tests",                         tests= False),
      elp("run unit tests",                          check= False)
  ],["top-down clustering",
      elp("min bin size = max(few, N^power)",        few= 10),
      elp("min bin size = max(few, N^power)",        power= 0.5),
      elp("enable heuristic comination",             speed= False),
      elp("in speed mode, min distance for retries", trivial= 0.05)
  ],["bottom-up pruning",
      elp("doubt reduction must be over x*unboubt",  undoubt= 1.05)
  ],["rule generation",
      elp("min supprot for acceptable rules",        least= 20),
      elp("build rules from top 'elite' ranges",     elite= 10)
  ]]

THE = options(*help())
random.seed(THE.seed)


