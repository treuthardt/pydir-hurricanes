#!/usr/bin/env python
##
##
## H-AVG_RUN.PY - Sets up and plots SQ*_m[0-6] result files from p2dfft.
##
## Version 1.0  23-Mar-2018
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
import stat ## Allow chmod status changes
import shutil ## High level file operations
#import matplotlib.pyplot as plt ## Allows plotting

##
## Global Variables
##
##   NOW: current date and time
##   VERSION: latest version number of this program
##   ROOT_DIR: root directory for processing the data
##   VALID_MIN_YR: min year directory
##   VALID_MAX_YR: max year directory
##   VERBOSE: print out what is happening as program runs
##

NOW=datetime.datetime.now() 
VERSION="1.0/20180323"
ROOT_DIR="/data1/patrick/PROJECTS/Hurricanes/Pictures/"
VALID_MIN_YR=1995
VALID_MAX_YR=2005
VERBOSE=0

##
## Let's go!
##

print("\nRunning H-AVG_RUN.PY version:", VERSION,"\n")

##
## Check if year choice is valid. If not, sends error message and kicks from
##   system.
##

def analyze_yr(choice_in):
    if int(choice_in) > VALID_MAX_YR or int(choice_in) < VALID_MIN_YR:
        sys.exit("ERROR: "+choice_in+" is not a vaild option.\n") #invalid choice boots from program
    print()
    return

##
## First, create a list of all the directories we will dive into
##

def make_dir_list(yr_choice_in):
    yr_dir=ROOT_DIR+str(yr_choice_in)+"/"
    hurr_dirs=os.listdir(yr_dir) #list all hurricane dirs in a year
    hurr_dirs.sort()
    float_dirs_out=[]
    for item01 in hurr_dirs: #check each hurricane dir
        contents_list=os.listdir(yr_dir+item01)
        for item02 in contents_list: #list contents of hurricane dir
            if fnmatch.fnmatch(item02,"FLOAT"): #check if FLOAT dir exists
                float_dirs_out.append(yr_dir+item01+"/FLOAT/") #add FLOAT to list
    float_dirs_out.sort()
    if VERBOSE != 0:
        print()
        print("Year directory: ",yr_dir)
        print()
        print("Hurricane directories: ",hurr_dirs)
        print()
        print("FLOAT directories: ",float_dirs_out)
    return float_dirs_out

##
## Go through each directory and copy original *.scaler files to
##   *.scaler_old files.
##

def scaler_copy(dir_list_in):
    scaler_path_out=[]
    for item01 in dir_list_in: #run for each hurricane directory
        contents_list=os.listdir(item01)
        skip=0
        for item02 in contents_list: #begin looking for *.scaler_old in dir
            if fnmatch.fnmatch(item02,"*.scaler_old"): #will skip if *old exists
                skip=1 #tag *.scaler_old already exits
                print("ATTENTION: "+item02+" already exists")
        if skip == 0: #begin coping if *.scaler_old doesn't already exist
            for item03 in contents_list: #run for each file in directory
                if fnmatch.fnmatch(item03,"*.scaler"): #find *.scaler file
#                    copyfile(item01+item03,item01+item03+"_old") #copy to diff file
                    print("Copied "+item03+" --> "+item03+"_old")
        for item04 in contents_list: #begin making path list of *.scaler files
            if fnmatch.fnmatch(item04,"*.scaler"): #find scaler file again
                scaler_path_out.append(item01+item04) #add path to list
    scaler_path_out.sort()
    print()
    return scaler_path_out

##
## Change *.scaler files so that each entry begins with SQ_*.
##

!!!!Need to change the contents of the file so that it has SQ_ in the front
def scaler_change(scaler_path_in):
    for item01 in scaler_path_in:
        with open(item01,"r") as f:
            contents_list=f.read()
        print(contents_list)
    print()
    return

##
## Next, go through each directory and extract the root string of the
##   SQ*_m[0-6] files and use that for basis of running h-avg.py.
##   The run string should be something like:
##   h-avg.py -c 1 -n Tanya.scaler -o SQ_19951101_174513_fix_results.txt SQ_19951101_174513_fix
##

def extract_root_string(input):
    return

##
## Finally, create a *.runme file to launch in bash to get out results and plots
##

def create_runme(input):
    return

##
## Main
##

yr_choice=input("\nSelect year from "+str(VALID_MIN_YR)+" - "+str(VALID_MAX_YR)+": ") #ask user which year to process

analyze_yr(yr_choice) #check if year is valid

dir_list=make_dir_list(yr_choice) #create list of dirs to dive into

scaler_path=scaler_copy(dir_list) #copy *.scaler files

scaler_change(scaler_path)
