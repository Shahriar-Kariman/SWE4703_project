
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


    def getBatteryInfo(self):
        return [self.name, self.id, self.originalCapacity, self.initialSOH]