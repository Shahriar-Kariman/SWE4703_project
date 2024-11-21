from dash import dcc
import plotly.graph_objects as go
import plotly.express as px

class Plots:
    def __init__(self, statistics):
        self.statistics = statistics

    def getPlots(self):
        graphsMap = {}

        # First do all the tabs for regular data plots
        SOHDatas1 = self.statistics.SOHMap
        SOHDatas3 = self.statistics.SOHMap3
        proFit1Datas = self.statistics.profit1Map
        proFit2Datas = self.statistics.profit2Map
        proFit3Datas = self.statistics.profit3Map

        i = 0
        x = [i for i in range(0, 11)]
        for b in self.statistics.cluster.batteries:
            key = b.name
            graph =[]

            # Plot SOH data for the user for both cluster and single user
            SOHData1 = SOHDatas1[key]
            SOHData3 = SOHDatas3[key]

            figure1=go.Figure(
                go.Scatter(
                    x=x,
                    y=SOHData1,
                    mode='lines+markers',
                    name='Cluster SOH Data',
                    line=dict(color='blue'),
                    marker=dict(color='blue'),
                )
            )

            figure1.add_trace(
                go.Scatter(
                    x=x,
                    y=SOHData3,
                    mode='lines+markers',
                    name='Single User SOH Data',
                    line=dict(color='red'),
                    marker=dict(color='red'),
                )
            )
            # append the figure to the graph
            graph.append(dcc.Graph( 
                figure=figure1                
            ))

            # Plot profit data for the user for both the two cluster profit models and single user
            proFit1Data = proFit1Datas[key]
            proFit2Data = proFit2Datas[key]
            proFit3Data = proFit3Datas[key]

            figure2=go.Figure(
                go.Scatter(
                    x=x,
                    y=proFit1Data,
                    mode='lines+markers',
                    name='Cluster Profit Model 1',
                    line=dict(color='blue'),
                    marker=dict(color='blue'),
                )
            )

            figure2.add_trace(
                go.Scatter(
                    x=x,
                    y=proFit2Data,
                    mode='lines+markers',
                    name='Cluster Profit Model 2',
                    line=dict(color='green'),
                    marker=dict(color='green'),
                )
            )

            figure2.add_trace(
                go.Scatter(
                    x=x,
                    y=proFit3Data,
                    mode='lines+markers',
                    name='Single User Profit Model',
                    line=dict(color='red'),
                    marker=dict(color='red'),
                )
            )

            # append the figure to the graph
            graph.append(dcc.Graph(
                figure=figure2
            ))

            # Add this user to the graph map using the i as a key
            graphsMap[i] = graph

            i += 1

        # Include one more tab for the average/summary data
        graph = []

        # First do the average SOH data
        self.statistics.updateAverages()
        averageSOHData1 = self.statistics.averageSOH
        averageSOHData3 = self.statistics.averageSOH3
        figure1 = go.Figure()
        figure2 = go.Figure()

        x = [b.name for b in self.statistics.cluster.batteries]

        figure1.add_trace(
            go.Bar(
                x=x,
                y=averageSOHData1,
                name='Average Cluster SOH Decrease',
                marker_color='blue'
            )
        )
        figure1.add_trace(
            go.Bar(
                x=x,
                y=averageSOHData3,
                name='Average Single User SOH Decrease',
                marker_color='red'
            )
        )

        graph.append(dcc.Graph(figure=figure1))

        # Now do the average profit data
        averageProFit1Data = self.statistics.averageProfit1
        averageProFit2Data = self.statistics.averageProfit2
        averageProFit3Data = self.statistics.averageProfit3

        figure2.add_trace(
            go.Bar(
                x=x,
                y=averageProFit1Data,
                name='Cluster Profit Model 1',
                marker_color='blue'
            )
        )
        figure2.add_trace(
            go.Bar(
                x=x,
                y=averageProFit2Data,
                name='Cluster Profit Model 2',                
                marker_color='green'
            )
        )
        figure2.add_trace(
            go.Bar(
                x=x,
                y=averageProFit3Data,
                name='Single User Profit',
                marker_color='red'
            )
        )

        graph.append(dcc.Graph(figure=figure2))

        # Finally looking at surmary / trend data
        # Get the DataFrame
        df = self.statistics.getDfByBattery()

        # Define the profit models
        profit_models = [
            "Average Profit Model 1",
            "Average Profit Model 2",
            "Average Profit Single User",
        ]

        # Create individual figures for Initial SOH vs. Average Profits
        for model in profit_models:
            fig = px.scatter(
                df,
                x="Initial SOH",
                y=model,
                labels={"y": "Average Profit", "x": "Initial SOH"},
                title=f"Initial SOH vs. {model}",
                trendline="ols",  # Ordinary Least Squares regression for trend lines
            )

            # Customize the appearance
            fig.update_traces(marker=dict(color="red" if model == "Average Profit Single User" else "blue"))
            fig.update_layout(
                xaxis_title="Initial SOH",
                yaxis_title="Average Profit",
            )

            # Append the figure to the graph array
            graph.append(dcc.Graph(figure=fig))

        # Create individual figures for Starting Capacity vs. Average Profits
        for model in profit_models:
            fig = px.scatter(
                df,
                x="Starting Capacity",
                y=model,
                labels={"y": "Average Profit", "x": "Starting Capacity"},
                title=f"Starting Capacity vs. {model}",
                trendline="ols",  # Ordinary Least Squares regression for trend lines
            )

            # Customize the appearance
            fig.update_traces(marker=dict(color="red" if model == "Average Profit Single User" else "blue"))
            fig.update_layout(
                xaxis_title="Starting Capacity",
                yaxis_title="Average Profit",
            )

            # Append the figure to the graph array
            graph.append(dcc.Graph(figure=fig))



        figure5 = go.Figure()
        averageSOHCluster = sum(df["Average Cluster SOH Decrease"])/len(df["Average Cluster SOH Decrease"])
        averageSOHSingle = sum(df["Average Single User SOH Decrease"])/len(df["Average Single User SOH Decrease"])
        figure5.add_trace(
            go.Bar(
                x=['Cluster'],
                y=[averageSOHCluster],
                name='Total Average Cluster SOH Decrease',
                marker_color='blue'
            )
        )
        figure5.add_trace(
            go.Bar(
                x=['Single User'],
                y=[averageSOHSingle],
                name='Total Average Single User SOH Decrease',                
                marker_color='red'
            )
        )

        graph.append(dcc.Graph(figure=figure5))

        graphsMap[i] = graph

        fileName = "SimulationData.xlsx"
        df.to_excel(fileName)
        
        return graphsMap
    
    
