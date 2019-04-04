import simpy
import random
from AGV import AGV
from ForkLift import ForkLift

STARTING_TIME_AVG = 200

class Sumitomo(object):
    def __init__(self,env,name):
        self.name = name
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
        self.start_time = random.expovariate(lambd=1.0/STARTING_TIME_AVG)
    def sumitomoProduction(self,env,process,queue):
        yield env.timeout(self.start_time)
        print ('Machine ' + self.name + " started", env.now)
        for i in range(61):
            #print (process,self.resource.count,"Process in queue: " + str(len(self.resource.queue)) + "/" + str(self.resource.capacity),"Time :" + str(self.env.now))
            request = self.resource.request()
            #print (process,'Holding Sumitomo',self.resource.users,self.resource.queue,env.now)
            #print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)
            yield request
            yield self.env.timeout(23)
            #print (process,'Releasing Sumitomo',self.resource.users,self.resource.queue,self.env.now)
            self.resource.release(request)
            #queue.addPiece()
            yield queue.put(1)
            #print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)
        
        # while (queue.level != 0):
        #     print ('Queue', queue, 'is not empty: ',queue.level)
        #     yield self.env.process(AGV.callAgv(queue))
        #print ('Queue ', queue, 'is now empty')