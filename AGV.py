import simpy
import random

class AGV(object):
    def __init__(self,env):
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
    def callAgv(self,queue):
        request = self.resource.request()
        print ('Requested AGV')
        yield request #richiedo la risorsa AGV
        print ('AGV goes to '+ str(queue))
        yield self.env.timeout(5) #tempo che l'AGV ci mette a venire TODO renderlo dinamico
        print ('AGV reached ' + str(queue))
        if queue.level>14:
            yield queue.get(15) #AGV libera coda da 15 pezzi
        elif (queue.level != 0):
            yield queue.get(queue.level)
        print ('AGV left ' + str(queue))
        yield self.env.timeout(5) #tempo che l'AVG ci mette per andare allo stock TODO renderlo dinamico
        print ('AGV reached stock. Free again')
        self.resource.release(request)   
