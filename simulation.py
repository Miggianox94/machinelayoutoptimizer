import simpy
from simpy.resources.container import Container,ContainerPut,ContainerGet
class Sumitomo():
    def __init__(self,env):
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
    def sumitomoProduction(self,env,process,queue):
        print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,env.now)
        request = self.resource.request()
        print (process,'Holding Sumitomo',self.resource.users,self.resource.queue,env.now)
        print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)
        yield request
        yield self.env.timeout(23)
        print (process,'Releasing Sumitomo',self.resource.users,self.resource.queue,self.env.now)
        self.resource.release(request)
        yield queue.put(1)
        print (queue.level,'queue',env.now)
        yield self.env.timeout(1)
        yield queue.get(1)
        print (queue.level,'queue', env.now)
        print (process,self.resource.count,self.resource.capacity,self.resource.users,self.resource.queue,self.env.now)


class Stock():
    def __init__(self,env):
        self.env = env
        self.container = simpy.Container(env, 100, init=0)
    def addPiece(self):
        self.container.put()
        print ('New Piece Added',len(self.container.get_queue),self.env.now)
        yield env.timeout(1)
        self.container.get()
        print ('Piece Dispatched',len(self.container.get_queue),self.env.now)

if __name__ == '__main__':
    env = simpy.Environment()
    sumitomo1 = Sumitomo(env)
    sumitomo2 = Sumitomo(env)
    queue2 = simpy.Container(env,100,0)
    env.process(sumitomo1.sumitomoProduction(env,'process1',queue2))
    env.process(sumitomo2.sumitomoProduction(env,'process2',queue2))
    env.run(100)

