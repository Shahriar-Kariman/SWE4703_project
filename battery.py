
class battery():
    def __init__(self, name, initialSOH, id=-1, capacity=40, startSoc=50):
        self.name = name
        self.id = id
        self.originalCapacity = capacity
        self.capacity = capacity * initialSOH # in kWh
        self.startSoc = startSoc  # in %
        self.initialSOH = initialSOH
        self.esitmatedSOH = initialSOH
        self.currentEnergy = (self.startSoc / 100) * self.capacity  # in kW
        self.profit1 = 0
        self.profit2 = 0
        self.profit3 = 0
        self.maxEnergy = self.capacity
        self.minEnergy = 0
        # will need to research to find the correct constants for the 2 bellow
        self.cycle_deg_rate = 0.0005  # Degradation per full charge/discharge cycle
        self.cal_deg_rate = 0.00001  # Time-based degradation per hour

    def getBatteryInfo(self):
        return [self.name, self.id, self.originalCapacity, self.initialSOH]

    # Charges the battery for a set amount of time
    def charge_battery(self, deltaT, decision): # deltaT unit is hours
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
        
        # Update the SOH and capacity based on degredation
        # cycle based degredation
        energy_transfer = abs(powerTransfer)
        num_cycles = energy_transfer/self.originalCapacity
        cycle_deg = self.cycle_deg_rate * num_cycles
        # calender based degredation
        cal_deg = self.cal_deg_rate * deltaT
        degredation = cycle_deg + cal_deg
        self.esitmatedSOH = max(0, self.esitmatedSOH - degredation)

        # update capacity
        self.capacity = self.originalCapacity * self.esitmatedSOH
        self.maxEnergy = self.capacity

        # returning a summery of what just happened
        # I dont really need to return anything though
        return {
            "decision": decision,
            "energy_transper": energy_transfer,
            "start_energy": startEnergy,
            "end_energy": self.currentEnergy,
            "degredation": degredation,
        }
