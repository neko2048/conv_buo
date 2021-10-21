import numpy as np
import netCDF4

homeDir = "/home/atmenu10246/"
case_name = "diurnal_prescribed"
category = "Thermodynamic"
set_axis = {
"xmin": 35000, 
"xmax": 50000, 
"ymin": 30000, 
"ymax": 45000, 
"zmin": 0, 
"zmax": 13000, 
}

def load_data(case_name, category, idx):
    try: 
        nc_location = homeDir + "VVM/DATA/{CN}/archive/{CN}.L.{CG}-{IDX:06d}.nc"\
                       .format(CN=case_name, CG=category, IDX=idx)
        data = netCDF4.Dataset(nc_location)
    except FileNotFoundError:
        nc_location = homeDir + "VVM/DATA/{CN}/archive/exp.L.{CG}-{IDX:06d}.nc"\
                       .format(CN=case_name, CG=category, IDX=idx)
        data = netCDF4.Dataset(nc_location)
    return data

class Coordinate:
    def __init__(self, case_name, category, tidx=0):
        self.xc, self.yc, self.zc, self.zz = self.getOriginAxis(case_name, tidx)
        self.setGlobalBoundAxis()
        self.dx, self.dy, self.dz = self.getAxisGradient()
        self.xb, self.yb, self.zb = self.setGridBoundAxis()

    def getOriginAxis(self, case_name, tidx=0):
        sampleNCdata = load_data(case_name, "Thermodynamic", idx=tidx)
        xc = np.array(sampleNCdata['xc'])
        yc = np.array(sampleNCdata['yc'])
        zc = np.array(sampleNCdata['zc'])
        zz = np.loadtxt("../constants/{CN}_z.txt".format(CN=case_name), skiprows=2)[:-1, 1] # W level (k, )
        return xc, yc, zc, zz

    def setGlobalBoundAxis(self):
        global set_axis
        set_axisarg = {
            "argxmin": np.argmin(np.abs(self.xc - set_axis['xmin'])), 
            "argxmax": np.argmin(np.abs(self.xc - set_axis['xmax'])), 
            "argymin": np.argmin(np.abs(self.yc - set_axis['ymin'])), 
            "argymax": np.argmin(np.abs(self.yc - set_axis['ymax'])), 
            "argzmin": np.argmin(np.abs(self.zc - set_axis['zmin'])), 
            "argzmax": np.argmin(np.abs(self.zc - set_axis['zmax'])), 
        }
        self.xc = self.xc[set_axisarg["argxmin"]:set_axisarg["argxmax"]+1]
        self.yc = self.yc[set_axisarg["argymin"]:set_axisarg["argymax"]+1]
        self.zc = self.zc[set_axisarg["argzmin"]:set_axisarg["argzmax"]+1]
        self.zz = self.zz[set_axisarg["argzmin"]:set_axisarg["argzmax"]+1]

    def getAxisGradient(self):
        dx, dy, dz = np.gradient(self.xc), np.gradient(self.yc), np.gradient(self.zc) # (i, ), (j, ), (k, )
        return dx, dy, dz

    def setGridBoundAxis(self):
        xb = (np.array([self.xc[0] - self.dx[0]] + [x for x in self.xc]) + np.array([x for x in self.xc] + [self.xc[-1] + self.dx[-1]])) / 2 
        yb = (np.array([self.yc[0] - self.dy[0]] + [y for y in self.yc]) + np.array([y for y in self.yc] + [self.yc[-1] + self.dy[-1]])) / 2 
        zb = np.array([self.zc[0], (self.zc[0] + self.zc[1]) / 2] + [z for z in self.zz[1:]])
        return xb, yb, zb

class DrawSystem:
    def __init__(self, case_name, category, tidx):
        self.homeDir = "/home/atmenu10246/"
        self.ncdata = load_data(case_name, category, tidx)
        self.axis = Coordinate(case_name, category)

    def drawCloud(self, profile):
        xc = self.axis.xc
        xarg = np.argmin(np.abs(xc  - profile))
        # rain
        cmap = nclcmap('BrownBlue12')
        colors = cm.Blues(np.linspace(0.3, 1))
        cmap = LinearSegmentedColormap.from_list('name', colors)
        qr = cut_edge(thmo["qr"], set_axisarg)[:, :, xarg]
        qr = ma.masked_array(qr, qr<=1e-6)#5e-6)
        pcolormesh(yb, zb, qr, cmap=cmap, vmin=0, vmax=0.005)
        #colorbar()
        # cloud
        colors = cm.Greys(np.hstack([np.linspace(0.5, 0.75, 95)]))
        cmap = LinearSegmentedColormap.from_list('name', colors)
        qc = cut_edge(thmo["qc"], set_axisarg)[:, :, xarg]
        qc = ma.masked_array(qc, qc<=0)
        pcolormesh(yb, zb, qc, cmap=cmap, vmin=0, vmax=0.005)
        #colorbar()

        # wind information
        y, z = np.meshgrid(yc, zz)
        w = cut_edge(dyna["w"], set_axisarg)[:, :, xarg]
        pw = w > 0
        quiver(y[pw], z[pw], 0, w[pw], color='red', alpha=0.2)
        nw = w < 0 
        quiver(y[nw], z[nw], 0, w[nw], color='blue', alpha=0.2)

        title("TIME: {T:06d}".format(T=i*2))
        savefig("cloud_{T:06d}.jpg".format(T=i), dpi=200)
        clf()


drawpart = DrawSystem(case_name, category, tidx=0)
