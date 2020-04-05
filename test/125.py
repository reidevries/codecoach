# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------
Filename   : multiple_scatter.py
Date       : 2013-01-11
Author     : Joe Lotz
Purpose    : Trying to recreate a graphic using matplotlib.
Sources    : [1] http://visual.ly/daylight-saving-time-explained
             [2] http://aa.usno.navy.mil/data/docs/RS_OneYear.php
-------------------------------------------------------------------------------
'''
import matplotlib.pyplot as plt

plt.close()

# define data
movies = [0.94,0.94,0.85]
nonsequels = [0.8,0.44,0.765]
sequels = [0.84,0.8,0.7]
music = [0.86,0.7,0.56]
flu = [0.94,0.86,0.94]

# build axes
xAxis = [0.4,0.5,0.6,0.7,0.8,0.9,1.0]
xAxis_blanklabels = ['','','','','','','']
xAxis_labels = ['0.4','0.5','0.6','0.7','0.8','0.9','1.0']

yAxis = [0.5,1.5,2.5]
yAxis_labels = ['Combined','Baseline','Search']

plt.figure(dpi=80)
#plt.rcParams['xtick.direction'] = 'out'
#plt.rcParams['ytick.direction'] = 'out'
plt.tick_params(axis='both', direction='out')

plt.subplot(5,1,1)
plt.scatter(movies,yAxis)
plt.grid()
plt.yticks(yAxis,yAxis_labels)
plt.xticks(xAxis,xAxis_blanklabels)
plt.xlim(min(xAxis)-0.02,max(xAxis)+0.02)
#plt.annotate(r' Movies  ',xytext=(.1,.10),xy=(1.02, 1.8), xycoords='data',
#            textcoords='offset points',rotation=-90,bbox=dict(boxstyle="square", fc="0.8"))
#newax = fig.add_axes()
#newax.patch.set_visible(False)
#newax.set_ylabel('Movies')

plt.subplot(5,1,2)
plt.scatter(nonsequels,yAxis)
plt.grid()
plt.yticks(yAxis,yAxis_labels)
plt.xticks(xAxis,xAxis_blanklabels)
plt.xlim(min(xAxis)-0.02,max(xAxis)+0.02)

plt.subplot(5,1,3)
plt.scatter(sequels,yAxis)
plt.grid()
plt.yticks(yAxis,yAxis_labels)
plt.xticks(xAxis,xAxis_blanklabels)
plt.xlim(min(xAxis)-0.02,max(xAxis)+0.02)

plt.subplot(5,1,4)
plt.scatter(music,yAxis)
plt.grid()
plt.yticks(yAxis,yAxis_labels)
plt.xticks(xAxis,xAxis_blanklabels)
plt.xlim(min(xAxis)-0.02,max(xAxis)+0.02)

plt.subplot(5,1,5)
plt.scatter(flu,yAxis)
plt.grid()
plt.yticks(yAxis,yAxis_labels)
plt.xticks(xAxis,xAxis_labels)
plt.xlim(min(xAxis)-0.02,max(xAxis)+0.02)

ax = plt.gca()
#ax.set_xlabel('Month', fontsize=20)
ax.set_xlabel('Fit', fontsize=18)

plt.show()
#plt.savefig("multiple_scatter.png",dpi=80)