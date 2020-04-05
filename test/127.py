# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------
Filename   : parallel.py
Date       : 2013-01-11
Author     : Joe Lotz
Purpose    : Trying to recreate a graphic using matplotlib.
Sources    : [1] http://visual.ly/daylight-saving-time-explained
             [2] http://aa.usno.navy.mil/data/docs/RS_OneYear.php
-------------------------------------------------------------------------------
'''
import matplotlib.pyplot as plt

PHI = 1.618  # golden ratio

plt.close()

# build data
combined = [0.8,0.84,0.94,0.87,0.94]
search = [0.44,0.8,0.7,0.94,0.86]
baseline = [0.765,0.7,0.56,0.85,0.94]

# build axes
yAxis = [0.4,0.5,0.6,0.7,0.8,0.9,1.0]
xAxis = [0.5,1.5,2.5,3.5,4.5]
xAxis_labels = ['Nonsequel Games','Sequel Games','Music','Movies','Flu']

plt.figure(figsize=(6*PHI,6),dpi=80)

plt.plot(xAxis,combined, color='green',marker='x', markeredgewidth=3,markersize=10,
         label='Combined',linewidth=2.5)
plt.plot(xAxis,baseline, color='blue',marker='o', markeredgewidth=1,markersize=10,
         label='Search',linewidth=2.5)
plt.plot(xAxis,baseline, color='blue',
         linestyle='solid',label='Search',linewidth=2.5)


        
plt.xlim(min(xAxis)-0.5, max(xAxis)+0.5)
plt.ylim(min(yAxis)-0.02, max(yAxis)+0.02)
plt.xticks(xAxis,xAxis_labels,rotation=20)

ax = plt.gca()
ax.set_ylabel('Correlation Between Predicted and Actual Outcome', fontsize=14)

#xkcd.XKCDify(ax, xaxis_loc=0.0, yaxis_loc=1.0,
#        xaxis_arrow='+-', yaxis_arrow='+-',
#        expand_axes=True)

plt.show()
#plt.savefig("multiple_scatter.png",dpi=80)
