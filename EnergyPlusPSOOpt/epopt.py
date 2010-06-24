#!/usr/bin/env python
import os, sys
import stat
#import subprocess

def appendColumnDataToDisk( filename, column_headers ):
  FILE = open(filename, 'a')
  
  
  str = ",".join(column_headers)
  FILE.write("ParticleNdx,Iter,")
  FILE.write(str)
  FILE.write('\n')
  FILE.close()
  return 

def appendParticlePositionsToDisk( filename, iteration, particle_list ):
  FILE = open(filename, 'a')
  for part_ndx, particle in enumerate(particle_list):
    header = "%d,%d," % (part_ndx, iteration)
    FILE.write(header)
    position = ",".join(["%f" % p_d for p_d in particle.position])
    FILE.write(position)
    FILE.write('\n')
  else:
    FILE.close()
  
  return 
    

def epexecutable():
  return "/Users/noel/energyplus/v5src/ep"
  #return "/Users/noel/energyplus/mms/null.sh"
  #return "/global/homes/n/ndk/energyplus/src/ep"

def simple_executable():
  return "./simpleExecutionScript.py"

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

def checkfile(file):
  if not os.path.exists(file):
    mayday("checkexe: os.path.exists says file not there (%s)" % file)
  return file_stmode(file)

def checkexe(exe):
  if not os.path.exists(exe):
    mayday("checkexe: os.path.exists says file not there (%s)" % exe)
  # i'm sure there is a better way to check if file is executable
  stmode = file_stmode(exe)
  if int(stmode) < 700:
    mayday("checkexe: file (%s) may not be executable stmode=%s" % (exe, stmode))
  return stmode

class NullObject( object ): pass
