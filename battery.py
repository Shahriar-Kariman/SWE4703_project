
class battery():
    def __init__(self, name, initialSOH, id=-1, capacity=40, startSoc=50, inverterMaxCharge=10, inverterMaxDischarge=10):
        self.name = name
        self.id = id
        self.originalCapacity = capacity
        self.capacity = capacity * initialSOH # in kWh
        self.currentSOC = startSoc  # in %
        self.initialSOH = initialSOH
        self.esitmatedSOH = initialSOH
        self.currentEnergy = (self.currentSOC / 100) * self.capacity  # in kW
        self.individualContribution = 0  # in kW
        self.profit1 = 0
        self.profit2 = 0
        self.profit3 = 0
        self.maxEnergy = self.capacity * 0.85
        self.minEnergy = self.capacity * 0.2
        self.inverterMaxCharge = inverterMaxCharge  # in kW
        self.inverterMaxDischarge = inverterMaxDischarge  # in kW
        # will need to research to find the correct constants for the 2 bellow
        self.cycle_deg_rate = 4.6/1000  # Degradation per full charge/discharge cycle
        # assuming annual capacity degradation (2%)
        self.cal_deg_rate =  (0.5/100)/(365*24)  # Time-based degradation per hour
        # I might add depth of discharge degredation later

    def getBatteryInfo(self):
        return [self.name, self.id, self.originalCapacity, self.initialSOH]

    # Charges or discharges the battery for a set amount of time
    def transfer_energy(self, deltaT, decision): # deltaT unit is hours
        [powerTransfer, new_currentEnergy] = self.calc_possible_powerTransfer(deltaT, decision)
        prev_energy = self.currentEnergy
        self.currentEnergy = new_currentEnergy
        if decision == "discharge":
            self.individualContribution += powerTransfer
        energy_transfer = abs(powerTransfer)
        # Update the SOH and capacity based on degredation
        cycle_deg = self.cycle_degredation(energy_transfer, prev_energy)
        cal_deg = self.calender_degredation(deltaT)
        degredation = cycle_deg + cal_deg
        self.apply_deg(degredation)
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
            new_currentEnergy = min(self.maxEnergy, proposedCurrentEnergy) # Check for max. capacity of battery
            powerTransfer = new_currentEnergy - startEnergy
        elif decision == "discharge":
            # Get current proposed contribution by multiplying power of inverter by deltaT to get the energy contribution, add to current capacity
            proposedCurrentEnergy = -1 * (self.inverterMaxDischarge * deltaT) + self.currentEnergy
            new_currentEnergy = max(self.minEnergy, proposedCurrentEnergy) # Check for min. capacity of battery
            powerTransfer = (startEnergy - new_currentEnergy) * -1
        else:
            powerTransfer = 0
        return [powerTransfer, new_currentEnergy]

    def can_transfer(self, energy, deltaT, decision):
        [possible_transfer, new_currentEnergy] = self.calc_possible_powerTransfer(deltaT, decision)
        if energy <= possible_transfer:
            return True
        return False
    
    # cycle based degredation approximation
    # I am kind of ignoring depth of discharge here for simplicity
    def cycle_degredation(self, energy_transfer, prev_energy):
        num_cycles = energy_transfer/prev_energy
        cycle_deg = self.cycle_deg_rate * num_cycles
        return cycle_deg

    # calender based degredation approximation
    def calender_degredation(self, deltaT):
        cal_deg = self.cal_deg_rate * deltaT
        return cal_deg
    
    def apply_deg(self, degredation):
        # it is critical that these are updated especially SOH and currentSOC
        self.esitmatedSOH = max(0, self.esitmatedSOH - degredation)
        self.capacity = self.originalCapacity * self.esitmatedSOH
        # between 85% to 20%
        self.maxEnergy = self.capacity * 0.85
        self.minEnergy = self.capacity * 0.2
        self.currentSOC = (self.currentEnergy/self.capacity) * 100
    