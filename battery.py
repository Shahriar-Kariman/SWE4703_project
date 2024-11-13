
class battery():
  def __init__(self, name, initialSOH, id=-1, capacity=40, startSoc=50, maxSoc=80, minSoc=20):
    self.name = name
    self.id = id
    self.capacity = capacity  # in kWh
    self.startSoc = startSoc  # in %
    self.maxSoc = maxSoc  # in %
    self.minSoc = minSoc  # in %
    self.intialSOH = initialSOH
    self.esitmatedSOH = initialSOH
    self.currentEnergy = (self.startSoc / 100) * self.capacity  # in kW
    self.minEnergy = (self.minSoc / 100) * self.capacity  # in kWh
    self.maxEnergy = (self.maxSoc / 100) * self.capacity