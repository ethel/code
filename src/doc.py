from ethel import *

def globs():
  header=""
  for k,v in globals().items():
     if callable(v):
         if str(v.__module__) != header:
             header=v.__module__
             print("\n#",header,"\n")
         if v.__doc__:
              print("\n## ",k,"\n\n",v.__doc__,"\n",sep="")

globs()
