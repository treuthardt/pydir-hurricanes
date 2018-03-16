#!/usr/bin/env python

##
##
## EDIT_SCRIPTER.PY - Edits *_scripter files for hurricane data
##
## Version 1.0  01-Dec-2017
##
## Author: 
##   Patrick Treuthardt
##
## Description: 
##   Looks for original *.scripter files, changes *.fits.txt 
##   to *.fits in the file, and saves the new version as *.scripter2. Also 
##   creates a job list file for running changed *.scripter2 files. 
##
## Revision History:
##   1.0 - first attempt
##
## Requirements: None
##
##

##
## Import System Libraries
##

import os ## operating system interfaces
import fnmatch ## unix filename pattern matching
import datetime ## Basic date and time types
import os.path ## Common pathname manipulations

##
## Main
##

now=datetime.datetime.now() ## gets current date and time
version='1.0/20171201'

print ""
print "edit_scripter.py version:", version
print ""


##
## Locate *.scripter files
##

path_01='/data1/patrick/PROJECTS/Hurricanes/Pictures/' ## base path

scripter_list=list() ## initialize array to add *.scripter files to
scripter2_list=list() ## initialize array to add *.scripter files to

for x in range(1995,2006): ## (start,end+1); enter year folders
    path_02=path_01+str(x)+'/'
    
    for folder in os.listdir(path_02+'.'): ## list folders in year
        path_03=path_02+str(folder)+'/' ## path to each folder containing *.scripter files
        
        for folder2 in os.listdir(path_03+'.'): ## look for FLOAT folder
            if fnmatch.fnmatch(folder2,'FLOAT'): ## for those with FLOAT folders
                path_04=path_03+'FLOAT/' ## path to those with FLOAT folders
                
                for file in os.listdir(path_04+'.'): ## list files in FLOAT folder
                    if fnmatch.fnmatch(file,'*.scripter'): ## find *.scripter files
                        scripter_list.append(path_04+file) ## create array list of *.scripter files
                    if fnmatch.fnmatch(file,'*.scripter2'): ## find *.scripter2 files
                        scripter2_list.append(path_04+file) ## create array list of *.scripter2 files

##
## Make list of *.scripter2 files
##

mod_scripter_list=list() ## initialize *.scripter -> *.scripter2 list

for i, file_list in enumerate(scripter_list): ## run from beginning to end of scripter_list
    mod_scripter_list.append(file_list+'2') ## add '2' to *.scripter file

##
## Compare mod_scripter_list elements to scripter2_list elements
##    and remove duplicates from mod_scripter_list
##

for x in range(0,len(scripter2_list)): ## run for length of number of *.scripter2 files
    contained=[y for y in mod_scripter_list if y in scripter2_list[x]] ## find files that already have *.scripter2
    mod_scripter_list.remove(contained[0]) ## remove already run *.scripter2 files from list
    
##
## Create new *.scripter2 files where needed
##

mod_scripter_list2= [list2.replace('.scripter2','.scripter') for list2 in mod_scripter_list] ## create list of original files that need to be modified from *.scripter to *.scripter2

##print mod_scripter_list2
##print mod_scripter_list

if os.path.exists('/data1/patrick/PROJECTS/Hurricanes/job_list_'+str(now.year)+str(now.month)+str(now.day)+'.txt'): ## look if file exists, if so delete it before appending
    os.remove('/data1/patrick/PROJECTS/Hurricanes/job_list_'+str(now.year)+str(now.month)+str(now.day)+'.txt') ## delete existing file

for index,element in enumerate(mod_scripter_list2): ## run for each element in mod_scripter_list2
    head, sep, tail=mod_scripter_list[index].partition('/FLOAT/') ## chop up path string

    f=open(mod_scripter_list2[index],'r') ## open *.scripter files for reading
    filedata=f.read() ## read *.scripter file
    f.close() ## close file for use

    newdata=filedata.replace(".txt,",",") ## find and replace this text

    f=open(mod_scripter_list[index],'w') ## open *.scripter2 file for writing
    f.write(newdata) ## write *.scripter2 file data
    f.close() ## close file for use

    f=open('/data1/patrick/PROJECTS/Hurricanes/job_list_'+str(now.year)+str(now.month)+str(now.day)+'.txt','a') ## open a file to write to named with date; a = append to file
    f.write('cd '+head+sep+' && 2dfft -i '+tail+' &\n') ## write single lines to file that will be used later
    f.close()  ## close file for writing.
    

