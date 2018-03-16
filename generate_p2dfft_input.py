#!/usr/bin/env python
##
##
## GENERATE_P2DFFT_INPUT.PY - Creates scripts to run p2dfft on hurricane images
##
## Version 1.0  09-Mar-2018
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
version='1.0/20180309'
base_path='/data1/patrick/PROJECTS/Hurricanes/Pictures/' # base path of data
begin_year=1995 #default beginning year
end_year=2005 #default ending year
runme_file="junk_test.runme"
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
## Locate directories with SQ*.fits files
##
######## NEED THIS TO WORK OVER MULITPLE YEARS AND HURRICANES ###########
def locate_directories(yr_input):
    path_02=[]
    for i in yr_input:
        path_01=base_path+str(i) #create path to year
        hurr_dirs1=os.listdir(path_01) #makes list of hurricane dirs in year
 #       print(hurr_dirs1)
        for j in hurr_dirs1:
            path_02.append(path_01+"/"+j) #creates list of folder paths
            ###NOT ALL HAVE FLOAT DIRECTORIES###
    print(path_02)
    for k in path_02:
        files_in_FLOAT=os.listdir(k)
        sq_list=[]
        for l in files_in_FLOAT:
            if fnmatch.fnmatch(l,"SQ*.fits"):
                sq_list.append(l)
        #print(sq_list)
        
#    print(hurr_dirs_master) 
        
    path_01=base_path+str(year[0]) #set to 1995 = year[0]
    hurr_dirs=os.listdir(path_01) #makes list of hurricane dirs in year
    path_02=path_01+"/"+hurr_dirs[0]+"/FLOAT/" #makes path to first hurricane dir for 1995 = year[0]
    files_in_FLOAT=os.listdir(path_02) #lists all files in FLOAT dir
    sq_list=[]
    for i in files_in_FLOAT: #look at each file in FLOAT dir
        if fnmatch.fnmatch(i,"SQ*.fits"): #look for matching files in dir
            sq_list.append(i) #store matching files in sq_list
       
    return path_02,sq_list 

##
## Write *.runme file
##
def create_runme_file(dir_sqfile_input,filename_input,run_num_input): #input sq files and directory, .runme file name
    runme_path=base_path.replace("Pictures/","")
    j=0
    if run_num_input > 24: #defaults max number to 24 cores
        print("\nWARNING: "+str(run_num_input)+" runs set to default maximum of 24.")
        run_num_input=24
    with open(runme_path+filename_input,'w') as f: #open for writing
        dir_txt=dir_sqfile_input[0] #directory with sq files
        for i in dir_sqfile_input[1]:
            j+=1
            if j%run_num_input == 0:
                f.write("cd "+dir_txt+" && 2dfft "+i+" ;\n") #write command line
            else:
                f.write("cd "+dir_txt+" && 2dfft "+i+" &\n") #write command line
    return runme_path+filename_input


year_choice=input("Select year from 1995 - 2005 or (A)ll: ")
year=create_year_list(year_choice) #saves year choice

dir_sqfile_list=(locate_directories(year)) 
#print(dir_sqfile_list[1][0])

print("\nCreated "+create_runme_file(dir_sqfile_list,runme_file,num_simul_runs))
