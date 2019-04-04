import simpy
import random
from AGV import AGV
from ForkLift import ForkLift
from Stock import Stock
from Sumitomo import Sumitomo
from GunScanner import GunScanner

RANDOM_SEED = 12345
NUMBER_OF_MACHINES = 10
DISTANCE_FROM_QUEUE_TO_STOCK_IN_SECONDS = 20
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
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    listOfSumitomo = sumitomo_generator(env,NUMBER_OF_MACHINES)
    listOfQueue = queue_generator(env,NUMBER_OF_MACHINES,100)
    agv = AGV(env)
    for i in range(NUMBER_OF_MACHINES):
        env.process(listOfSumitomo[i].sumitomoProduction(env,'sumitomo_'+str(i),listOfQueue[i],agv))
   
    env.run()


