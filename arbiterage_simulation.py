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

for b in battries:
  print(b.esitmatedSOH)

stats = StatisticsCluster(main_cluster)
# plot = Plots(stats)

# TOU rates for each hour in Ontario
ON_PEAK = 15.8
OFF_PEAK = 7.6
MID_PEAK = 12.2
summer_day_rates = [OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, MID_PEAK, MID_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, 7.6]
winter_day_rate = [OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, ON_PEAK, ON_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, 7.6]

# Look at Ontario website for number of events
# 2 $ per kWh
# event is 5 hours

def simulate_day(day):
  for i in range(24):
    d = make_decision(day[i])
    main_cluster.share_load(d["decision"], d["amount"], 1, day[i])
  

def simulate_summer():
  # summer is 184 days
  for i in range(184):
    simulate_day(summer_day_rates)
  

def simulate_winter():
  # winter is 182 days
  for i in range(181):
    simulate_day(winter_day_rate)
  

def simulate_year():
  simulate_summer()
  simulate_winter()

def make_decision(rate):
  decision = "idle"
  energy_amount = 0 # kW
  if rate == ON_PEAK:
    decision = "discharge"
    # energy_amount = 12
  elif rate == OFF_PEAK:
    decision = "charge"
    # energy_amount = 12
  else:
    if main_cluster.total_SOC<50:
      decision = "charge"
      # energy_amount = 7
    elif main_cluster.total_SOC>60:
      decision = "discharge"
      # energy_amount = 7
  return {"decision": decision, "amount": 10}

simulate_year()

total_profit1 = 0
total_profit2 = 0
for b in main_cluster.batteries:
  total_profit1 += b.profit1
  total_profit2 += b.profit2
  print("profit 1", b.profit1, "profit 2", b.profit2, "state of health", b.esitmatedSOH)
print("total profit 1", total_profit1, "total profit 2", total_profit2)
