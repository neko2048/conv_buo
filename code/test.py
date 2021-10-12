import numpy as np
import netCDF4 
# ========== self defined =========
from data_load import load_data


if __name__ == "__main__":
    case_name = str(input())
    home_dir = "/home/atmenu10246/"

    data = load_data(case_name, "Thermodynamic", idx=0)

    xc, yc = np.array(diag['xc']), np.array(diag['yc']), 
    zc = np.array(diag['zc'])

    xmin, xmax= 40800, 41200
    