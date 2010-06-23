import epopt
import PSO
import Particle
from random import uniform

def simulationInProgress():
    return epopt.exists("PSO.pickle")

if not simulationInProgress():
    specs = open("Specification.txt").readlines()

    for spec in specs:
        name, range = spec.split(":")
        
        range = range.strip()
        range = range[1:-1]

        least, greatest = range.split(",")
        least = float(least)
        greatest = float(greatest)


    
    for ip in range(NParticles):
        p = Particle.Particle(positionMinMaxList, Cf)
        particleList.append( p )










