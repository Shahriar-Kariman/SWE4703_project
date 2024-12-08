from battery import battery

# Honestly I think this one battery test alone is pretty worthless
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
