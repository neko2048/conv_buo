import numpy as np
import numpy as np
from numpy import ma
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import scipy.ndimage.filters as filters
import sys
##### import self-defined lib #####
from nclcmaps import nclcmap
#sys.path.append('../code/')
from initiate import *

class Convection():
    def __init__(self, tidx):
        self.xc, self.yc, self.zc = xc, yc, zc
        self.zz = zz
        self.xb, self.yb, self.zb = xb, yb, zb
        self.thmo = load_data(case_name, "Thermodynamic", idx=tidx)
        self.dyna = load_data(case_name, "Dynamic", idx=tidx)
        self.tvbuoyancy = gen_tv_buoyancy(data=self.thmo, edge_arg=set_axisarg) # shape: (k, j, i)

    def get3Dcore(self):
        w = cut_edge(self.dyna["w"], set_axisarg) # choose for xy now
        wc = np.array([w[0]] + [xw for xw in (w[1:]+w[:-1])/2]) # z level same as the one with theta
        qc = cut_edge(self.thmo["qc"], set_axisarg)

        core3DMask = np.logical_and(self.tvbuoyancy > 0, qc > 0)
        core3DMask = np.logical_and(core3DMask, qc > 0)
        return core3DMask

    def get3Dshell(self):
        qc = cut_edge(self.thmo["qc"], set_axisarg)
        shell3DMask = np.array(qc > 0, dtype=int) - np.array(self.core3DMask, dtype=int)
        return shell3DMask

    def getCorePlanView(self):
        corePlanView = np.sum(self.core3DMask, axis=0)
        return corePlanView

    def getCoreMax(self, numGrid=20, threshold=5):
        numGrid += 1 # the boundary counts
        xbsubGrid = np.linspace(self.xb[0], self.xb[-1], numGrid)
        ybsubGrid = np.linspace(self.yb[0], self.yb[-1], numGrid)
        CoreMaxPosition = np.zeros(self.corePlanView.shape)
        for j in range(len(xbsubGrid)-1):
            for i in range(len(ybsubGrid)-1):
                xsubGridStart = np.argmin(abs(self.xc - xbsubGrid[j]))
                xsubGridEnd = np.argmin(abs(self.xc - xbsubGrid[j+1]))
                ysubGridStart = np.argmin(abs(self.yc - ybsubGrid[i]))
                ysubGridEnd = np.argmin(abs(self.yc - ybsubGrid[i+1]))
                
                subGridCoreMaxValue = np.max(self.corePlanView[ysubGridStart:ysubGridEnd+1, xsubGridStart:xsubGridEnd+1])
                subGridCoreMinValue = np.min(self.corePlanView[ysubGridStart:ysubGridEnd+1, xsubGridStart:xsubGridEnd+1])
                if (subGridCoreMaxValue - subGridCoreMinValue > threshold):
                    subGridMaxPosition = (self.corePlanView[ysubGridStart:ysubGridEnd+1, xsubGridStart:xsubGridEnd+1] == subGridCoreMaxValue)
                    subGridMaxPosition = np.array(subGridMaxPosition, dtype=int)
                    CoreMaxPosition[ysubGridStart:ysubGridEnd+1, xsubGridStart:xsubGridEnd+1] += subGridMaxPosition
        return CoreMaxPosition


        #coreMaxValue = filters.maximum_filter(self.corePlanView, neighbourhood_size)
        #coreMax = (self.corePlanView == coreMaxValue)
        #coreMinValue = filters.minimum_filter(self.corePlanView, neighbourhood_size)
        #diff = ((coreMaxValue - coreMinValue) >= threshold)
        #coreMax[diff == 0] = 0
        #return coreMax

if __name__ == "__main__":
    for i in range(tidx, tidx+length):
        convection = Convection(tidx=i)
        convection.core3DMask = convection.get3Dcore()
        convection.corePlanView = convection.getCorePlanView()
        convection.CoreMaxPosition = convection.getCoreMax()
        # =====testing region=====
        pcolormesh(xb, yb, convection.corePlanView)
        colorbar()
        xx, yy = np.meshgrid(xc, yc)
        scatter(xx, yy, convection.CoreMaxPosition, 'red')
        numGrid = 20
        xbsubGrid = np.linspace(convection.xb[0], convection.xb[-1], numGrid)
        ybsubGrid = np.linspace(convection.yb[0], convection.yb[-1], numGrid)
        xx, yy = np.meshgrid(xbsubGrid, ybsubGrid)
        pcolormesh(xx, yy, np.full(shape=(yy.shape[0]-1, yy.shape[1]-1), fill_value=1), facecolor='none', edgecolor='black', cmap="binary_r", vmax=1, alpha=0.2)
        savefig("test{}.jpg".format(i), dpi=300)
        # =====testing region=====
        
        # ========== drawing options ========== #
        output_string = "task {START} -> {NOW} -> {END} ({P} %)"\
                        .format(START=tidx, NOW=i, END=tidx+length-1, P=((i - tidx + 1)/(length)*100))
        print(output_string)

