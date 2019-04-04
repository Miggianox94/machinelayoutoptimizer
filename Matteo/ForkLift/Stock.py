import simpy

class Stock(object):
    def __init__(self,env,name,size=100):
        self.env = env
        self.container = simpy.Container(env, 100, init=0)
    def addPiece(self):
        yield self.container.put()
        print ('New Piece Added',len(self.container.get_queue),self.env.now)
        yield self.container
        yield self.env.timeout(1)
        self.container.get()
        print ('Piece Dispatched',len(self.container.get_queue),self.env.now)