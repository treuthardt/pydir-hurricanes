#!/usr/bin/env python

##
##
## PITCH_PLOT-H1.0.PY - Plots results of p2dfft on hurricane data
##
## Version 1.0  06-Dec-2017
##
## Author: 
##   Patrick Treuthardt
##
## Description: 
##    
##
## Revision History:
##   1.0 - first attempt
##
## Requirements: pidly, pexpect, numpy, scipy
##
##

##
## Import System Libraries
##
import os # operating system interfaces
import datetime # Basic date and time types
# import pidly # control IDL within Python https://github.com/anthonyjsmith/pIDLy
import fnmatch # unix filename pattern matching
from idlpy import * # python to IDL bridge

##
## Main
##

now=datetime.datetime.now() # gets current date and time
#idl = pidly.IDL() # capitalization matters; sets idl
version='1.0/20171206'

print ""
print "pitch_plot-h1.0.py version:", version
print ""

path_01='/data1/patrick/PROJECTS/Hurricanes/Pictures/' # base path

##
## Create list of years
##
year=[] #initialize year list
for i in range(1995,2005+1): #start year,end year+1
    year.append(i) #append year to list

##
## Create list of hurricanes in specific year
##
named_hurricanes=os.listdir("/data1/patrick/PROJECTS/Hurricanes/Pictures/"+str(year[0])) #list of hurricane directories in a given year



scaler_list=list() # initialize array to add *.scaler files to

##
## Creates scaler_list array with paths to *.scaler files
##
path_01c_list=[] # initialize array for storing directory paths

for x in range(1995,2005+1): # (start_year,end_year+1)
    path_01a=path_01+str(x)+'/' # path to each year folder
    for folder1 in os.listdir(path_01a+'.'):
        path_01b=path_01a+folder1+'/' # path to each hurricane in each year
        for folder2 in os.listdir(path_01b+'.'):
            if fnmatch.fnmatch(folder2,'FLOAT'): # look for 'FLOAT' string
                path_01c=path_01b+'FLOAT/' # path to each FLOAT dir in each hurricane
                path_01c_list.append(path_01c) # create list of FLOAT paths
                for file in os.listdir(path_01c+'.'):
                    if fnmatch.fnmatch(file,'*.scaler'): # find *.scaler files
                        scaler_list.append(path_01c+file) # adds to array list of *.scaler files


#for x in scaler_list: # for each element in scaler_list array
f=open(scaler_list[0],'r') # open array element 0 for reading 
lines=f.readlines() # read lines from array f
result_01=[] # initialize scale array of nautical miles/pixel 
result_02=[] # initialize root name array of *_m* files
result_03=[] # initialize scale array of nautical miles/pixel

for y in lines: # for each line in lines
    result_01.append(y.split('\t')[1]) # '\t' for tab deliminated; [1]=2nd element in array only = scale
    result_02.append(y.split('\t')[0]) # creates array of root words for *_m*files
f.close() # close array for reading

for x in result_01: # for each line in result_01
    result_03.append(x.strip('\n')) # removes \n from scale numbers (naut. miles/pix)

file_list_01=[] # initialize array of file paths
file_path_01={} # initialize dictionary for file paths and scale factors
z=0 # initialize counter

for x in result_02: # add *_m* to root names
    for y in range(0,7): # run for m=0-6
        file_list_01.append(path_01c_list[0]+str(x)+'_m'+str(y)) # creates array of file paths
        file_path_01[path_01c_list[0]+str(x)+'_m'+str(y)]=result_03[z] # add [file path key] = scale factor value
    z=z+1 # increment counter

print file_path_01.keys()
print
print file_path_01.values()
print
print file_list_01
print
print file_list_01[1]
print
print file_path_01[file_list_01[1]]

f=open(file_list_01[1],'r')
rows=f.readlines()
f.close()

split_rows=rows[0].split()
print split_rows[3],split_rows[4]
print rows[0]

