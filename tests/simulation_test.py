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
  assert c.total_energy==16*40
  assert c.total_capacity==16*40
  # Off peak when at 100%
  d = make_decision(OFF_PEAK, c)
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy==16*40
  assert c.total_capacity<16*40
  # Off peak at 85% - charging
  c = make_cluster(16, 85)
  d = make_decision(OFF_PEAK, c)
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy==16*40*0.85
  assert c.total_capacity<16*40
  # Off peak at 70% - charging
  c = make_cluster(16, 70)
  d = make_decision(OFF_PEAK, c)
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  # The way the share load function is setup right now
  # we always go over delta energy but never under hence
  # total_energy>energy+d["amount"] for dis
  assert c.total_energy>=16*40*0.70 + 80
  assert c.total_capacity<16*40
  # Off peak at 30% - charging
  c = make_cluster(16, 30)
  d = make_decision(OFF_PEAK, c)
  assert c.total_energy==16*40*0.3
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy>=16*40*0.3 + 90
  assert c.total_capacity<16*40
  # Mid peak at 70% - discharge
  c = make_cluster(16, 70)
  d = make_decision(MID_PEAK, c)
  assert c.total_energy==16*40*0.7
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy<=16*40*0.7 - 40
  assert c.total_capacity<16*40
  # Mid peak at 25% -> shouldnt be any chages
  c = make_cluster(16, 25)
  d = make_decision(MID_PEAK, c)
  assert c.total_energy==16*40*0.25
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy==16*40*0.25
  assert c.total_capacity==16*40
  # On peak at 85% - discharge
  c = make_cluster(16, 85)
  d = make_decision(ON_PEAK, c)
  assert c.total_energy==16*40*0.85
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy<=16*40*0.85 - 100
  assert c.total_capacity<16*40
  # On peak at 75% - discharge
  c = make_cluster(16, 75)
  d = make_decision(ON_PEAK, c)
  assert c.total_energy==16*40*0.75
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy<=16*40*0.75 - 90
  assert c.total_capacity<16*40
  # On peak at 60% - discharge
  c = make_cluster(16, 60)
  d = make_decision(ON_PEAK, c)
  assert c.total_energy==16*40*0.60
  c.share_load(d["decision"], d["amount"], 1, OFF_PEAK)
  assert c.total_energy<=16*40*0.60 - 80
  assert c.total_capacity<16*40
