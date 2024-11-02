import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#define BESS Class
class BESS():  # new class
  def __init__(self, name, initialSOH, id=-1, capacity=40, inverterMaxCharge=10, inverterMaxDischarge=10, startSoc=50, maxSoc=100, minSoc=20):
      self.name = name
      self.id = id
      self.capacity = capacity  # in kWh
      self.inverterMaxCharge = inverterMaxCharge  # in kW
      self.inverterMaxDischarge = inverterMaxDischarge  # in kW
      self.startSoc = startSoc  # in %
      self.maxSoc = maxSoc  # in %
      self.minSoc = minSoc  # in %
      self.minEnergy = (self.minSoc / 100) * self.capacity  # in kWh
      self.maxEnergy = (self.maxSoc / 100) * self.capacity  
      self.currentEnergy = (self.startSoc / 100) * self.capacity  # in kW
      self.intialSOH = initialSOH
      self.esitmatedSOH = initialSOH


#define functions for energy transfer
  def determineEnergyTransfer(self, deltaT, decision):
    #initialize working variables
    proposedCurrentEnergy = 0
    powerTransfer = 0
    startEnergy = self.currentEnergy

    if decision == "charge":
      # Get current proposed contribution by multiplying power of inverter by deltaT to get the energy contribution, add to current capacity
      proposedCurrentEnergy = (self.inverterMaxCharge * deltaT) + self.currentEnergy
      self.currentEnergy = min(self.maxEnergy, proposedCurrentEnergy) # Check for max. capacity of battery
      powerTransfer = self.currentEnergy - startEnergy

    elif decision == "discharge":
      # Get current proposed contribution by multiplying power of inverter by deltaT to get the energy contribution, add to current capacity
      proposedCurrentEnergy = -1 * (self.inverterMaxDischarge * deltaT) + self.currentEnergy
      self.currentEnergy = max(self.minEnergy, proposedCurrentEnergy) # Check for min. capacity of battery
      powerTransfer = (startEnergy - self.currentEnergy) * -1

    else:
      powerTransfer = 0

    #print(powerTransfer)
    return powerTransfer
