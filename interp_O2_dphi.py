import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import RectBivariateSpline, UnivariateSpline


# set up the spline function
data = np.genfromtxt('dphi_temp_conc.txt')

dphi_val = np.unique( data[:,0] )
T_val    = np.unique( data[:,1] )

nphi = len(dphi_val)
nT   = len(T_val)

dphi_grid = np.reshape( data[:,0], [nphi, nT ] )
temp_grid = np.reshape( data[:,1], [nphi, nT ] )
C_cal     = np.reshape( data[:,2], [nphi, nT ] )

C_spline = RectBivariateSpline( dphi_grid[:,0], temp_grid[0,:], C_cal )


# read in the O2 data
O2_raw = np.genfromtxt("dphi.txt")


# read in the temp data
temp = np.genfromtxt("temp.txt")
temp_spline = UnivariateSpline( temp[:,0], temp[:,1], s=0.1  )

#fh = open("O2_cor.txt","w")
for time,dphi in O2_raw:
    temp = temp_spline( time )
    print("{} {} {} ".format( time, C_spline(dphi,temp)[0,0], temp   ) )#, file=fh )
#fh.close()


