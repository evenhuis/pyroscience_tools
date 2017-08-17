#!/usr/bin/python

import re
import time
import fileinput
import sys, getopt

from datetime import datetime as dt

# This stops error -32 when piping into head or tail
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

name = ''  # this is the header

try:
    opts,args = getopt.getopt(sys.argv[1:],"hc:n:st:",["help","column=","name=","string"])
except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)

col = -1
string=0
t0="23/09/16 00:00:00"

for o, a in opts:
    if   o == "-h":
        usage()
        exit()
    elif o == "-c":
        col = int(a)
    elif o == "-n":
        name = a
    elif o =="-s":
        string=1
    elif o =="-t":
        t0=a

if col == -1:
    print "ERROR : columns not set "
    exit(1)


# set the refernce time
b= map(int,re.split('/|-| +|:|\.',t0))
time0 = dt( b[2]+2000, b[1], b[0], b[3], b[4], b[5] )

# Read a date/time from the Oxygen data
data_found = False 

for line in fileinput.sys.stdin:
    a = re.split('\t',line)

    if len(a)<2 :
        continue

    if data_found : 
        # split the date field up
        b = re.split('/|-| +|:',a[0])
        yr =int(b[2])
        mon=int(b[1])
        day=int(b[0])

        b = re.split('/|-| +|:',a[1])
        hr =int(b[0])
        mn =int(b[1])
        sec=int(b[2])


        # make the time object
        time1 = dt( yr,  mon,  day,  hr,    mn, sec )

        # calculate the difference in days
        if( time1 < time0 ):
            time_delta = time0 - time1
            time = (time_delta.days*24*60*60-time_delta.seconds)/24./60./60.
            time =  time
        else:
            time_delta = time1 - time0
            time = (time_delta.days*24*60*60+time_delta.seconds)/24./60./60.

        # print comment
        #if len(a)>3 and len(a[2])>0 :
        #    print "#",a[2]

        # save the variable
        if string :
            var = a[col+1]
            var.replace("\n","")
            if( len(var)>1):
                print '{0} "{1:s}"'.format(time,var.replace("\n","") )
        else:
            try:
                var = float(a[col+1])
                print '{0} {1:.6f}'.format( time, var )
            except:
                print '{0}  NA'.format( time )

    if a[0]=="Date" and a[1]=="Time (HH:MM:SS)" :
        data_found = True



