from cluster import cluster
from battery import battery
from time_handler import time_handler
from arbiterage_simulation import summer_day_rates, winter_day_rate, ON_PEAK, OFF_PEAK, MID_PEAK

def make_cluster(n):
  c = cluster(n)
  for i in range(n):
    name = f"Battery_{i+1}"
    initialSOH = 1
    battery_id = i
    capacity = 40
    startSoc = 100
    b = battery(name, initialSOH, battery_id, capacity, startSoc)
    c.add_battery(b)

def test_simulation():
  t = time_handler()
  c = make_cluster(3)
