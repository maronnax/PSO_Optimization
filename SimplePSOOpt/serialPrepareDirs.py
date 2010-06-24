#!/usr/bin/env python
import os, sys, pickle, pdb
from optparse import OptionParser
import PSO
import Particle
from random import uniform
#import subprocess
import epopt

#
# Global variables.  I should externalize these into some kind of file
# somewhere.
# 

class NullObject(object): pass

def parseInputSpecificationFile( filename ):

  param_parsing_mode = False

  run_parameters = {}
  optimization_parameters = {}

  spec_file = open(filename)
  for line in spec_file.xreadlines():

    if line.startswith("Parameters:"):
      param_parsing_mode = True
      continue
    elif line.strip() == "":
      continue

    name, value = line.split(':')
    name, value = name.strip(), value.strip()
    
    if param_parsing_mode:
      lower_bound, upper_bound = value.split(",")
      lower_bound, upper_bound = float(lower_bound), float(upper_bound)
      optimization_parameters[name] = (lower_bound, upper_bound)
    else:
      if name == "NumParticles":
        run_parameters["NumParticles"] = int(value)
      elif name == "MaxIterations":
        run_parameters["MaxIterations"] = int(value)
      elif name == "MaxConstantIterations":
        run_parameters["MaxConstantIterations"] = int(value)
      else:
        print "Unknown run parameter '%s' in input file." % name
        exit(0)
  else:
    spec_file.close()
    
  return run_parameters, optimization_parameters

def loadPickleFromFilename(filename):
  file = open(filename, 'r')
  data = pickle.load( file )
  return data

def pickleToFilename(data, filename):
  file = open(filename, 'w')
  pickle.dump(pso_data, file)
  return 

#
# Noel's Parallel Code: 
# Make sure executables are present and prepare the N directories to
# be run.
#

# initial directory prepare (should run this before submitting parallel job)
parser=OptionParser(description="usage: serialPrepareDirs.py x, where x is Nranks ")
parser.add_option("-i", dest = "input_file", default = "INPUT_SPECIFICATION.IN", type="string", \
                    help="Specify an initialization file to use.")

(inp, args) = parser.parse_args()
input_file = inp.input_file

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
epopt.checkexe("./serialFinalize.py")
epopt.checkexe("./a.out")  # the simple C++ executable

# 
# SimplePSOOpt Specific stuff.
# 
epopt.checkfile(input_file)
  
for ir in range(Nranks):
  dir = epopt.rundirname(ir)
  print dir

  # make dir if not there
  if not os.path.isdir(dir):
    os.system("mkdir -p "+dir)

  os.chdir(dir)
  os.system("ln -fs ../" + epopt.simple_executable() + " ss")
  os.chdir("..")

run_params, parameters = parseInputSpecificationFile( input_file )

NParticles = run_params["NumParticles"]
NIterations = run_params["MaxIterations"]
NConstantIterations = run_params["MaxConstantIterations"]

# Initial values for velocity updating params.  
c1 = 2.0
c2 = 2.0
Cf = 0.2 # Max speed of the particle in any particular dimension is 
         # Cf * (param_range_max - param_range_min) in that dimension.


# Because all the PSO data has to be stored/retrieved from disc every
# time serialScoopDirs.py is called, I am putting it all in one big
# "anonymous" object.  This could be improved by storing it to two or
# more files, so that for the vast majority of serial scoop, only a
# small number of data is serialized to/from the disk. 

canonical_keys = parameters.keys()[:]
positionMinMaxList = [parameters[k] for k in canonical_keys]

pso_data = NullObject()

pso_data.Ns = 5.0 # Paramaters for the dynamic inertia components 
pso_data.wi = 1.0 # Paramaters for the dynamic inertia components 
pso_data.Nranks = Nranks
pso_data.current_iteration = 0
pso_data.max_iterations = NIterations
pso_data.max_constant_iterations = NConstantIterations

pso_data.parameter_ranges = parameters

# This is probably redundant, but because everything is being
# serialized so much, I want to make sure I have a "canonical" keys.
pso_data.canonical_parameters  = canonical_keys

# The actual particles, which hold their current position, current
# velocity, c1, c2, cF, and the best position they have ever seen.
pso_data.particle_list = \
    [Particle.Particle(positionMinMaxList, c1, c2, Cf) \
       for ip in range(NParticles)] 
pso_data.current_particle_results = [] # A cache for the scores for the current iteration
pso_data.best_particle = pso_data.particle_list[0]  # The best particle overall.

# Set up the next first pass of optimizations
# Set up simulations from pso.data.currentParticleNdx ... pso.data.currentParticleNdx
for sim_setup_ndx in xrange(pso_data.Nranks):

  particle = pso_data.particle_list[sim_setup_ndx] # Copy by reference.
  parameter_vals = particle.position[:]
  
  rank_dir = epopt.rundirname(sim_setup_ndx)

  filename = os.path.join(rank_dir, "Params.txt")
  params_file = open(filename, 'w')

  for ndx in xrange(len(parameter_vals)):
    line = "%s:\t%f\n" % (pso_data.canonical_parameters[ndx], parameter_vals[ndx])
    params_file.write(line)
  else:
    params_file.close()
    
pickleToFilename( pso_data, "Particle.Dat")



