from random import uniform
#from particle import Particle

#func = lambda x:math.cos(x) * math.exp(math.sin(x)) * math.sin(x)  / 1.5

#def func(particle):
#  sum=0.0
#  
#  for p in particle.position
#    sum += p
#  avg = sum/float(len(particle.position))
#  val = math.cos(avg) * math.exp(math.sin(avg)) * math.sin(avg)  / 1.5
#  return val

#class Particle:
#  def __init__(self, positionList):
#    self.positionList=positionList
#    self.bestPosition=positionList
#    self.velocityList=[]
#    for i in range(0,len(self.positionList)):
#      self.velocityList.append(0)
#
#
#  def __str__(self):
#    s=""
#    for i in range(0, len(self.positionList)):
#      s+="%2d pos=%7.2f vel=%7.2f best=%7.2f\n" % (i, self.positionList[i], \
#                                                   self.velocityList[i], \
#                                                   self.bestPosition[i])
#    return s



class PSO:
    def __init__(self, pop_size, min, max, phi, phi2, lr, maxiter, func):
        self.func = func
        self.pop = []
        # 0: position, 1: velocity, 2: fitness
        self.min = min
        self.max = max
        for i in xrange(pop_size):
            self.pop.append([uniform(self.min, self.max), uniform(-1, 1), 0])
        self.evaluate()
        self.gdest = self.pop[0]
        self.pdest = self.pop[0]
        self.phi = phi
        self.phi2 = phi2
        self.lr = lr
        self.maxiter = maxiter
    
    def update_velocity(self):
        for i in self.pop:
            i[1] = self.lr * i[1] + uniform(0, self.phi) \
                    * (self.pdest[0] - i[0]) + uniform(0, self.phi2) \
                    * (self.gdest[0] - i[0])
 
    def evaluate(self):
        for i in self.pop:
            i[2] = self.func(i[0])
 
    def move(self):
        for i in self.pop:
            i[0] += i[1]
 
    def __cmp_by_fitness(self, a, b):
        return cmp(a[2], b[2])
    
    def run(self, update_func=False):
        for i in xrange(self.maxiter):
            if update_func:
                update_func()
            self.update_velocity()
            self.move()
            self.evaluate()
            self.pop.sort(self.__cmp_by_fitness, reverse=0)
            self.pdest = self.pop[0]
            if self.pdest[2] < self.gdest[2]:
                self.gdest = self.pdest

                
