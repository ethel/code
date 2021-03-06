from cli import option,options
import random

THE = options(
"""
ETHEL v0.1.0 multi-objective rule generator
(c) 2018: Tim Menzies timm@ieee.org, BSD 2-Clause License
""",
"""
Copyright (c) 2018, Tim Menzies
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
  ["general",
      option("start up action",                         act= ""),
      option("random number seed",                      seed= 1),
      option("define small change",                     cohen= [0.2, 0.1,0.3,0.5]),
      option("input data svs file",                     data= "data/auto.csv"),
      option("trace all calls",                         verbose= False),
      option("decimals to display floats",              decimals= 3),
      option("list unit tests",                         tests= False),
      option("run unit tests",                          check= False)
  ],["top-down clustering",
      option("min bin size = max(few, N^power)",        few= 10),
      option("min bin size = max(few, N^power)",        power= 0.5),
      option("enable heuristic comination",             speed= False),
      option("in speed mode, min distance for retries", trivial= 0.05)
  ],["bottom-up pruning",
      option("doubt reduction must be over x*unboubt",  undoubt= 1.1)
  ],["rule generation",
      option("min support for acceptable rules",        least= 20),
      option("build rules from top 'elite' ranges",     elite= 10)
  ]
)  

random.seed(THE.seed)
