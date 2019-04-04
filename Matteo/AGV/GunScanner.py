import simpy
import random

class GunScanner(object):
    #l'idea e' che il tipo con la pistola aspetti che un pallet sia pieno per pistolettarlo. 
    # Concettualmente quindi e' come un "AGV". Aspetta che ci siano 15 elementi sulla coda e li processa. 
    # L'unica differenza e' che dopo di lui, l'entita' ForkLift verra' chiamata per portare a destinazione le scatole.
    def __init__(self,env):
        self.env = env
        self.resource = simpy.Resource(env,capacity=1)
    def scanWithGun(self,queue):
        request = self.resource.request()
        print ('Guy with the GUN called:')
        yield request #richiedo la risorsa omino
        print ('Guy goes to '+ str(queue))
        yield self.env.timeout(1) #tempo che l'omino ci mette a venire TODO renderlo dinamico
        print ('Guy scanned ' + str(queue))