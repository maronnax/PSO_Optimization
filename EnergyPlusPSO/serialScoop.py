#!/usr/bin/env python
import os, sys, re, pickle, pdb
from optparse import OptionParser
#import subprocess
import epopt
import Particle

# however success is determined, this is one way to send info back to C++
RETURNVALUE = 0 # Everythng fine, continue.
                # 1: Unknown error.
                # 2: Max iterations reached.
                # 3: Bestparticle is constant for max number times
                # 4: Best solution is constant for max number times 

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

print "Running SerialScrape with n = %s" % args[0]

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
  print "    Particle %d fitness = %f" % (len(pso_data.current_particle_results), value)
  pso_data.current_particle_results.append( value )
  # Set particle fiteness at the same time
  os.chdir("..")

# 
# Do central processing: deciding whether to end, possibly update the
# intertial constants on the particles, update the particle positons
# and velocities.
# 

updates_c1 = []
updates_c2 = []

if len(pso_data.current_particle_results) == len(pso_data.particle_list):

  pso_data.current_iteration += 1
  print "Iteration %d" % pso_data.current_iteration

  if pso_data.current_iteration % 50 == 0:
      # This is the part where we update some or all of the particle
      # intertia, c1 (fraction of attraction towards the best position
      # in param space this particle has seen), c2 (fraction of
      # attraction towards the best position any particle has ever
      # seen), Cf, which is the max_speed conversion factor.
    pso_data.Ns += 1

    old_inertia = pso_data.particle_list[0].w_inertia
    old_cf = 1.0 / (pso_data.Ns - 1)

    new_inertia = .9 * old_inertia
    new_cf = 1.0 / (pso_data.Ns)

    print "Updating Global Particle Swarm Parameters Cf w_intertia."
    print "(cf, w): (%.5f, %.5f) -> (%.5f, %.5f)" % (old_inertia, old_cf, new_inertia, new_cf)

    # Go through and update each particle's inertia, 
    for particle in pso_data.particle_list:
      # Update the particle's intertia
      particle.w_inertia = .9 * particle.w_inertia

      Cf = 1.0 / pso_data.Ns 
      for dim in xrange(particle.Ndimensions):
        minp, maxp = particle.positionMinMaxList[dim]
        particle.velocityMax[dim] = Cf * (maxp - minp)

  if pso_data.current_iteration >= pso_data.max_iterations:
    RETURNVALUE = 2 # Codes seem kinda lame here

  print "Updating particle velocities and positions."
  # Update each of the particles with the record of how it's done.
  for ndx, res in enumerate(pso_data.current_particle_results):
    pso_data.particle_list[ndx].setFitness( res )

  bestparticle = Particle.determineBestParticle(pso_data.particle_list)

  print "Updated Positions:"
  for p_ndx, particle in enumerate(pso_data.particle_list):

    print "Particle %d Pre: \n\tPosition - %s, \n\tVelocity - %s" % (p_ndx, particle.position, particle.velocity)
    particle.updateVelocity(bestparticle)
    particle.updatePosition()
    print "Particle %d Post: \n\tPosition - %s, \n\tVelocity - %s" % (p_ndx, particle.position, particle.velocity)

  
  epopt.appendParticlePositionsToDisk( pso_data.OutputFile, pso_data.current_iteration, pso_data.particle_list)    
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
    
print "End serial scrape"


if RETURNVALUE == 2:
  print "Maximum simulation iterations (%d) reached.  Ending PSO simulation." \
      % pso_data.max_iterations
elif RETURNVALUE == 3:
  print "Convergence criterion reached: best particle constant for over %d iterations.  Ending PSO simulation" \
      % pso_data.max_constant_iterations
elif RETURNVALUE == 4:
  print "Convergence criterion reached: best solution constant for over %d iterations.  Ending PSO simulation" \
      % pso_data.max_constant_iterations

exit( RETURNVALUE )
