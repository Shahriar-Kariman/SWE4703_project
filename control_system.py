import cluster
import battery
from random import randrange

b = []

for i in range(32):
  b.append( battery("name_"+i, randrange(70, 80, i, 40+randrange(-4,4))) )

class control_system():
  def __init__(self, inverterMaxCharge=10, inverterMaxDischarge=10, maxSoc=80, minSoc=20):
    self.cluster = cluster(32)
    map(self.cluster.add_battery, b)
    self.inverterMaxCharge = inverterMaxCharge  # in kW
    self.inverterMaxDischarge = inverterMaxDischarge  # in kW
    self.maxSoc = maxSoc  # in %
    self.minSoc = minSoc  # in %
  
  def determineEnergyTransfer(self, deltaT, decision, bat):
    #initialize working variables
    proposedCurrentEnergy = 0
    powerTransfer = 0
    startEnergy = bat.currentEnergy

    if decision == "charge":
      # Get current proposed contribution by multiplying power of inverter by deltaT to get the energy contribution, add to current capacity
      proposedCurrentEnergy = (self.inverterMaxCharge * deltaT) + bat.currentEnergy
      bat.currentEnergy = min(bat.maxEnergy, proposedCurrentEnergy) # Check for max. capacity of battery
      powerTransfer = bat.currentEnergy - startEnergy

    elif decision == "discharge":
      # Get current proposed contribution by multiplying power of inverter by deltaT to get the energy contribution, add to current capacity
      proposedCurrentEnergy = -1 * (self.inverterMaxDischarge * deltaT) + bat.currentEnergy
      bat.currentEnergy = max(bat.minEnergy, proposedCurrentEnergy) # Check for min. capacity of battery
      powerTransfer = (startEnergy - bat.currentEnergy) * -1

    else:
      powerTransfer = 0

    #print(powerTransfer)
    return powerTransfer
    