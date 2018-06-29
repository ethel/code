# command line interface shortcuts

import argparse

def option(h, **d):
  def elp1():
    if val is False :
          return dict(help=h, action="store_true")
    elif isinstance(val,list):
          return dict(help=h+(";e.g. %s" % val[0]), choices=val,          
                      default=default, metavar=m ,type=t)
    else: 
          return dict(help=h + ("; e.g. %s" % val), 
                      default=default, metavar=m, type=t)
  key,val = list(d.items())[0]
  default = val[0] if isinstance(val,list) else val
  m,t = "S",str
  if isinstance(default,int)  : m,t= "I",int
  if isinstance(default,float): m,t= "F",float
  return  key, elp1()

def options(before, after, *lst):
  parser = argparse.ArgumentParser(epilog=after, description = before, 
                                   add_help=False,
              formatter_class = argparse.RawDescriptionHelpFormatter)
  seen=["h"]
  for group in lst:
      sub = parser.add_argument_group(group[0])
      for key, rest in group[1:]:
        flag = key[0]
        if flag in seen:
           sub.add_argument("--"+key,**rest)
        else:
           sub.add_argument("-" + flag, "--"+key,**rest)
           seen += [flag]
      if group[0]=="general":
        sub.add_argument("-h", "--help", action="help", 
                          help="show this help message and exit")
  tmp=  parser.parse_args()
  tmp.HELLO, tmp.COPYRIGHT= before, after
  return tmp


