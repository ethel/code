#!/usr/bin/env python3
import os , re, sys, time
from random import random as r, choice as any
from contextlib import contextmanager
from oks import ok
from lib import *
from config import THE
from obj import o
from tree import *
from data import csv
from things import Thing, Num, Sym
from tables import Table, table

#class Range(object):
#  def __init__(i, col, name, rows, lo, hi=None):
#    if hi == None: hi = lo
#    i.col,i.name,i.rows,i.lo,i.hi = col,name,rows,lo,hi

# sdsa

if __name__ == '__main__':   
  if THE.tests:
    ok(show=True)
  elif THE.main:
    ok(act=THE.main)
  else:
    ok() if THE.check else print(help()[0])

