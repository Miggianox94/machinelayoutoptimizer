import simpy
import random

RANDOM_SEED = 12345
NUMBER_OF_MACHINES = 10
DISTANCE_FROM_QUEUE_TO_STOCK_IN_SECONDS = 20
from simpy.resources.container import Container,ContainerPut,ContainerGet
class Sumitomo():
    def __init__(self,env,name):
        self.name = name
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
    def sumitomoProduction(self,env,process,queue,AGV):
        while True:
            print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,env.now)
            request = self.resource.request()
            print (process,'Holding Sumitomo',self.resource.users,self.resource.queue,env.now)
            print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)
            yield request
            yield self.env.timeout(23)
            print (process,'Releasing Sumitomo',self.resource.users,self.resource.queue,self.env.now)
            self.resource.release(request)
            #queue.addPiece()
            yield queue.put(1)
            print (queue.level,'queue',env.now)
            yield self.env.timeout(1)
            if (queue.level > 14):
                env.process(AGV.callAgv(queue))
                #AGV.callAgv(queue)
                
                
            print (queue.level,'queue', env.now)
            print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)

class AGV():
    def __init__(self,env):
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
    def callAgv(self,queue):
        request = self.resource.request()
        print ('Requested AGV')
        yield request #richiedo la risorsa AGV
        print ('AGV goes to '+ str(queue))
        yield env.timeout(5) #tempo che l'AGV ci mette a venire TODO renderlo dinamico
        print ('AGV reached ' + str(queue))
        yield queue.get(15) #AGV libera coda da 15 pezzi
        print ('AGV left ' + str(queue))
        yield env.timeout(5) #tempo che l'AVG ci mette per andare allo stock TODO renderlo dinamico
        print ('AGV reached stock. Free again')
        self.resource.release(request)   
        


class Stock():
    def __init__(self,env,name,size=100):
        self.env = env
        self.container = simpy.Container(env, 100, init=0)
    def addPiece(self):
        yield self.container.put()
        print ('New Piece Added',len(self.container.get_queue),self.env.now)
        yield self.container
        yield env.timeout(1)
        self.container.get()
        print ('Piece Dispatched',len(self.container.get_queue),self.env.now)

def sumitomo_generator(env, n):
    listOfSumitomo = []
    for i in range(n):
        listOfSumitomo.append(Sumitomo(env,"sumitomo_"+str(i)))
    return listOfSumitomo

def queue_generator(env,n,size):
    listOfQueue = []
    for i in range(n):
        #listOfQueue.append(Stock(env,size,'queue_'+str(i)))
        listOfQueue.append(simpy.Container(env,size,0))
    return listOfQueue


if __name__ == '__main__':
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    listOfSumitomo = sumitomo_generator(env,NUMBER_OF_MACHINES)
    listOfQueue = queue_generator(env,NUMBER_OF_MACHINES,100)
    agv = AGV(env)
    for i in range(NUMBER_OF_MACHINES):
        env.process(listOfSumitomo[i].sumitomoProduction(env,'process_'+str(i),listOfQueue[i],agv))
    env.run(1000)

