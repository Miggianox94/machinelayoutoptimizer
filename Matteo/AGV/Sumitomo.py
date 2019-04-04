import simpy
import random
from AGV import AGV
from ForkLift import ForkLift

class Sumitomo(object):
    def __init__(self,env,name):
        self.name = name
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
    def sumitomoProduction(self,env,process,queue,AGV):
        for i in range(50):
            print (process,self.resource.count,"Process in queue: " + str(len(self.resource.queue)) + "/" + str(self.resource.capacity),"Time :" + str(self.env.now))
            request = self.resource.request()
            print (process,'Holding Sumitomo',self.resource.users,self.resource.queue,env.now)
            print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)
            yield request
            yield self.env.timeout(23)
            print (process,'Releasing Sumitomo',self.resource.users,self.resource.queue,self.env.now)
            self.resource.release(request)
            #queue.addPiece()
            yield queue.put(1)
            print (queue.level,'queue',self.env.now)
            yield self.env.timeout(1)
            if (queue.level > 14):
                self.env.process(AGV.callAgv(queue))
                #AGV.callAgv(queue)
            print (queue.level,'queue:'+str(queue), self.env.now)
            print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)
        
        while (queue.level != 0):
            print ('Queue', queue, 'is not empty: ',queue.level)
            yield self.env.process(AGV.callAgv(queue))
        print ('Queue ', queue, 'is now empty')