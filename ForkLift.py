import simpy
import random


class ForkLift(object):
    def __init__(self,env):
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
    
    def liftBoxes(self,queues):
        while True:
            request = self.resource.request()
            print ('ForkLift in sleeping mode...')
            yield self.env.timeout(10*60)
            print ('ForkLift starts tour')
            for queue in queues:
                if queue.level > 30:
                    print ('Forklift takes 30 elements')
                    yield queue.get(30) #muletto prende 30 pezzi
                elif (queue.level != 0):
                    print ('Forklift takes ' + str(queue.level)+ ' elements')
                    yield queue.get(queue.level)
            print ('ForkLift left ' + str(queue))
            yield self.env.timeout(5) #tempo che l'AVG ci mette per andare allo stock TODO renderlo dinamico
            print ('ForkLift reached stock. Free again')
            self.resource.release(request)