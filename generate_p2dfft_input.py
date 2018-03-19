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
## Main
##
now=datetime.datetime.now() ## gets current date and time
version='1.0/20180309'
base_path='/data1/patrick/PROJECTS/Hurricanes/Pictures/' # base path of data
begin_year=1995 #default beginning year
end_year=2005 #default ending year
runme_file="launch_01.runme"
num_simul_runs=8 #number of p2dfft's to run at same time

print("\nRunning GENERATE_P2DFFT_INPUT.PY version:", version,"\n")

##
## Create list of years
##
def create_year_list(choice_input):
    year_output=[] #initialize list
    if choice_input == "A" or choice_input == "a":
        for i in range(begin_year,end_year+1): 
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
        path_01=base_path+str(i) #create path to year
        hurr_dirs1=os.listdir(path_01) #makes list of hurricane dirs in year
 #       print(hurr_dirs1)
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
def create_runme_file(sq_list_input,filename_input,run_num_input): #input sq files and directory, .runme file name
    runme_path=base_path.replace("Pictures/","")
    if run_num_input > 24: #defaults max number to 24 cores
        print("\nWARNING: "+str(run_num_input)+" runs set to default maximum of 24.")
        run_num_input=24
    with open(runme_path+filename_input,'w') as f: #open for writing
        f.write('start_time="$(date -u +%s)"\n') #keeps track of start of run in bash
        for i in sq_list_input: #each key in dictionary
            f.write("cd "+sq_list_input[i]+" && 2dfft "+i+"\n") #write command line with element followed by key
        f.write('end_time="$(date -u +%s)"\n') #keeps track of end of run in bash
        f.write('elapsed="$(($end_time - $start_time))"\n') #math in bash
        f.write('echo "Total of $elapsed seconds elapsed during run."') #prints elapsed time to terminal
    os.chmod(runme_path+filename_input,stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH) #chmod's status to allow rwx by user & group, rx by others
    return runme_path+filename_input

##
## Ask user to select year for run
##
year_choice=input("Select year from 1995 - 2005 or (A)ll: ")
year=create_year_list(year_choice) #saves year choice

##
## Run routine to find SQ files
##
dir_sqfile_list=(locate_directories(year))

##
## Tell user that process is complete
##
print("\nCreated "+create_runme_file(dir_sqfile_list,runme_file,num_simul_runs))
