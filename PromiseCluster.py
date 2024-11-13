from BESS import BESS
import GenerateCluster
import numpy as np

class PromiseCluster:
    def __init__(self):        
        self.cluster = GenerateCluster.generateCluster()
        self.totalCapacity, self.minimumCapacity = GenerateCluster.getClusterInformtion(self.cluster)
        self.prices = np.array([0.12, 0.10, 0.08, 0.05, 0.05, 0.02, -0.05, -0.05, -0.05, 0.02, 0.10, 0.15, 0.18, 0.25, 0.30, 0.35, 0.40, 0.40, 0.30, 0.25, 0.20, 0.15, 0.12, 0.10])

    def simulate(self):
        for t in range(24):
            # if prices[t] > 0.30 and emissions[t] > 0.50 and ev.currentEnergy > ev.minSoc:
            #     energy_transfer = ev.determineEnergyTransfer(deltaT, "discharge")
            # else:
            #     energy_transfer = ev.determineEnergyTransfer(deltaT, "idle")
                # No cost or emissions for idling

            if prices[t] > 0.10 and ev.currentEnergy > ev.minSoc:
                energy_transfer = ev.determineEnergyTransfer(deltaT, "discharge")
            elif prices[t] <= 0.10 and ev.currentEnergy < ev.minSoc:
                energy_transfer = ev.determineEnergyTransfer(deltaT, "charge")
            elif prices[t] <= 0.10 and ev.currentEnergy > ev.minSoc:
                energy_transfer = ev.determineEnergyTransfer(deltaT, "discharge")
            elif prices[t] <= 0:
                energy_transfer = ev.determineEnergyTransfer(deltaT, "charge")

            # Update SOC
            df.loc[t, 'energy'] = energy_transfer
            df.loc[t, 'energyCost'] = energy_transfer * prices[t]
            df.loc[t, 'energyEmissions'] = energy_transfer * emissions[t]
            df.loc[t, 'socKWH'] = ev.currentEnergy  # Track SOC after energy transfer

    def determineEnergyTransferCluster(self, deltaT, decision):
        totalEnergyTransfer = 0

        for bess in self.cluster:
            energyTransfer = bess.determineEnergyTransfer(deltaT, decision)
            totalEnergyTransfer += energyTransfer