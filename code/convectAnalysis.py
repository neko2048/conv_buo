import numpy as np
import numpy as np
from numpy import ma
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys
##### import self-defined lib #####
from nclcmaps import nclcmap
sys.path.append('../code/')
from initiate import *

class Convection()
    def __init__(self, tidx):
        self.thmo = load_data(case_name, "Thermodynamic", idx=tidx)
        self.dyna = load_data(case_name, "Dynamic", idx=tidx)
        self.core3DMask = get3Dcore()

    def get3Dcore():
        w = cut_edge(self.dyna["w"], set_axisarg) # choose for xy now
        wc = np.array([w[0]] + [xw for xw in (w[1:]+w[:-1])/2]) # z level same as the one with theta
        qc = cut_edge(self.thmo["qc"], set_axisarg)

        core3DMask = np.logical_and(tvbuoyancy > 0, qc > 0)
        core3DMask = np.logical_and(core3DMask, qc > 0)
        return core3DMask

    def get3Dshell():
        self.shellMask = np.array(qc > 0, dtype=int) - np.array(self.core3DMask, dtype=int)


if __name__ == "__main__":
    for i in range(tidx, tidx+length):
        convection = Convection()
        global tvbuoyancy 
        tvbuoyancy = gen_tv_buoyancy(data=thmo, edge_arg=set_axisarg) # shape: (k, j, i)
    
        # =====testing region=====
        
        # =====testing region=====
        
        # ========== drawing options ========== #
        output_string = "task {START} -> {NOW} -> {END} ({P} %)"\
                        .format(START=tidx, NOW=i, END=tidx+length-1, P=((i - tidx + 1)/(length)*100))
        print(output_string)

