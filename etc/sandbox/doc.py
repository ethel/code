from ethel import *
import contextlib

def globs():
  header=""
  headers=[]
  lines=[]
  for k,v in globals().items():
     if callable(v):
         if str(v.__module__) != header:
           if v.__module__:
            if v.__module__ not in  ["contextlib","__main__"]:
             header=v.__module__
             lines += [["\n_______\n\n#<a name=\"",header,"\">",header,"</a>\n"]]
             headers += [header]
         if v.__doc__:
              doc = v.__doc__
              doc = re.sub(r'\n[ \t]*', "\n", doc)
              lines += [["\n## ",k,"\n\n",doc,"\n"]]
  for h in headers:
    print(h)
  for line in lines:
    print(*line,sep="")

globs()
