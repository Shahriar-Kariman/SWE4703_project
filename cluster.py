
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
  
  def share_load(self, decision, delta_energy, deltaT, rate):
    # Essentially a greedy algorithm to just pick the batteries with the healthist batteries with the most amount of charge
    if decision == "discharge":
      sorted_batteries = sorted(self.batteries, key=lambda b: (b.esitmatedSOH, b.currentSOC), reverse=True)
    else:
      sorted_batteries = sorted(self.batteries, key=lambda b: (b.esitmatedSOH, -1 * b.currentSOC), reverse=True)
    remaining_energy = abs(delta_energy)
    total_energy_transfer = 0
    total_cluster_capacity = 0
    for battery in sorted_batteries:
      total_cluster_capacity += battery.capacity
      # making sure the energy tranfer from the battery does not exceed the remaining energy
      if remaining_energy>0:
        result = battery.transfer_energy(deltaT, decision)
        a = 1 if result["decision"]=="discharge" else -1
        total_energy_transfer += a * result["energy_transfer"]
        battery.add_profit_1(rate, result["decision"], result["energy_transfer"], deltaT)
        remaining_energy -= result["energy_transfer"]
      else:
        degredation = battery.calender_degredation(deltaT)
        battery.apply_deg(degredation)
    
    total_profit = total_energy_transfer * rate
    for battery in sorted_batteries:
      battery.add_profit_2(total_profit, total_cluster_capacity)

    self.update_SOC()
  
  def update_SOC(self):
    self.total_capacity = 0
    self.total_energy = 0
    for b in self.batteries:
      self.total_capacity += b.capacity
      self.total_energy += b.currentEnergy
    self.total_SOC = self.total_energy/self.total_capacity * 100
  
  def weekend_calender_deg(self, days):
    for battery in self.batteries:
      # 24 hours in a day
      degredation = battery.calender_degredation(24*days)
      battery.apply_deg(degredation)