from battery import battery

# ----------------------- single battery tests -----------------------

def test_1_battery():
  b = battery("test_battery", 1, 0, startSoc=100)
  possible_transfer = b.calc_possible_powerTransfer(2, "discharge")
  # if I discharge a battery with inverterMaxCharge=10
  # for 2 hours I should get:
  # power_transfer = -20 and new_currentEnergy = 20
  assert possible_transfer[0]==-20
  assert possible_transfer[1]==20
  # So the calcualtion it self should not apply the changes
  # so the battery needs to be at the same condition as the
  # begining
  assert b.name == "test_battery"
  assert b.id == 0
  assert b.capacity == 40
  assert b.currentSOC == 100
  assert b.currentEnergy == 40
  # Now I can test the degredations
  cycle_deg = b.cycle_degredation(possible_transfer[0])
  # now because I am discharging for half a cycle
  assert cycle_deg == 4.6/1000/2
  calender_deg = b.calender_degredation(2)
  assert calender_deg == (0.5/100)/(365*24) * 2
  # Now for charging
  b = battery("test_battery", 1, 0, startSoc=60)
  possible_transfer = b.calc_possible_powerTransfer(1, "charge")
  # if I charge a battery with inverterMaxCharge=10
  # for 1 hours I should get:
  # power_transfer = 10 and new_currentEnergy = 40*0.6+10
  assert possible_transfer[0]==10
  assert possible_transfer[1]==34
  # Now I can test the degredations again
  cycle_deg = b.cycle_degredation(possible_transfer[0])
  # now because I am discharging for quarter of a cycle
  assert cycle_deg == 4.6/1000/4
  calender_deg = b.calender_degredation(1)
  assert calender_deg == (0.5/100)/(365*24) * 1
  # and the edge cases like charging near full charge and
  # discharging when almost out
  b = battery("test_battery", 1, 0, startSoc=80)
  possible_transfer = b.calc_possible_powerTransfer(1, "charge")
  # considering maxEnergy is 85% of the capacity
  assert possible_transfer[0]==40*0.05
  assert possible_transfer[1]==40*0.85
  # and min energy is 20%
  b = battery("test_battery", 1, 0, startSoc=25)
  possible_transfer = b.calc_possible_powerTransfer(1, "discharge")
  assert possible_transfer[0]==-40*0.05
  assert possible_transfer[1]==40*0.2

# So far test one has estanlished that calc_possible_powerTransfer
# and the degredation functions work
# test 2 will check if it correctly changes the battery in accordance
def test_2_battery():
  b = battery("test_battery", 1, 0, startSoc=100)
  result_1 = b.transfer_energy(3, "discharge")
  assert result_1["energy_transfer"]==30
  assert result_1["degredation"]==4.6/1000*3/4+(0.5/100)/(365*24) * 3
  assert b.capacity == 40-result_1["degredation"]
  assert b.currentEnergy == 40-30
  num_cycles = 20/b.capacity
  result_2 = b.transfer_energy(2, "charge")
  assert result_2["energy_transfer"]==20
  assert result_2["degredation"]==4.6/1000*num_cycles+(0.5/100)/(365*24) * 2
  assert b.capacity == 40-result_1["degredation"]-result_2["degredation"]
  assert b.currentEnergy == 40-30+20

# ----------------------- cluster tests -----------------------

def test_1_cluster():
  pass