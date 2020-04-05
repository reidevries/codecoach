# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------
Filename   : osu_oregon.py
Date       : 2013-01-06
Author     : Joe Lotz
Purpose    : Trying to recreate a graphic found but using oregon data.
Data       : UO_vs_OSU.csv
Sources    : [1] http://thedailyviz.com/2012/11/24/charting-the-fsu-florida-rivalry/
             [2] http://www.sports-reference.com/cfb/play-index/rivals.cgi?request=1&school_id=oregon&opp_id=oregon-state
-------------------------------------------------------------------------------
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close()

PHI = 1.618  # golden ratio

# define plot colors, allows me to adjust afterwards
#l_color = (myColor.blue(),myColor.red())
l_color = ('#7570B3','#D95F02')

data = pd.read_table('OSU_vs_UO.csv', sep=',')

'''
data.G is the game number
data.Date is the date of the game
data.Pts is the UO score
data.Opposition is the OSU score
'''

years = data.Date.apply(lambda x: '\''+(str(x[-2:])))

osu_score = np.array(data.Pts)
uo_score = np.array(data.Opp)

# Initiate
Y_OSU = [0]*len(osu_score)
Y_UO  = [0]*len(osu_score)

# Process
for cnt in range(0, len(osu_score)):
    if osu_score[cnt] > uo_score[cnt]:    
        Y_OSU[cnt] = osu_score[cnt]
    else:
        Y_UO[cnt] = -uo_score[cnt]

    
# Create a new figure w/ 6 point height, using 80 dots per inch
plt.figure(figsize=(10,15*PHI), dpi=80)

# Create a new subplot from a grid of 1x1
plt.subplot(1,1,1)

ylocations = np.arange(len(Y_OSU))+.5
plt.barh(ylocations,Y_OSU,color=l_color[0])
plt.barh(ylocations,Y_UO,color=l_color[1])

a = np.array(years)
b = a[::-1]

# Add Y-axis Year labels
plt.yticks(ylocations+ 0.5/2, b)

ax = plt.gca()
ax.xaxis.grid(True, which='major') 
ax.xaxis.set_major_locator(MaxNLocator(14))
ax.set_xticklabels(('','60','50','40','30','20','10','0','10','20','30','40','50','60',''))

# Add a title
plt.figtext(0.15,.925,'Oregon State vs. Oregon', fontsize=22, ha='left', weight='bold')
plt.figtext(0.15,.91,'Margin of Victory: 1916-2012',fontsize=16,ha='left')

#plt.suptitle('Oregon State vs. Oregon', fontsize=16)
#plt.title('Margin of Victory: 1916-2012')

# Add a xlabel
plt.xlabel('Points', fontsize=16)

# X Limit
plt.xlim(-70, 70)

plt.show()

#plt.savefig("osu_uo.png",dpi=80)