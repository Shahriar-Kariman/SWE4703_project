from dash import Dash, dcc, html
import random
from cluster import cluster_shawn
from battery import battery
from statisticsCluster import StatisticsCluster
from plots import Plots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)



# Initialize the main cluster with a maximum of 32 batteries
main_cluster = cluster_shawn(max_num_batteries=32)

# Create and add 32 dummy batteries to the main cluster
for i in range(32):
    name = f"Battery_{i+1}"
    initialSOH = random.uniform(0.8, 1.0)  # SOH starts between 80% and 100%
    battery_id = i
    capacity = random.randint(30, 50)  # Capacity between 30 and 50 kWh
    startSoc = random.randint(40, 60)  # Starting SOC between 40% and 60%
    b = battery(name, initialSOH, battery_id, capacity, startSoc)
    main_cluster.add_battery(b)

# Initialize the singular cluster with a maximum of 32 batteries
singular_cluster = cluster_shawn(max_num_batteries=32)

# Create and add 32 dummy batteries to the singular cluster
for i in range(32):
    name = f"Battery_{i+1}"
    initialSOH = random.uniform(0.7, 0.9)  # SOH starts between 70% and 90%
    battery_id = i
    capacity = random.randint(25, 45)  # Capacity between 25 and 45 kWh
    startSoc = random.randint(50, 70)  # Starting SOC between 50% and 70%
    b = battery(name, initialSOH, battery_id, capacity, startSoc)
    singular_cluster.add_battery(b)

# Create StatisticsCluster instances for each simulation
main_stats = StatisticsCluster(main_cluster)


# Simulate 10 years for the main cluster
for year in range(10):
    for b in main_cluster.batteries:
        # SOH decreases by 1-3% per year
        b.esitmatedSOH -= random.uniform(0.01, 0.03)
        b.esitmatedSOH = max(b.esitmatedSOH, 0.2)  # SOH cannot drop below 20%

        # Profits for different models
        b.profit1 += random.uniform(100, 200)
        b.profit2 += random.uniform(150, 250)
        b.profit3 += random.uniform(200, 300)

    # Update main cluster stats
    main_stats.updateClusterStats()

# Simulate 10 years for the singular cluster
for year in range(10):
    for b in singular_cluster.batteries:
        # SOH decreases by 2-4% per year (different parameter)
        b.esitmatedSOH -= random.uniform(0.02, 0.04)
        b.esitmatedSOH = max(b.esitmatedSOH, 0.15)  # SOH cannot drop below 15%

        # Profits for model 3 only (different range)
        b.profit3 += random.uniform(250, 350)

    # Update singular cluster stats
    main_stats.updateSingularStats(singular_cluster)

# Update averages for both simulations
batteries = main_cluster.batteries
plots = Plots(main_stats).getPlots()

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(
            label=batteries[i].name,
            children=[
                html.Div(
                    dcc.Graph(
                        id=f'plot-{i}-{j}',  # Unique ID for each graph
                        figure=plots[i][j].figure,  # Ensure plots[i][j] is a valid Graph component
                        style={'width': '1500px', 'height': '1000px'}  # Increased size for square graphs
                    )
                ) for j in range(len(plots[i]))  # Iterate over the graphs in plots[i]
            ]
        ) for i in range(len(batteries))
    ] + [
        dcc.Tab(
            label="Summary",
            children=[
                html.Div(
                    dcc.Graph(
                        id=f'summary-plot-{j}',  # Unique ID for each graph in summary
                        figure=plots[32][j].figure,  # Ensure plots[32][j] is a valid Graph component
                        style={'width': '1500px', 'height': '1000px'}  # Increased size for square graphs
                    )
                ) for j in range(len(plots[32]))  # Iterate over the graphs in plots[32]
            ]
        )
    ])
])



if __name__ == '__main__':
    app.run(debug=True)
