#Particle.py

from random import uniform
import math, pdb

from math import sin, sqrt

class Particle:
  def __init__(self, positionMinMaxList, c1, c2, Cf):

    self.positionMinMaxList=positionMinMaxList
    self.Ndimensions = len(positionMinMaxList)

    self.Cf = Cf
    self.c1 = c1
    self.c2 = c2

    # missing the dynamic reduction parameters (kappa, d, wd)
    #self.dynamicD = 10
    #self.kappa = 1
    self.w_inertia = 1.0
    self.age = 0 # how many iterations since a better position
    
    self.position=[]  # list of positions
    self.bestposition=[]  # list of best positions of all time
    self.velocity=[]  # list of velocities
    self.velocityMax = [] # list of maximum velocities. 

    for minp,maxp in positionMinMaxList:
      rp = uniform(minp,maxp)
      self.position.append(rp)

      velocityMax = Cf*(maxp-minp) 
      self.velocity.append(uniform(0,velocityMax))
      self.velocityMax.append(velocityMax)

    else:
      self.bestposition = self.position[:]

    self.fitvalue = 1e10 # Set with a very high number
    self.bestfitvalue = self.fitvalue  # initialize with first one

  # update velocity based on Eq 2 in paper
  def updateVelocity(self, bestparticle):    # pass in bestparticle
    # use temporaries to make final equation easier to read
    c1 = self.c1
    c2 = self.c2

    # Is this what we want?
    r1 = uniform(0,1) # random value between 0 and 1
    r2 = uniform(0,1) # random value between 0 and 1
    w = self.w_inertia

    for i in range(self.Ndimensions):
      vi = self.velocity[i] # velocity at dimension i
      xi  = self.position[i] # position at dimension i
      bxi = self.bestposition[i] # best position at dimension i
      bxg = bestparticle.bestposition[i] # best position of best particle at dimension i (from outside scope)
      self.velocity[i] = w*vi + c1*r1*(bxi - xi) + c2*r2*(bxg - xi)

      if abs(self.velocity[i]) > self.velocityMax[i]:
        # This gives us a self.velocityMax[i] with the same sign as self.velocity[i]
        self.velocity[i] = math.copysign(self.velocityMax[i], self.velocity[i])

  # update position based on Eq 1 in paper
  def updatePosition(self):
    for i in range(self.Ndimensions):
      self.position[i] = self.position[i] + self.velocity[i]
      minp,maxp = self.positionMinMaxList[i]

      # This is a new reflective scheme.  For now, we're only
      # reflecting the velocity.  This is so we will have a better
      # than average view into the behavior on the boundry of
      # parameter space, but could be changed later.
      if self.position[i] < minp: 
        self.position[i]=minp
        self.velocity[i] = self.w_inertia**2 * (-self.velocity[i])
      if self.position[i] > maxp: 
        self.position[i]=maxp
        self.velocity[i] = self.w_inertia**2 * (-self.velocity[i])

  # Update these velocity parameters.  
  def updateVelocityMax_Inertia(self, w_intertia, Cf, c1, c2):
    self.w_intertia = w_intertia
    self.Cf = Cf
    self.c1 = c1
    self.c2 = c2
    return 

  # Update the fitness.  This is assumed to be associated with the
  # current position for the purposed of updating the
  # bestFitnessValue.
  def setFitness(self, value):
    self.fitvalue = value
    self.updateBestFitnessValue(self.fitvalue)
    return 

  # decide if best fitness value & bestpositions need to be updated (currently looking for minimum value)
  def updateBestFitnessValue(self, fitvalue):
    self.fitvalue = fitvalue
    if (self.fitvalue < self.bestfitvalue):
      self.age=0
      self.bestfitvalue = self.fitvalue
      for i in range(self.Ndimensions):
        self.bestposition[i] = self.position[i]
    else:
      self.age = self.age + 1
          
  def __str__(self):
    s=""
    for i in range(len(self.positionMinMaxList)):
      s+="%2d pos=%7.2f vel=%7.2f bestpos=%7.2f\n" % \
          (i, self.position[i], self.velocity[i], self.bestposition[i])
    s+="fitvalue=%7.2f  bestfitvalue=%8.2f  age=%3d" % (self.fitvalue, self.bestfitvalue, self.age)
    return s


# global function -- not in Particle class
def determineBestParticle(particleList):
  if len(particleList) < 1:
    print "Error, particle list is 0!"
  bestparticle=particleList[0]  # first one
  for p in particleList:
    if p.bestfitvalue < bestparticle.bestfitvalue:
      bestparticle=p
  return bestparticle


