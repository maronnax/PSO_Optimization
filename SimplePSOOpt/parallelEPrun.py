#!/usr/bin/env python
import os, sys, pdb
from optparse import OptionParser
#import subprocess
import epopt

parser=OptionParser(description="usage: parallelEPrun.py x, where x is rank number")
#parser.add_option("-p", dest="Nprepare_dirs", default=0, type="int",
#             help="prepare dirs only.  -p N, to prepare N directories")
(inp, args) = parser.parse_args()

print_args=False
if print_args:
  print inp
  if len(args) > 0:
    print "unparsed opt: ", args

if len(args) == 1:
  rank = int(args[0])
  if rank < 0:
    print "usage: parallelEPrun.py x, where x is rank number, cannot be negative"
else:
  print "usage: parallelEPrun.py x, where x is rank number"
  exit(0)

# run for each rank
dir = epopt.rundirname(rank)
os.chdir(dir) 

print "  running parallelEPrun.py in dir="+os.getcwd()

# might keep this command fixed, and have prepareDirs always link/copy a ./ep in here

os.system("python ./ss >& Results.txt")

os.chdir("..")

