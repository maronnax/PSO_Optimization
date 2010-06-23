#!/usr/bin/env python
import os, sys, re, time
import Particle
from random import uniform

#Classroom_Weekday_T1: 10.5
#Classroom_Weekday_T2: 0.25
#Classroom_Weekday_T3: 0.05
#Classroom_Weekday_T4: 14.0

# A list of the min/max values for each dimension of each particle.
# Note that this is also where I determine the number of dimensions.
#positionMinMaxList=[(0,100), (0,12), (-100,0)]
positionMinMaxList=[(-100,100), (-100, 100), (-100, 100), (-100, 100)]

#p=Particle.Particle(positionMinMaxList)
#print p

#r1=uniform(0, 1)
#r2=uniform(0, 1)
c1 = 2.0
c2 = 2.0
Cf = 0.5
kiterationMax=1000
Nparticles=5000
tbest_age = 0  # number of iterations with no new best overall particle

particleList=[]
for ip in range(Nparticles):
  p = Particle.Particle(positionMinMaxList, c1, c2, Cf)
  particleList.append(p)
  # print p

# where to store bestparticle data?  for now keep it here and pass into Particle class when needed
# first best particle
bestparticle = Particle.determineBestParticle(particleList)
#print "bestparticle=\n", bestparticle


for kiter in range(kiterationMax):
  print "-----------time step iteration kiter=%5d  best fit=%17.13f" % (kiter,  bestparticle.bestfitvalue)
  for particle in particleList:
    # update particle velocity    
    particle.updateVelocity(bestparticle)
    particle.updatePosition()
    #particle.updateVelocityMax_Inertia()
    fitvalue = particle.evaluateFitness()
    particle.updateBestFitnessValue(fitvalue)
    #print particle

  previous_bestparticle = bestparticle
  bestparticle = Particle.determineBestParticle(particleList)
  if (previous_bestparticle != bestparticle):
    tbest_age = 0
  else:
    tbest_age+=1
  #print "bestparticle=\n", bestparticle, " tbest_age=", tbest_age


print "bestparticle=\n", bestparticle, " tbest_age=", tbest_age
