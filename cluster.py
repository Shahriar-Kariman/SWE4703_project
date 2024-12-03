
class cluster():
  def __init__(self, max_num_batteries):
    self.batteries = []
    self.num_batteries = 0
    self.max_num_batteries = max_num_batteries
    self.total_capacity = 0
    self.total_energy = 0
    self.total_SOC = 0
  
  # Adding a battery to the cluster
  def add_battery(self, b):
    if b.capacity==0:
      return
    if self.max_num_batteries <= self.num_batteries:
      return
    self.batteries.append(b)
    self.num_batteries += 1
    self.update_SOC()

  # Removing a battery from the cluster
  def remove_battery(self, b):
    if b in self.batteries:
      self.batteries.remove(b)
      self.num_batteries -= 1
  
  def share_load(self, decision, delta_energy, deltaT):
    # Essentially a greedy algorithm to just pick the batteries with the healthist batteries with the most amount of charge
    sorted_batteries = sorted(self.batteries, key=lambda b: (b.esitmatedSOH, b.currentSOC), reverse=True)
    remaining_energy = abs(delta_energy)
    for battery in sorted_batteries:
      # making sure the energy tranfer from the battery does not exceed the remaining energy
      if not battery.can_transfer(remaining_energy, deltaT, decision):
        result = battery.transfer_energy(deltaT, decision)
        remaining_energy -= result['energy_transfer']
      else:
        degredation = battery.calender_degredation(deltaT)
        battery.apply_deg(degredation)
    self.update_SOC()
  
  def update_SOC(self):
    self.total_capacity = 0
    self.total_energy = 0
    for b in self.batteries:
      self.total_capacity += b.capacity
      self.total_energy += b.currentEnergy
    self.total_SOC = self.total_energy/self.total_capacity * 100