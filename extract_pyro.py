#!/usr/bin/python
import re
import time
import fileinput
import sys, getopt

import datetime as dt

# This stops error -32 when piping into head or tail
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

import codecs
sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')

name = ''  # this is the header

try:
    opts,args = getopt.getopt(sys.argv[1:],"hc:n:st:",["help","column=","name=","string"])
except getopt.GetoptError as err:
    print(str(err))
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
    print("ERROR : columns not set ")
    exit(1)


# set the refernce time
time0 = dt.datetime.strptime( t0,"%d/%m/%y %H:%M:%S")

# Read a date/time from the Oxygen data
data_found = False 

for line in fileinput.sys.stdin:
    a = re.split('\t',line)

    if len(a)<2 :
        continue

    if data_found : 
        time1 = dt.datetime.strptime("{} {}".format(a[0],a[1]), "%d/%m/%Y %H:%M:%S" )

        # calculate the difference in days
        time = (time1-time0)/dt.timedelta(days=1)

        # save the variable
        if string :
            var = a[col+1]
            var.replace("\n","")
            if( len(var)>1):
                print('{0:8.5f} "{1:s}"'.format(time,var.replace("\n","") ))
        else:
            try:
                var = float(a[col+1])
                print('{0:8.5f} {1:.6f}'.format( time, var ))
            except:
                print('{0:8.5f}  NA'.format( time ))

    if a[0]=="Date" and a[1]=="Time (HH:MM:SS)" :
        data_found = True



