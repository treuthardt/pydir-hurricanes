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
## Main
##
now=datetime.datetime.now() ## gets current date and time
version='1.0/20180319'
intern_path='/data1/patrick/PROJECTS/Hurricanes/Pictures/' #internal drive path of data
extern_path='/media/patrick/Hurricane_B/Hurricanes/Pictures/' #external drive path of data
valid_min_year=1995
valid_max_year=2005
print("\nRunning COPY_FLOAT_DIRS.PY version:", version,"\n")

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
def look_for_float_dirs(input):
    return

##
## Main
##
year_choice=input("\nSelect year from 1995 - 2005: ") #ask user which year to process

analyze_year(year_choice) #test year choice
