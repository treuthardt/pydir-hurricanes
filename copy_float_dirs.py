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
import stat ## Allow chmod status changes

##
## Global Variables
##
now=datetime.datetime.now() ## gets current date and time
version='1.0/20180319'
job_path='/data1/patrick/PROJECTS/Hurricanes/' #path to copy job file
job_name='copy01.runme'
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
## Find FLOAT dirs on remote drive
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
    return(path_03) #returns list of FLOAT dirs on remote drive

##
## Copy contents of remote FLOAT dirs to local drive
##
def copy_procedure(float_dirs_input):
    float_dirs_out=intern_path+str(year_choice)+"/"
    year_dirs=os.listdir(intern_path)
    exists_01=0
    exter_hurr_dirs01=[]

    ##
    ## Check if year directory exists in local path
    ##
    for l in year_dirs: #check contents of dir
        if fnmatch.fnmatch(l,str(year_choice)): #look for matching year dir
            print("Found "+float_dirs_out)
            exists_01+=1 #indicate year dir exists
    if exists_01 == 0: #if year dir doesn't exist
        sys.exit("ERROR: mkdir "+float_dirs_out+"\n") #prompt to create year dir
    print()

    ##
    ## Store each hurricane directory from remote drive
    ##
    for item01 in float_dirs_input: #for each FLOAT dir on remote drive
        exter_hurr_dirs01.append(item01.split("/")[7]) #store each hurr dir in list

    ##    
    ## Check if hurricane directory exists in local path
    ##
    intern_hurr_dirs01=os.listdir(float_dirs_out) #list contents of internal year path
    intern_hurr_dirs02=[] #initializes list
    for item02 in exter_hurr_dirs01: #for each hurr dir in external drive path
        exists_02=0 #set mark as not found
        for item03 in intern_hurr_dirs01: #for each item in internal year path
            if item02 == item03: #if dirs exist in both paths
                print("Found "+float_dirs_out+item03+"/")
                intern_hurr_dirs02.append(float_dirs_out+item03+"/") #create list of paths
                exists_02+=1 #mark as found
        if exists_02 == 0: #if dir not found in internal drive path
            sys.exit("ERROR: mkdir "+float_dirs_out+item02+"/\n") #quit and prompt to create hurr dir
    print()
    
    ##
    ## Check if FLOAT dir exists in local hurricane directories
    ##
    intern_float_dir02=[]
    for item04 in intern_hurr_dirs02:
        intern_float_dir01=os.listdir(item04) #list items in hurr dir to look for FLOAT dir
        exists_03=0 #set mark as not found
        for item05 in intern_float_dir01:
            if fnmatch.fnmatch(item05,"FLOAT"): #look for existing FLOAT dir
                print("Found "+item04+"FLOAT/")
                intern_float_dir02.append(item04+"FLOAT/") #add existing FLOAT dir to list
                exists_03+=1 #set mark as found
        if exists_03 == 0: #if FLOAT dir not found in internal drive path
            sys.exit("ERROR: mkdir "+item04+"FLOAT/\n") #quit and prompt to create FLOAT dir
    print()

    ##
    ## When all okay, write shell script for copying!
    ##
    float_dirs_input.sort() #sort list of remote FLOAT dirs
    intern_float_dir02.sort() #sort list of internal FLOAT dirs
    with open(job_path+job_name,'w') as f:
        f.write("#"+str(now)+"\n")
        f.write('start_time="$(date -u +%s)"\n') #keeps track of start of run in bash
        for x in range(0,len(float_dirs_input)-1):
            f.write("cp "+float_dirs_input[x]+"* "+intern_float_dir02[x]+"*\n")
        f.write('end_time="$(date -u +%s)"\n') #keeps track of end of run in bash
        f.write('elapsed="$(($end_time - $start_time))"\n') #math in bash
        f.write('echo "Total of $elapsed seconds elapsed during run."') #prints elapsed time to terminal
    os.chmod(job_path+job_name,stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH) #chmod's status to allow rwx by user & group, rx by others
    

##
## Main
##
year_choice=input("\nSelect year from "+str(valid_min_year)+" - "+str(valid_max_year)+": ") #ask user which year to process
print()
analyze_year(year_choice) #test year choice
remote_float_dirs=look_for_float_dirs(year_choice) #save list of FLOAT dirs for a given year on remote drive
copy_procedure(remote_float_dirs)

print("\nCreated "+job_path+job_name) #Tell user that process is complete
