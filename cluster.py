
class cluster_shawn():
  def __init__(self, max_num_batteries):
    self.batteries = []
    self.num_batteries = 0
    self.max_num_batteries = max_num_batteries
  
  # Adding a battery to the cluster
  def add_battery(self, b):
    if self.max_num_batteries <= self.num_batteries:
      return
    self.battereis.append(b)
    self.num_batteries += 1

  # Removing a battery to the cluster
  def remove_battery_at(self, b):
    if self.num_batteries == 0:
      return
    self.batteries.remove(b)
    self.num_batteries -= 1