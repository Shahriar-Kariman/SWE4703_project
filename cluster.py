
class cluster_shawn():
  def __init__(self, max_num_batteries):
    self.batteries = []
    self.num_batteries = 0
    self.max_num_batteries = max_num_batteries
  
  # Adding a battery to the cluster
  def add_battery(self, b):
    if self.max_num_batteries <= self.num_batteries:
      return
    self.batteries.append(b)
    self.num_batteries += 1

  # Removing a battery from the cluster
  def remove_battery(self, b):
    if b in self.batteries:
      self.batteries.remove(b)
      self.num_batteries -= 1
  
  def share_load(self, delta_energy, deltaT):
    # Essentially a greedy algorithm to just pick the batteries with the healthist batteries with the most amount of charge
    sorted_batteries = sorted(self.batteries, key=lambda b: (b.esitmatedSOH, b.currentSOC), reverse=True)
    decision = "charge" if delta_energy>0 else "discharge"
    remaining_energy = abs(delta_energy)
    for battery in sorted_batteries:
      # making sure the energy tranfer from the battery does not exceed the remaining energy
      if not battery.can_transfer(remaining_energy, deltaT, decision):
        result = battery.transfer_energy(deltaT, decision)
        remaining_energy -= result['energy_transfer']
      else:
        degredation = battery.calender_degredation(deltaT)
        battery.apply_deg(degredation)
  