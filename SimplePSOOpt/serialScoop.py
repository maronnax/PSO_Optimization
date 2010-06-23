#!/usr/bin/env python
import os, sys, re, pickle, pdb
from optparse import OptionParser
#import subprocess
import epopt
import Particle

class NullObject(object): pass

def loadPickleFromFilename(filename):
  file = open(filename, 'r')
  data = pickle.load( file )
  return data

def pickleToFilename(data, filename):
  file = open(filename, 'w')
  pickle.dump(pso_data, file)
  return 

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


pso_data = loadPickleFromFilename("Particle.Dat")

# 
# Scoop all the data from each of the directories
#

for dir_ndx, idir in enumerate(dirList):
  print "   serially scooping results in directory:", idir
  
  if not os.path.isdir(idir):
    print "directory "+idir+" not there! ignore?"
    exit(1)
    
  os.chdir(idir)

  output_file = "./Results.txt"

  if not os.path.exists(output_file):
    print "did not find ", output_file
    exit(1)

  lines = open(output_file, 'r').readlines()

  print "Checking Results for directory %d.... " % dir_ndx
  if not lines[0].startswith("0"):
    # This is a no op and, for the moment, we assume this is natural,
    # and not because of an error, so we break.
    print "NOOP, Breaking loop."
    os.chdir("..")
    break

  value = float(lines[1])
  print "    Particle %d value = %.3f" % (len(pso_data.current_particle_results), value)
  pso_data.current_particle_results.append( value )
  # Set particle fiteness at the same time
  os.chdir("..")

# 
# Do central processing: deciding whether to end, possibly update the
# intertial constants on the particles, update the particle positons
# and velocities.
# 

if len(pso_data.current_particle_results) == len(pso_data.particle_list):

  print "Done with an iteration"

  print "Updating particle velocities and positions."
  # Update each of the particles with the record of how it's done.
  for ndx, res in enumerate(pso_data.current_particle_results):
    pso_data.particle_list[ndx].setFitness( res )

  bestparticle = Particle.determineBestParticle(pso_data.particle_list)

  print "Updated Positions:"
  for p_ndx, particle in enumerate(pso_data.particle_list):
    particle.updateVelocity(bestparticle)
    particle.updatePosition()

    print "Particle %d: \n\tPosition - %s, \nt\tVelocity - %s" % (p_ndx, particle.position, particle.velocity)

  pso_data.current_particle_results = []

# 
# pso is in the correct state, so we prepare a file of results to
# determine whether or not things are correct.
#

current_optimization_offset = len(pso_data.current_particle_results)
# Seed directories 

for rank_ndx in xrange(pso_data.Nranks):
  # If it current_optimization_offset + rank_ndx corresponds to a
  # particle, write that data to the directory, otherwise, write a
  # noop.
  filename = os.path.join( epopt.rundirname(rank_ndx), "Params.txt")
  INPUT_FILE = open(filename, 'w')

  if current_optimization_offset + rank_ndx >= len(pso_data.particle_list):
    INPUT_FILE.write("NOOP\n")
    print "   Writing NOOP into directory %d" % rank_ndx
    INPUT_FILE.close()
  else:

    print "   Writing particle %d into directory %d" % \
        (current_optimization_offset + rank_ndx, rank_ndx)
                                                          
    particle = pso_data.particle_list[current_optimization_offset + rank_ndx]
    parameter_vals = particle.position[:]
    for ndx in xrange(len(parameter_vals)):
      line = "%s:\t%f\n" % (pso_data.canonical_parameters[ndx], parameter_vals[ndx])
      INPUT_FILE.write(line)
    else:
      INPUT_FILE.close()

pickleToFilename( pso_data, "Particle.Dat")
    
# however success is determined, this is one way to send info back to C++
success=True
if success:
  exit(0)
else:
  exit(1)
