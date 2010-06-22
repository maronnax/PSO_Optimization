from random import uniform

#func = lambda x:math.cos(x) * math.exp(math.sin(x)) * math.sin(x)  / 1.5

class Particle:
  def __init__(self, positionMinMaxList, Cf):
    self.positionMinMaxList=positionMinMaxList
    self.Cf = Cf
    
    self.position=[]  # list of positions
    self.velocity=[]  # list of velocities
    self.bestPosition=[] # list of best positions
    for minp,maxp in positionMinMaxList:
      rp = uniform(minp,maxp)
      self.position.append(rp)
      self.bestPosition.append(rp)

      velocityMax = Cf*(maxp-minp)
      self.velocity.append(uniform(0,velocityMax))
    
  def __str__(self):
    s=""
    for i in range(len(self.positionMinMaxList)):
      s+="%2d pos=%7.2f vel=%7.2f best=%7.2f\n" % \
          (i, self.position[i], self.velocity[i], self.bestPosition[i])
    return s



