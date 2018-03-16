#!/usr/bin/env python

##
##
## PITCH_PLOT-H2.0.PY - Plots results of p2dfft on hurricane data
##
## Version 2.0  06-Mar-2018
##
## Author: 
##   Patrick Treuthardt
##
## Description: 
##    
##
## Revision History:
##   2.0 - second attempt after completing python course
##   1.0 - first attempt
##
## Requirements: none
##
##


### Import System Libraries
import os # operating system interfaces
import datetime # Basic date and time types
import fnmatch # unix filename pattern matching
###

###
### Main
###
now=datetime.datetime.now() # gets current date and time
version='2.0/20180306'
base_path='/data1/patrick/PROJECTS/Hurricanes/Pictures/' # base path of data
begin_year=1995
end_year=2005

print()
print("pitch_plot-h2.0.py version: "+version)
print()

## Create list of years
year=[] #initialize list
for i in range(begin_year,end_year+1): #
    year.append(i) #append year to list
##

path_01="/data1/patrick/PROJECTS/Hurricanes/Pictures/"+str(year[0]) #set specifically for 1995=year[0]

## Create list of hurricanes directories in a given year
hurr_dirs=os.listdir(path_01) #makes list of hurricane directories in specific year
##

path_02=path_01+"/"+hurr_dirs[0]+"/FLOAT/" #sets first hurricane directory for a given year

## Look for *.scaler files in specific path
for file in os.listdir(path_02): #look at files in path
    if fnmatch.fnmatch(file,"*.scaler"): #find files that match *.scaler
        hurricane_scale=file #store files as variable
##

with open(path_02+hurricane_scale,'r') as f: #opens *.scaler file for reading
    scale_data=f.readlines() #reads each line of data into list
    
prefix_name=[] #initialize list of file prefixes
nm_per_pix=[] #initialize list of scales (nautical miles/pixel)
place_holder=[]
for item in scale_data:
    place_holder.append(item.strip("\n")) #remove trailing \n's

for item in place_holder:
    prefix_name.append(item.split("\t")[0]) #pulls prefixes into list
    nm_per_pix.append(item.split("\t")[1]) #pulls scales into list
print(nm_per_pix)

##### NEED TO CREATE DICTIONARY OF PREFIXES WITH SCALES#####




