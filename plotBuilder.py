from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PlotBuilderInterface:
    def getHist(self, data, name):
        dataArray = np.array(data, dtype=float)
        dataArray = dataArray[~np.isnan(dataArray)]
        
        if dataArray.size == 0:
            print(f"Немає даних для побудови гістограми: {name}")
            return Figure(dpi=100)
            
        figure = Figure(dpi=100)
        plot = figure.subplots()
        
        weights = np.ones_like(dataArray) / len(dataArray)

        calculated_bins = np.histogram_bin_edges(dataArray, bins='auto')
        
        plot.hist(
            dataArray, 
            bins=calculated_bins, 
            weights=weights,       
            edgecolor='black',     
            alpha=0.75             
        )
        
        plot.set_xlabel(name)
        plot.set_ylabel("Relative Frequency")
        
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



