#!/usr/bin/env python
##
##
## COPY_FLOAT_DIRS.PY - Copies FLOAT directories from Hurricane_B to WOPR:/data1
##
## Version 1.0  19-Mar-2018
##
## Author: 
##   Patrick Treuthardt
##
## Description: 
##
## Revision History:
##   1.0 - first attempt
##
## Requirements: None
##

##
## Import System Libraries
##
import os ## operating system interfaces
import fnmatch ## unix filename pattern matching
import datetime ## Basic date and time types
import os.path ## Common pathname manipulations
import sys ## System-specific parameters and functions

##
## Global Variables
##
now=datetime.datetime.now() ## gets current date and time
version='1.0/20180319'
intern_path='/data1/patrick/PROJECTS/Hurricanes/Pictures/' #internal drive path of data
extern_path='/media/patrick/Hurricane_B/Hurricanes/Pictures/' #external drive path of data
valid_min_year=1995
valid_max_year=2005

print("\nRunning COPY_FLOAT_DIRS.PY version:", version,"\n") #Let's go!

##
## Check if year choice is valid
##
def analyze_year(choice_input):
    if int(choice_input) > valid_max_year or int(choice_input) < valid_min_year:
        sys.exit("ERROR: "+choice_input+" is not a vaild option.\n") #invalid choice boots from program
    return

##
##
##
def look_for_float_dirs(year_input):
    path_01=extern_path+str(year_input)+"/" #path to selected year
    path_02=[] #create empty list
    path_03=[]
#    dir_suffix=[]
    hurr_dirs=os.listdir(path_01) #list directories
    for i in hurr_dirs: 
        if fnmatch.fnmatch(i,str(year_input)+"*"): #look for usable dirs
            path_02.append(path_01+i+"/") #create list of usable dirs
 #           dir_suffix.append(i+"/")
 #   print(dir_suffix)
 #   print()
    for j in path_02:
        dirs_in_hurr=os.listdir(j) #list contents of hurr dir
        for k in dirs_in_hurr: #look at each element in list
            if fnmatch.fnmatch(k,"FLOAT"): #if FLOAT is in dir
                path_03.append(j+"FLOAT/") #create list of dirs with FLOAT
    print(path_03)
    print()
    
    return

##
## Main
##
year_choice=input("\nSelect year from "+str(valid_min_year)+" - "+str(valid_max_year)+": ") #ask user which year to process
print()
analyze_year(year_choice) #test year choice
look_for_float_dirs(year_choice)
