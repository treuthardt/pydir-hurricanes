#!/usr/bin/env python
##
##
## GENERATE_P2DFFT_INPUT.PY - Creates scripts to run p2dfft on hurricane images
##
## Version 1.0  16-Mar-2018
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

##
## Global Variables
##
##   NOW: gets current date and time
##   VERSION: latest version number of this program
##   BASE_PATH: base path of data
##   BEGIN_YEAR: default beginning year
##   END_YEAR: default ending year
##   RUNME_DIR: directory holding *.runme text files to run in bash
##   RUNME_FILE: default filename of runmefile

NOW=datetime.datetime.now() ## gets current date and time
VERSION='1.0/20180309'
BASE_PATH='/data1/patrick/PROJECTS/Hurricanes/Pictures/' # base path of data
BEGIN_YEAR=1995 #default beginning year
END_YEAR=2005 #default ending year
RUNME_DIR="/data1/patrick/PROJECTS/Hurricanes/runme/"
RUNME_FILE="launch_01.runme"

##
## Let's go!
##

print("\nRunning GENERATE_P2DFFT_INPUT.PY version:", version,"\n")

##
## Create list of years
##

def create_year_list(choice_input):
    year_output=[] #initialize list
    if choice_input == "A" or choice_input == "a":
        for i in range(BEGIN_YEAR,END_YEAR+1): 
            year_output.append(i) #append each year to list
    elif int(choice_input) < 2006 and int(choice_input) > 1994:
        year_output.append(choice_input) #append single choice to list
    else:
        sys.exit("ERROR: "+choice_input+" is not a valid option. ")
    return year_output

##
## Locate and link directories with SQ*.fits files
##

def locate_directories(yr_input):
    path_02=[]
    path_03=[]
    for i in yr_input: #looks in listed years
        path_01=BASE_PATH+str(i) #create path to year
        hurr_dirs1=os.listdir(path_01) #makes list of hurricane dirs in year
        for j in hurr_dirs1:
            path_02.append(path_01+"/"+j) #creates list of folder paths
    for k in path_02: #looks in listed hurricane dirs
        files_in_hurr_dir=os.listdir(k)
        for l in files_in_hurr_dir:
            if fnmatch.fnmatch(l,"FLOAT"): #finds directories with FLOAT sub dirs
                path_03.append(k+"/FLOAT/") #saves list of FLOAT paths
    sq_list={} #sets as empty dictionary
    for m in path_03: #look at each FLOAT dir
        files_in_FLOAT=os.listdir(m) #list everything in FLOAT dir
        for n in files_in_FLOAT: #look at each file in FLOAT dir
            if fnmatch.fnmatch(n,"SQ*.fits"): #if it's the correct file...
                sq_list[n]=m #create dictionary element with SQ*fits file and FLOAT dir
    return sq_list #return dictionary

##
## Write *.runme file
##

def create_runme_file(sq_list_input,filename_input): #input sq files and directory, .runme file name
    runme_path=RUNME_DIR
    with open(runme_path+filename_input,'w') as f: #open for writing
        f.write("#"+str(NOW)+"\n") #time stamp
        f.write('start_time="$(date -u +%s)"\n') #keeps track of start of run in bash
        for i in sq_list_input: #each key in dictionary
            f.write("cd "+sq_list_input[i]+" && 2dfft "+i+"\n") #write command line with element followed by key
        f.write('end_time="$(date -u +%s)"\n') #keeps track of end of run in bash
        f.write('elapsed="$(($end_time - $start_time))"\n') #math in bash
        f.write('echo "Total of $elapsed seconds elapsed during run."') #prints elapsed time to terminal
    os.chmod(runme_path+filename_input,stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH) #chmod's status to allow rwx by user & group, rx by others
    return runme_path+filename_input

##
## Main 
##

year_choice=input("Select year from 1995 - 2005 or (A)ll: ") #Ask user to select year for run
year=create_year_list(year_choice) #saves year choice

dir_sqfile_list=(locate_directories(year)) #Run routine to find SQ files

print("\nCreated "+create_runme_file(dir_sqfile_list,RUNME_FILE)) #Tell user that process is complete

