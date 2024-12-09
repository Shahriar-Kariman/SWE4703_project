from cluster import cluster
from battery import battery
from time_handler import time_handler
from arbiterage_simulation import summer_day_rates, winter_day_rate, ON_PEAK, OFF_PEAK, MID_PEAK, make_decision

def make_cluster(n, SOCs):
  c = cluster(n)
  for i in range(n):
    name = f"Battery_{i+1}"
    initialSOH = 1
    battery_id = i
    capacity = 40
    b = battery(name, initialSOH, battery_id, capacity, SOCs)
    c.add_battery(b)
  return c

# I could have gone more in detail with the degredation
# in these tests but since I already did that in the general tests I wont do that
def test_simulation():
  c = make_cluster(16, 100)
  # A summer day consists of
  # 12 OFF_PEAK, 6 MID_PEAK and 6 ON_PEAK hours
  assert c.total_energy==16*40
  assert c.total_capacity==16*40
  # Off peak when at 100%
  d = make_decision(OFF_PEAK)
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy==16*40
  assert c.total_capacity<16*40
  # Off peak at 85% - charging
  c = make_cluster(16, 80)
  d = make_decision(OFF_PEAK)
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy==16*40*0.85
  assert c.total_capacity<16*40
  # Off peak at 70% - charging
  c = make_cluster(16, 70)
  d = make_decision(OFF_PEAK)
  assert c.total_energy==16*40*0.7
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  # The way the share load function is setup right now
  # we always go over delta energy but never under hence
  # total_energy>energy+d["amount"] for dis
  assert c.total_energy>16*40*0.70 + 80
  assert c.total_capacity<16*40
