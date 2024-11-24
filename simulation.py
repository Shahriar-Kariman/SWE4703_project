import cluster
import battery
import random
from statisticsCluster import StatisticsCluster
from plots import Plots

# Initialize the main cluster with a maximum of 32 batteries
main_cluster = cluster(max_num_batteries=32)

battries = []

# Create and add 32 dummy batteries to the main cluster
for i in range(32):
  name = f"Battery_{i+1}"
  initialSOH = random.uniform(0.6, 0.8)
  battery_id = i
  capacity = random.randint(30, 50)  # Capacity between 30 and 50 kWh
  startSoc = 100
  b1 = battery(name, initialSOH, battery_id, capacity, startSoc)
  b2 = battery(name, initialSOH, battery_id, capacity, startSoc)
  main_cluster.add_battery(b1)
  battries.append(b2)

stats = StatisticsCluster(main_cluster)
plot = Plots(stats)

yearly_contract = 100  # kW
# 10 event for 10 years each 25$ per kW
total_profits = 25 * yearly_contract * 10 * 10

for year in range(10):
  for event in range(10):
    for hours in range(5):
      main_cluster.share_load(100, 1)
    # charge all batteries until full charge
  for b in main_cluster.batteries:
    b.profit1 += b.individualContribution/(yearly_contract) * (total_profits/10)
    b.individualContribution = 0
    # DO PROFITS PROMISE
  stats.updateClusterStats()