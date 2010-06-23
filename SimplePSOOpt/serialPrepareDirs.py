#!/usr/bin/env python
import os, sys
from optparse import OptionParser
#import subprocess
import epopt

# initial directory prepare (should run this before submitting parallel job)

parser=OptionParser(description="usage: serialPrepareDirs.py x, where x is Nranks ")
#parser.add_option("-p", dest="Nprepare_dirs", default=0, type="int",
#             help="prepare dirs only.  -p N, to prepare N directories")
(inp, args) = parser.parse_args()

#print_args=True
#if print_args:
#  print inp
#  if len(args) > 0:
#    print "unparsed opt: ", args

if len(args) == 1:
  Nranks = int(args[0])
  if Nranks < 0:
    print "usage: serialPrepareDirs.py x, where x is rank number, cannot be negative"
else:
  print "usage: serialPrepareDirs.py x, where x is rank number"
  exit(0)

# various other checks
#if not os.path.exists(epopt.idfname(ir)):
epopt.checkexe(epopt.simple_executable())
epopt.checkexe("./parallelEPrun.py")
epopt.checkexe("./serialScoop.py")
epopt.checkexe("./a.out")  # the simple C++ executable

  
for ir in range(Nranks):
  dir = epopt.rundirname(ir)
  print dir

  # make dir if not there
  if not os.path.isdir(dir):
    os.system("mkdir -p "+dir)

  os.chdir(dir)
  #os.system("cp "+executable()+" .")
  os.system("ln -fs " + epopt.simple_executable() + " ./ss")

  # this is where you could change the idf file in each directory
  # os.system("cp "+epopt.idfname(ir)+" .")

  #os.system("cp "+epopt.epwname(ir)+" .")
  # os.system("ln -fs "+epopt.epwname(ir)+" .")

  #os.system("cp ../Energy+.idd .")
  # os.system("ln -fs ../Energy+.idd .")
  os.chdir("..")

  #franksh = "go%04d.sh" % i
  #OUT = open(franksh, 'w')
  #OUT.write("set -x\n")
  #OUT.write("cd r%04d\n" % i)
  #OUT.write("pwd\n")
  #OUT.write("./a.out > out\n")
  #OUT.close()
  #os.system("chmod 755 "+franksh)

