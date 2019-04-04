import simpy
import random


class ForkLift(object):
    def __init__(self,env,name):
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
        self.capacity = 300
        self.numberOfItems = 0
        self.totalItems = 0
        self.name = name
    def liftBoxes(self,queues):
        while True:
            request = self.resource.request()
            print ('ForkLift in sleeping mode...')
            yield self.env.timeout(10*60)
            print ('ForkLift starts tour')
            for queue in queues:
                print (queue.level,self.capacity,self.numberOfItems)
                if ((queue.level >= 30) and ((self.capacity-self.numberOfItems)>30)):
                    print ('More than 30...'+str(queue.level))
                    self.numberOfItems = self.numberOfItems + 30
                    self.totalItems = self.totalItems + 30
                    print (self.name + ' takes 30 elements', str(self.numberOfItems/30) + " pallets on the forklift")                    
                    yield queue.get(30) #muletto prende 30 pezzi
                #TODO PER ADESSO PRENDE SOLO I PALLET. E I PALLET SONO DA 30.
                #elif (queue.level != 0):
                #    print ('Forklift takes ' + str(queue.level)+ ' elements')
                #    yield queue.get(queue.level)
            print ('ForkLift left ' + str(queue))
            yield self.env.timeout(5)
            print ('ForkLift reached stock. Free again')
            self.numberOfItems = 0
            self.resource.release(request)
    
    def getTotalProcessed(self):
        return self.totalItems