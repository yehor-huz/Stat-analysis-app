from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PlotBuilderInterface:
    def getHist(self, data, name):
        dataArray = np.array(data)
        figure = Figure(dpi=100)
        plot = figure.subplots()
        plot.hist(dataArray, weights=np.zeros_like(dataArray) + 1. / dataArray.size, bins=np.arange(min(data), max(data) + 1, 1))
        plot.set_xlabel(name)
        plot.set_ylabel("Frequency")
        return figure
    
    def getScatter(self, data, names):
        dataArray = np.array(data)
        figure = Figure(dpi=100)
        plot = figure.subplots()
        plot.scatter(dataArray[0], dataArray[1])
        plot.set_xlabel(names[0])
        plot.set_ylabel(names[1])
        plot.legend()
        return figure
    
    def getPairplot(self, dataFrame):
        grid = sns.pairplot(dataFrame, diag_kind='auto')
        figure = grid.figure
        figure.set_dpi(100)
        return figure



