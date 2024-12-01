from cluster import cluster
from battery import battery
import random
from statisticsCluster import StatisticsCluster
# from plots import Plots

# Initialize the main cluster with a maximum of 32 batteries
main_cluster = cluster(32)

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
# plot = Plots(stats)

# Lets assume I have an array full of ditonaries to let me know
# to charge or discharge and to what amount
data = [[round(random.uniform(-10, 10), 2) for _ in range(24)] for _ in range(365)]

def simulate_day(day):
  for i in range(24):
    main_cluster.share_load(day[i], 1)

def simulate_year(year):
  for i in range(365):
    simulate_day(year[i])

simulate_year(data)