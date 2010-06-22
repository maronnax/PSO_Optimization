#!/usr/bin/env python
import os, sys
import stat
#import subprocess

def epexecutable():
  return "/Users/noel/energyplus/v5src/ep"
  #return "/Users/noel/energyplus/mms/null.sh"
  #return "/global/homes/n/ndk/energyplus/src/ep"

def simple_executable():
  return "/Users/naddy/Work/Building_Optimization_Project_36601F/PSOOptimization/simple_parallel_pso/simpleExecutionScript.py"

def idfname(rank):
  return "../in.idf"

def epwname(rank):
  return "../in.epw"

def rundirname(rank):
  return "r%04d" % (rank)

def mayday(string1, string2='', string3='', string4=''):
  s="syut.mayday: %s %s %s %s" % (string1, string2, string3, string4)
  print s
  sys.exit(0)

def file_stmode(file):
  mode = os.stat(file)[stat.ST_MODE]
  return oct(mode & 0777)

def checkexe(exe):
  if not os.path.exists(exe):
    mayday("checkexe: os.path.exists says file not there (%s)" % exe)
  # i'm sure there is a better way to check if file is executable
  stmode = file_stmode(exe)
  if int(stmode) < 700:
    mayday("checkexe: file (%s) may not be executable stmode=%s" % (exe, stmode))
  return stmode
