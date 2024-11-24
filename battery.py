
class battery():
    def __init__(self, name, initialSOH, id=-1, capacity=40, startSoc=50):
        self.name = name
        self.id = id
        self.originalCapacity = capacity
        self.capacity = capacity * initialSOH # in kWh
        self.currentSOC = startSoc  # in %
        self.initialSOH = initialSOH
        self.esitmatedSOH = initialSOH
        self.currentEnergy = (self.currentSOC / 100) * self.capacity  # in kW
        self.profit1 = 0
        self.profit2 = 0
        self.profit3 = 0
        self.maxEnergy = self.capacity
        self.minEnergy = 0
        # will need to research to find the correct constants for the 2 bellow
        self.cycle_deg_rate = 0.0005  # Degradation per full charge/discharge cycle
        self.cal_deg_rate = 0.00001  # Time-based degradation per hour
        # I might add depth of discharge degredation later

    def getBatteryInfo(self):
        return [self.name, self.id, self.originalCapacity, self.initialSOH]

    # Charges or discharges the battery for a set amount of time
    def transfer_energy(self, deltaT, decision): # deltaT unit is hours
        # Update the SOH and capacity based on degredation
        # cycle based degredation
        powerTransfer = self.calc_possible_powerTransfer(deltaT, decision)
        energy_transfer = abs(powerTransfer)
        num_cycles = energy_transfer/self.originalCapacity
        cycle_deg = self.cycle_deg_rate * num_cycles
        # calender based degredation
        cal_deg = self.cal_deg_rate * deltaT
        degredation = cycle_deg + cal_deg
        self.esitmatedSOH = max(0, self.esitmatedSOH - degredation)

        # it is critical that these are updated especially SOH and currentSOC
        self.capacity = self.originalCapacity * self.esitmatedSOH
        self.maxEnergy = self.capacity
        self.currentSOC = self.currentEnergy/self.maxEnergy

        # returning a summery of what just happened
        # I dont really need to return anything though
        return {
            "decision": decision,
            "energy_transfer": energy_transfer,
            "end_energy": self.currentEnergy,
            "degredation": degredation,
        }
    
    def calc_possible_powerTransfer(self, deltaT, decision):
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
        return powerTransfer
