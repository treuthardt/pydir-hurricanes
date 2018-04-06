#!/usr/bin/env python
##
##
## COLLECT_DATA.PY - Pulls preferred mode, pitch angle, and standard deviation
##                   from each hurricane's *_results.txt file.
##
## Version 1.0  06-Apr-2018
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
from shutil import copyfile ## High level file operations
#import matplotlib.pyplot as plt ## Allows plotting

##
## Global Variables
##
##   NOW: current date and time
##   VERSION: latest version number of this program
##   DATA_DIR: directory where compiled data is stored
##   ROOT_DIR: root directory for processing the data
##   RUNME_DIR: directory holding *.runme text files to run in bash
##   VALID_MIN_YR: min year directory
##   VALID_MAX_YR: max year directory
##   VERBOSE: print out what is happening as program runs
##

NOW=datetime.datetime.now() 
VERSION="1.0/20180406"
DATA_DIR="/data1/patrick/PROJECTS/Hurricanes/"
ROOT_DIR=DATA_DIR+"Pictures/"
RUNME_DIR=DATA_DIR+"runme/"
VALID_MIN_YR=1995
VALID_MAX_YR=2005
VERBOSE=0

##
## Let's go!
##

print("\nRunning COLLECT_DATA.PY version:", VERSION,"\n")

##
## Check if year choices are valid. If not, sends error message and kicks from
##   system.
##

def analyze_yr(start_choice_in,end_choice_in):
    if int(start_choice_in) > VALID_MAX_YR or int(start_choice_in) < VALID_MIN_YR or int(end_choice_in) > VALID_MAX_YR or int(end_choice_in) < VALID_MIN_YR or end_choice_in < start_choice_in:
        sys.exit("ERROR: At least one selection was not vaild.\n") #invalid choice boots from program
    print()
    return()

##
## Generate a list of years in the range that has been selected
##

def generate_yr_list(start_choice_in,end_choice_in):
    year_list=list(range(int(start_choice_in),int(end_choice_in)+1))   
    return(year_list)

##
## First, create a list of all the directories we will dive into
##

def make_dir_list(year_list_in):
    print("Gathering list of directories...")
    float_dirs_out=[]
    for year in year_list_in:
        yr_dir=ROOT_DIR+str(year)+"/"
        hurr_dirs=os.listdir(yr_dir) #list all hurricane dirs in a year
        hurr_dirs.sort()
        for item01 in hurr_dirs: #check each hurricane dir
            contents_list=os.listdir(yr_dir+item01)
            for item02 in contents_list: #list contents of hurricane dir
                if fnmatch.fnmatch(item02,"FLOAT"): #check if FLOAT dir exists
                    float_dirs_out.append(yr_dir+item01+"/FLOAT/") #add FLOAT to list
                    if VERBOSE != 0:
                        print()
                        print("Year directory: ",yr_dir)
                        print()
                        print("Hurricane directories: ",hurr_dirs)
                        print()
                        print("FLOAT directories: ",float_dirs_out)
    float_dirs_out.sort()
    return float_dirs_out

##
## Create a list of *_results.txt files in each directory
##

def results_files_list(float_dirs_in):
    print("Finding *_results.txt files...")
    results_file_path=[]
    for item01 in float_dirs_in: #look at each FLOAT dir
        content_list=os.listdir(item01) #read contents of dir
        for item02 in content_list: #look at each item in dir
            if fnmatch.fnmatch(item02,"*_results.txt"): #look for specific files
                results_file_path.append(item01+item02) #add specific files to list
    return(results_file_path) #return list of files

##
## Open the *_results.txt files from list and pull relevant data
##

def gather_data(results_path_in,start_yr_in,end_yr_in):
    data_file=DATA_DIR+str(start_yr_in)+"-"+str(end_yr_in)+"_comp_data.txt" #data file to be written
    print("Gathering relevant data from *_results.txt files...")
    with open(data_file,'w') as g: #write header of data file
        g.write("#File\tRadius\tBar\tMode(P)\tMean(P)\tStdDev (P)\tMean(O)\tStdDev (O)\tMean(1)\tStdDev (1)\tMean(2)\tStdDev (2)\tMean(3)\tStdDev (3)\tMean(4)\tStdDev (4)\tMean(5)\tStdDev (5)\tMean(6)\tStdDev (6)\n")
    for item01 in results_path_in: #look at each *_results.txt file
        with open(item01,'r') as f: #open *_results.txt file for reading
            for i, line in enumerate(f): #count number of lines in file
                if i == 1: #use second line
                    with open(data_file,'a') as h: #append data file
                        h.write(line)
    print("\nWrote "+data_file+"\n")
    return(data_file)

##
## Main
##

start_yr_choice=input("\nSelect beginning year from "+str(VALID_MIN_YR)+" - "+str(VALID_MAX_YR)+": ") #ask user beginning year to process

end_yr_choice=input("\nSelect ending year from "+str(VALID_MIN_YR)+" - "+str(VALID_MAX_YR)+": ") #ask user end year to process

analyze_yr(start_yr_choice,end_yr_choice) #check if year selections are valid

year_list=generate_yr_list(start_yr_choice,end_yr_choice) #generate a text list of years

dir_list=make_dir_list(year_list) #create list of dirs to dive into

results_path=results_files_list(dir_list) #create a list of *_results.txt files for each dir

data_file=gather_data(results_path,start_yr_choice,end_yr_choice) #gather relevant data from *_results.txt files 

