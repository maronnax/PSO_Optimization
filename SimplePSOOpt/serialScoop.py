#!/usr/bin/env python
import os, sys, re
from optparse import OptionParser
#import subprocess
import epopt

Nscoopdirs=0
specific_dir=-1
parser=OptionParser(description="usage: serialscoop.py x, where x is number dirs to work on")
parser.add_option("-i", dest="specific_dir", default=-1, type="int",
             help="scoop particular dir -i 5: scoop workdir 5")
(inp, args) = parser.parse_args()

print_args=False
if print_args:
  print inp
  if len(args) > 0:
    print "unparsed opt: ", args

dirList=[]
if len(args) == 0 and inp.specific_dir>-1:
  # looking in one specific dir
  dirList.append(epopt.rundirname(inp.specific_dir))
elif len(args) == 1:
  Nscoopdirs = int(args[0])
  if Nscoopdirs < 0:
    print "cannot have negative scoopdirs"
  for ir in range(Nscoopdirs):
    dirList.append(epopt.rundirname(ir))
else:
  print "usage: serialscoop.py x, where x is N dirs"
  exit(1)


done=False

for idir in dirList:
  print "   serially scooping directory:", idir
  
  if not os.path.isdir(idir):
    print "directory "+idir+" not there! ignore?"
    exit(1)
    
  os.chdir(idir)

  errfile = "./Results.txt"
  if not os.path.exists(errfile):
    print "did not find ", errfile
    exit(1)

  ERR = open(errfile, 'r')
  var = ERR.read()
  ERR.close()
  hlines=var.splitlines()
    
  os.chdir("..")

# however success is determined, this is one way to send info back to C++
success=True
if success:
  exit(0)
else:
  exit(1)

