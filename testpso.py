#!/usr/bin/env python
import os, sys, re, time
import PSO
import Particle
from random import uniform

#Classroom_Weekday_T1: 10.5
#Classroom_Weekday_T2: 0.25
#Classroom_Weekday_T3: 0.05
#Classroom_Weekday_T4: 14.0

positionMinMaxList=[(0,100), (0,12), (-100,0)]

#p=Particle.Particle(positionMinMaxList)
#print p

#r1=uniform(0, 1)
#r2=uniform(0, 1)
c1 = 2.0
c2 = 2.0
Cf = 0.5
kiterationMax=3
Nparticles=5

particleList=[]
for ip in range(Nparticles):
  p = Particle.Particle(positionMinMaxList, Cf)
  particleList.append(p)
  print p
  #fitvalue = PSO.func(p)

for kiter in range(kiterationMax):
  print kiter

  
