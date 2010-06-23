#Particle.py

from random import uniform
import math, pdb

from math import sin, sqrt

def func2(particle):
  sum=0.0
  for i in range(particle.Ndimensions):
    sum += particle.position[i]* particle.position[i]
  avg = math.sin(sum/float(particle.Ndimensions))
  return avg

def func(particle):
  sum=0.0

  for i in range(particle.Ndimensions):
    sum += particle.position[i]
  avg = sum/float(particle.Ndimensions)
  val = math.cos(avg) * math.exp(math.sin(avg)) * math.sin(avg)  / 1.5
  return val

def func( particle ):
  
  alpha = 3.0

  x = particle.position[0]
  y = particle.position[1]
  z = particle.position[2]
  a = particle.position[3]

  return (x**2 + y**2 + z**2 + a**2) * 0.25 * (2 + alpha * sin(sqrt(x**2 + y**2 + z**2 + a**2)))

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
    self.w_inertia = 0.5  # ?  could make this dynamic
    self.age = 0 # how many iterations since a better position
    
    self.position=[]  # list of positions
    self.bestposition=[]  # list of best positions of all time
    self.velocity=[]  # list of velocities
    for minp,maxp in positionMinMaxList:
      rp = uniform(minp,maxp)
      self.position.append(rp)
      self.bestposition.append(rp)
      velocityMax = Cf*(maxp-minp) # could make this a dynamic variable
      self.velocity.append(uniform(0,velocityMax))

    self.fitvalue = self.evaluateFitness()
    self.bestfitvalue = self.fitvalue  # initialize with first one


  # update velocity based on Eq 2 in paper
  def updateVelocity(self, bestparticle):    # pass in bestparticle
    # use temporaries to make final equation easier to read
    c1 = self.c1
    c2 = self.c2
    r1 = uniform(0,1) # random value between 0 and 1
    r2 = uniform(0,1) # random value between 0 and 1
    w = self.w_inertia
    
    for i in range(self.Ndimensions):
      vi = self.velocity[i] # velocity at dimension i
      xi  = self.position[i] # position at dimension i
      bxi = self.bestposition[i] # best position at dimension i
      bxg = bestparticle.bestposition[i] # best position of best particle at dimension i (from outside scope)
      self.velocity[i] = w*vi + c1*r1*(bxi - xi) + c2*r2*(bxg - xi)

  # update position based on Eq 1 in paper
  def updatePosition(self):
    for i in range(self.Ndimensions):
      self.position[i] = self.position[i] + self.velocity[i]
      minp,maxp = self.positionMinMaxList[i]
      if self.position[i] < minp: self.position[i]=minp
      if self.position[i] > maxp: self.position[i]=maxp

  # update dynamic velocity max and inertia (w) -- but we aren't doing that right now...
  def updateVelocityMax_Inertia(self):
    pass

  # do the real work -- presumably call energyPlus
  def evaluateFitness(self):
    return func(self)

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


