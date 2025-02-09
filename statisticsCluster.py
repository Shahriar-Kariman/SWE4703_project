import pandas as pd

class StatisticsCluster:
    def __init__(self, cluster, batteries):
        self.cluster = cluster
        self.batteries = batteries

        # Per year stats for all batteries
        self.SOHMap = {}
        self.SOHMap3 = {}
        self.profit1Map = {}
        self.profit2Map = {}
        self.profit3Map = {}

        # Averages stats
        self.averageSOH = []
        self.averageSOH3 = []
        self.averageProfit1 = []
        self.averageProfit2 = []
        self.averageProfit3 = []

        # Initial stats maps
        for b in self.cluster.batteries:
            self.SOHMap[b.name] = [b.esitmatedSOH]
            self.SOHMap3[b.name] = [b.esitmatedSOH]
            self.profit1Map[b.name] = [0]
            self.profit2Map[b.name] = [0]
            self.profit3Map[b.name] = [0]

    def updateClusterStats(self):
        for b in self.cluster.batteries:
            self.SOHMap[b.name].append(b.esitmatedSOH)
            self.profit1Map[b.name].append(b.profit1)
            self.profit2Map[b.name].append(b.profit2)

    def updateSingularStats(self):
        for b in self.batteries:
            self.SOHMap3[b.name].append(b.esitmatedSOH)
            self.profit3Map[b.name].append(b.profit3)

    def updateAverages(self):
        for b in self.cluster.batteries:
            self.averageSOH.append((self.SOHMap[b.name][0] - self.SOHMap[b.name][-1])/len(self.SOHMap[b.name]))
            self.averageSOH3.append((self.SOHMap3[b.name][0] - self.SOHMap3[b.name][-1])/len(self.SOHMap3[b.name]))
            self.averageProfit1.append((self.profit1Map[b.name][-1]) / len(self.profit1Map[b.name]))
            self.averageProfit2.append((self.profit2Map[b.name][-1]) / len(self.profit2Map[b.name]))
            self.averageProfit3.append((self.profit3Map[b.name][-1]) / len(self.profit3Map[b.name]))

    def getDfByBattery(self):
    # Create a list to hold rows
        rows = []

        # Collect average stats
        averageSOHData1 = self.averageSOH
        averageSOHData3 = self.averageSOH3
        averageProfit1Data = self.averageProfit1
        averageProfit2Data = self.averageProfit2
        averageProfit3Data = self.averageProfit3

        # Loop through batteries to populate the rows
        for i, b in enumerate(self.cluster.batteries):
            rows.append([
                b.name,
                b.id,
                b.originalCapacity,
                b.originalCapacity * b.initialSOH,
                b.initialSOH,
                b.esitmatedSOH,
                self.batteries[i].esitmatedSOH,
                averageProfit1Data[i],
                averageProfit2Data[i],
                averageProfit3Data[i],
                averageSOHData1[i],
                averageSOHData3[i],
            ])

        # Convert rows to a DataFrame
        df = pd.DataFrame(
            rows,
            columns=[
                "Name",
                "ID",
                "Original Capacity (kWh)",
                "Starting Capacity (kWh)",
                "Initial SOH (%)" ,
                "Final SOH (Cluster, %)" ,
                "Final SOH (Single User, %)" ,
                "Average Yearly Profit (Model 1, $)",
                "Average Yearly Profit (Model 2, $)",
                "Average Yearly Profit (Single User, $)",
                "Average Yearly Cluster SOH Decrease (%)" ,
                "Average Yearly Single User SOH Decrease (%)",
            ],
        )

        return df


