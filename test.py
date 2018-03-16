#!/usr/bin/env python

import os

year=[]
for i in range(1995,2005+1):
    year.append(i)

print(year)
print(os.listdir("/data1/patrick/PROJECTS/Hurricanes/Pictures/"+str(year[0])))

