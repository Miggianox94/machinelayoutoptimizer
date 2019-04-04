import simpy
import random
from AGV import AGV
from ForkLift import ForkLift
from Stock import Stock
from Sumitomo_forklift import Sumitomo
from GunScanner import GunScanner

RANDOM_SEED = 12345
NUMBER_OF_MACHINES = 2
DISTANCE_FROM_QUEUE_TO_STOCK_IN_SECONDS = 20
NUMBER_OF_FORKLIFT = 2
AVERAGE_TIME_TO_START = 30
STD_DEV_TO_START = 10
from simpy.resources.container import Container,ContainerPut,ContainerGet
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
    
    try:
        random.seed(RANDOM_SEED)
        env = simpy.Environment()
        processes = []
        listOfSumitomo = sumitomo_generator(env,NUMBER_OF_MACHINES)
        listOfQueue = queue_generator(env,NUMBER_OF_MACHINES,100)
        listOfForklift = [ForkLift(env,'ForkLift_'+str(i)) for i in range(NUMBER_OF_FORKLIFT)]
        for i in range(NUMBER_OF_MACHINES):
            env.process(listOfSumitomo[i].sumitomoProduction(env,'sumitomo_'+str(i),listOfQueue[i]))
        for forkLift in listOfForklift:
            processes.append(env.process(forkLift.liftBoxes(listOfQueue)))
    
        env.run()
    
    except KeyboardInterrupt:
        print env.now
        
        for p in processes:
            try:
                p.interrupt()
            except Exception:
                print ('Already Interrupted')

    
        for forkLift in listOfForklift:
            print 'total',forkLift.getTotalProcessed()

        for queue in listOfQueue:
            print queue.level

