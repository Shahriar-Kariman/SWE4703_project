from cluster import cluster
# from dash import Dash, dcc, html
from battery import battery
import random
from statisticsCluster import StatisticsCluster
from time_handler import time_handler
# from plots import Plots

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



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

# for b in battries:
#   print(b.esitmatedSOH)

stats = StatisticsCluster(main_cluster)

# TOU rates for each hour in Ontario
ON_PEAK = 15.8
OFF_PEAK = 7.6
MID_PEAK = 12.2
summer_day_rates = [OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, MID_PEAK, MID_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK]
winter_day_rate = [OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, ON_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, MID_PEAK, ON_PEAK, ON_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK, OFF_PEAK]

time = time_handler()

# Look at Ontario website for number of events
# 2 $ per kWh
# event is 5 hours

def simulate_day(day):
  for i in range(24):
    if not time.is_weekend():
      d = make_decision(day[i], main_cluster)
      main_cluster.share_load(d["decision"], d["amount"], 1, day[i])
    else:
      main_cluster.weekend_calender_deg(1)
      break
  time.end_day()

def simulate_day_battery(day):
  for batt in battries:
    for i in range(24):
        if not time.is_weekend():
            d = make_decision_battery(day[i], batt)
            result = batt.transfer_energy(1, d)
            batt.add_profit_3(result["energy_transfer"], day[i], d, 1)
        else:
            batt.weekend_calender_deg(1)
            break
    time.end_day()
    

def simulate_summer():
  # summer is 184 days (May 1st to Oct 31st)
  for i in range(184):
    simulate_day(summer_day_rates)

def simulate_summer_battery():
  # summer is 184 days (May 1st to Oct 31st)
  for i in range(184):
    simulate_day_battery(summer_day_rates)


def simulate_winter():
  # winter is 182 days (Nov 1st to April 30th)
  for i in range(181):
    simulate_day(winter_day_rate)

def simulate_winter_battery():
  # winter is 182 days (Nov 1st to April 30th)
  for i in range(181):
    simulate_day_battery(winter_day_rate)
  

def simulate_year():
  simulate_summer()
  simulate_winter()

def simulate_year_battery():
  simulate_summer_battery()
  simulate_winter_battery()

def make_decision(rate, main_cluster):
  decision = "idle"
  energy_amount = 0 # kW
  if rate == ON_PEAK:
    decision = "discharge"
    if main_cluster.total_SOC>80:
      energy_amount = 150
    elif main_cluster.total_SOC>70:
      energy_amount = 100
    else:
      energy_amount = 80
  elif rate == OFF_PEAK:
    decision = "charge"
    if main_cluster.total_SOC<25:
      energy_amount = 70
    elif main_cluster.total_SOC<50:
      energy_amount = 50
    else:
      energy_amount = 30
  else:
    if main_cluster.total_SOC>50:
      decision = "discharge"
      energy_amount = 70
  return {"decision": decision, "amount": energy_amount}

def make_decision_battery(rate, battery):
  decision = "idle"
  if rate == ON_PEAK:
    decision = "discharge"
  elif rate == OFF_PEAK:
    decision = "charge"
  else:
    if battery.currentSOC>50:
      decision = "discharge"
  return decision


for i in range(10):
  simulate_year()
  print("year", i)
  stats.updateClusterStats()

time = time_handler()
for i in range(10):
  simulate_year_battery()
  print("year", i)
  stats.updateSingularStats(battries)



total_profit1 = 0
total_profit2 = 0
total_profit3 = 0
for b in main_cluster.batteries:
  total_profit1 += b.profit1
  total_profit2 += b.profit2
  print("profit 1", b.profit1, "profit 2", b.profit2, "state of health", b.esitmatedSOH)
print("total profit 1", total_profit1, "total profit 2", total_profit2)

for b in battries:
  total_profit3 += b.profit3
  print("profit 3", b.profit3, "state of health", b.esitmatedSOH)
print("total profit 3", total_profit3)

# batteries = main_cluster.batteries
# plots = Plots(stats).getPlots()

# app = Dash(__name__, external_stylesheets=external_stylesheets)
# app.layout = html.Div([
#     dcc.Tabs([
#         dcc.Tab(
#             label=batteries[i].name,
#             children=[
#                 html.Div(
#                     dcc.Graph(
#                         id=f'plot-{i}-{j}',  # Unique ID for each graph
#                         figure=plots[i][j].figure,  # Ensure plots[i][j] is a valid Graph component
#                         style={'width': '1500px', 'height': '1000px'}  # Increased size for square graphs
#                     )
#                 ) for j in range(len(plots[i]))  # Iterate over the graphs in plots[i]
#             ]
#         ) for i in range(len(batteries))
#     ] + [
#         dcc.Tab(
#             label="Summary",
#             children=[
#                 html.Div(
#                     dcc.Graph(
#                         id=f'summary-plot-{j}',  # Unique ID for each graph in summary
#                         figure=plots[32][j].figure,  # Ensure plots[32][j] is a valid Graph component
#                         style={'width': '1500px', 'height': '1000px'}  # Increased size for square graphs
#                     )
#                 ) for j in range(len(plots[32]))  # Iterate over the graphs in plots[32]
#             ]
#         )
#     ])
# ])



# if __name__ == '__main__':
#     app.run(debug=True)
