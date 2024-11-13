from BESS import BESS
import random

def generateCluster():
    cluster = []
    for i in range(32):
       name =  "Battery" + str(i)
       initialSOH = random.randint(60, 85)
       id = i
       initialCapacity = random.randint(40, 100)
       inverterMaxCharge = 10
       inverterMaxDischarge = 10
       startSoc = 100
       maxSoc = 90
       minSoc = 20

       tempBess = BESS(name, initialSOH, id, initialCapacity, inverterMaxCharge, inverterMaxDischarge, startSoc, maxSoc, minSoc)
       cluster.append(tempBess)

    return cluster

def getClusterInformtion(cluster):
    totalCapacity = 0
    minimumCapacity = 100000
    for bess in cluster:
        totalCapacity += bess.capacity
        if bess.capacity < minimumCapacity:
            minimumCapacity = bess.capacity

    return totalCapacity, minimumCapacity

