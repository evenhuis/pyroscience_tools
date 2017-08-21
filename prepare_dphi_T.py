#!/usr/bin/python
import numpy as np
import fileinput
import sys, getopt
import re

# This stops error -32 when piping into head or tail
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

import codecs
sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')

dphi_range=[10,30 ]
temp_range=[15,30]
nc=1

try:
    opts,args = getopt.getopt(sys.argv[1:],"hc:t:d:",["help","temp=","dphi="])
except getopt.GetoptError as err:
    sys.exit(2)

for o, a in opts:
    if   o == "-h":
        usage()
        exit()
    elif o == "-c":
        nc =int(a)
    elif o == "-t":
        temp_range = list(map(int,a.split(":")))
    elif o == "-d":
        dphi_range = list(map(int,a.split(":")))
    else : 
        pass


# reads in the dphi and T from ranges from a pyrosciuence


# creates regular grid for dphi and T 
# this gets fed into the spreadsheet along with the header info

mode=None
cals = np.array( [4,14] )

for line in fileinput.sys.stdin:
        a = re.split('\t',line)
        
        if a[0]=="Settings:"   : 
            mode="Set" 
            ns = 0
        if a[0]=="Calibration:": 
            ns = 0
            mode="Cal"
        if a[0]=="Temp."       : mode=None
        if a[0]=="Data"        : mode=None
        
        if mode=="Cal":
        
            if( ns==nc ):
                for i in range(3,7):
                    print(a[i])
                print()
                print()
                for i in range(8,10):
                    print(a[i])
                print()
                print(a[12])
                print(a[10])
                print(a[11])
                print(a[13])
                print(a[14])
                print(a[17])
            ns=ns+1

        
# ouput the dphi_T grid
temp_x = np.linspace( temp_range[0], temp_range[1], 11 )
dphi_y = np.linspace( dphi_range[0], dphi_range[1], 11 )

temp_xy, dphi_xy = np.meshgrid( temp_x, dphi_y )
f = open("dphi_temp.txt",'w')
nx,ny = np.shape(temp_xy)
for ix in range(nx):
    for iy in range(ny):
        f.write("{:.3f}\t{:.3f}\n".format( dphi_xy[ix,iy],temp_xy[ix,iy]))
f.close()



