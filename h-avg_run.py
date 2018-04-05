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
from shutil import copyfile ## High level file operations
#import matplotlib.pyplot as plt ## Allows plotting

##
## Global Variables
##
##   NOW: current date and time
##   VERSION: latest version number of this program
##   ROOT_DIR: root directory for processing the data
##   RUNME_DIR: directory holding *.runme text files to run in bash
##   VALID_MIN_YR: min year directory
##   VALID_MAX_YR: max year directory
##   VERBOSE: print out what is happening as program runs
##

NOW=datetime.datetime.now() 
VERSION="1.0/20180323"
ROOT_DIR="/data1/patrick/PROJECTS/Hurricanes/Pictures/"
RUNME_DIR="/data1/patrick/PROJECTS/Hurricanes/runme/"
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
    print("Copying *.scaler files to *.scaler_old...")
    scaler_path_out=[]

    for item01 in dir_list_in: #run for each hurricane directory
        contents_list=os.listdir(item01)
        skip=0

        for item02 in contents_list: #begin looking for *.scaler_old in dir
            if fnmatch.fnmatch(item02,"*.scaler_old"): #will skip if *old exists
                skip=1 #tag *.scaler_old already exits
                print("SKIPPING: "+item02+" already exists")

        if skip == 0: #begin coping if *.scaler_old doesn't already exist
            for item03 in contents_list: #run for each file in directory

                if fnmatch.fnmatch(item03,"*.scaler"): #find *.scaler file
                    copyfile(item01+item03,item01+item03+"_old") #copy to diff file
                    print("Copied "+item03+" --> "+item03+"_old")

        for item04 in contents_list: #begin making path list of *.scaler files
            if fnmatch.fnmatch(item04,"*.scaler"): #find scaler file again
                scaler_path_out.append(item01+item04) #add path to list

    scaler_path_out.sort()
    print()
    return scaler_path_out

##
## Append *.scaler files so that each entry that doesn't begin with SQ_*, does.
##

def scaler_change(scaler_path_in):
    print("Appending *.scaler files...")
    substring="SQ_"
    junk_counter=0 #useless activity in if statement
    message_tracker=[] #used to keep track of messages

    for item01 in scaler_path_in: #in each scaler file to be modified
        temp_list=[] #temp storage list

        with open(item01,"r") as f: #open file for appending and reading
            for item02 in f: #look at each item in file
                temp_list.append(item02) #create list of file contents
        temp_list.sort() #sort that list for clarity

        for item04 in temp_list: #each line in file contents
            if substring+item04 in temp_list: #look for SQ_* versions of line
                junk_counter+=1
            else: #if SQ_* version of line doesn't exist

                if substring in item04: #Check if SQ_* already in line
                    junk_counter+=1
                else: #finds lines without SQ_ in them

                    if item01 not in message_tracker: #notify if appending
                        print("APPENDING: "+item01)
                        message_tracker.append(item01)
                    with open(item01,"a+") as h: #append to *.scaler file
                            h.write("SQ_"+item04)

        if item01 not in message_tracker: #notify if nothing changed
            print("SKIPPING: "+item01)

    print()
    return

##
## Next, go through each directory and extract the root string of the
##   SQ*_m[0-6] files and use that for basis of running h-avg.py.
##   The run string should be something like:
##   h-avg.py -c 1 -n Tanya.scaler -o SQ_19951101_174513_fix_results.txt SQ_19951101_174513_fix
##
##   Finally, create a *.runme file to launch in bash to get out results and plots
##

def extract_root_string(scaler_path_in,yr_choice_in):
    run_number=0 #first iteration set to 0
    for item01 in scaler_path_in:
        temp_list=[] #empty list

        with open(item01,"r") as f: #open *.scaler file for reading
            for item02 in f: #look at each element in *.scaler file
                if "SQ_" in item02: #look for SQ_ prefix in element
                    root,scale=item02.split("\t") #split string around tab
                    temp_list.append(root) #append root string to list

        dir,scaler_file=item01.split("/FLOAT/") #split text around /FLOAT/

        if run_number == 0: #if it's the first run, delete and write file
            with open(RUNME_DIR+str(yr_choice_in)+"_results.runme","w") as g: #deletes and writes to file
                g.write("#"+str(NOW)+"\n") #time stamp
                for item03 in temp_list: #write correct lines
                    g.write("cd "+dir+"/FLOAT/ && h-avg.py -c 1 -n "+scaler_file+" -o "+item03+"_results.txt "+item03+"\n") #write line for getting results

        else: #subsequent runs, append to file
            with open(RUNME_DIR+str(yr_choice_in)+"_results.runme","a") as h:
                for item03 in temp_list: #write correct lines
                    h.write("cd "+dir+"/FLOAT/ && h-avg.py -c 1 -n "+scaler_file+" -o "+item03+"_results.txt "+item03+"\n")

        run_number+=1 #increment run number

    os.chmod(RUNME_DIR+str(yr_choice_in)+"_results.runme",stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH) #chmod's status to allow rwx by user & group, rx by others
    return

##
## Main
##

yr_choice=input("\nSelect year from "+str(VALID_MIN_YR)+" - "+str(VALID_MAX_YR)+": ") #ask user which year to process

analyze_yr(yr_choice) #check if year is valid

dir_list=make_dir_list(yr_choice) #create list of dirs to dive into

scaler_path=scaler_copy(dir_list) #copy *.scaler files

scaler_change(scaler_path) #append corrected root names to *.scaler files

extract_root_string(scaler_path,yr_choice) #extract root strings and create *.runme file
