# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------
Filename   : census.py
Date       : 2013-01-13
Author     : Joe Lotz
Purpose    : Trying to recreate a graphic using matplotlib.
Sources    : [data] http://www.census.gov/dataviz/visualizations/025/508.php
             [image] http://www.census.gov/dataviz/visualizations/025/
-------------------------------------------------------------------------------
'''

import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import csv
import numpy as np

plt.close()

PHI = 1.618  # golden ratio

def build_csv(html_doc='I5_data.html',csv_file='I5_data.csv'):
    soup = BeautifulSoup(open(html_doc))
    table = soup.find("table")
    
    data = []
    for row in table.find_all('tr')[1:]:
        col = row.find_all('td')
        # parse each col in the row
        sign = col[0].string
        mile = col[1].string
        population = col[2].string
        area = col[3].string
        pop_density = col[4].string
        # build the record
        record = (sign, mile, population, area, pop_density)
        data.append(record)
        
    result = open(csv_file,'wb')
    writer = csv.writer(result, dialect = 'excel')
    writer.writerows(data)
    result.close()

def read_csv(csv_file='I5_data.csv'):
    record = ('sign','mile','population','area','pop_density')
    data = pd.read_csv(csv_file,names=record)
    return data

def findMax(level):
    peaks = [0]*len(level)
    numPeaks = 0
    for i in range(1, len(level)-1):
        if level[i-1] < level[i] and level[i+1] < level[i] and level[i]>9000 and level[i]<12000:
            peaks[i] = 1
            numPeaks += 1    
    return peaks
#################################

data = read_csv()
#
yAxis = data.mile
xAxis = data.pop_density


maximas_ndx = findMax(xAxis)
maximas = []
cnt = 0
index=[]
for x in xAxis:
    if maximas_ndx[cnt]==1: 
        maximas.append(xAxis[cnt])
        index.append(cnt)
    cnt = cnt+1

mycircle = [24,39,84,340,414,496,527,608,620,680]
myfilled = [5,53,66,237,258,550,639]

plt.close()
plt.figure(figsize=(5,5*PHI),dpi=80)

plt.plot(xAxis,yAxis,color='#3069b2')
testing=True
if testing==True:
    plt.plot(np.ones(len(mycircle))*15250, yAxis[mycircle],linestyle='None',
             marker='o',markersize=7,markeredgecolor='k',markerfacecolor='w')
    plt.plot(np.ones(len(myfilled))*15250, yAxis[myfilled],linestyle='None',
             marker='o',markersize=7,markeredgecolor='k',markerfacecolor='k')
else:
    plt.plot(np.ones(len(index))*15250, yAxis[index], marker='o',
                edgecolor='k',facecolor='k')


plt.barh(yAxis,xAxis, edgecolor='#3069b2')



#plt.fill(xAxis,yAxis,'b')
plt.xticks([0,2500,5000,7500,10000,12500,15000],
           ['0','2,500','5,000','7,500','10,000','12,500','15,000'],
            rotation=90)
plt.xlim(0,15500)
plt.ylim(0,max(yAxis)+5)

plt.xlabel('population density / m$^2$',size=14)
plt.ylabel('miles',size=14)

plt.show()

#plt.savefig("census.png",dpi=80)