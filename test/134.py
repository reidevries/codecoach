# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------
Filename   : SUNRISE_SUNSET.py
Date       : 2012-11-27
Author     : Joe Lotz
Purpose    : My attempt at recreating the results from one of my favorite blogs
                using Python.
Sources    : http://datagenetics.com/blog/august12012/index.html

-------------------------------------------------------------------------------
'''
import math
import matplotlib.pyplot as plt

global LENGTH
global DIAMETER
global PI


'''
FROSTUM
            b
   -------------------   -
    \               /    |
   l \             /     | h
      \___________/      |
            d            -

Volume_frostum = (pi h)/12 (d^2+db+b^2)
'''

def height(angle): return mycos(angle) * LENGTH
def base(angle): return 2 * opp(angle) + DIAMETER
def opp(angle): return mysin(angle) * LENGTH
def mycos(angle_degrees): return math.cos(math.radians(angle_degrees))
def mysin(angle_degrees): return math.sin(math.radians(angle_degrees))
def volume(angle):
    volume = ((PI*height(angle))/12) * ( math.pow(DIAMETER,2) + \
                (DIAMETER * base(angle)) + math.pow(base(angle),2))
    return volume

####### CONSTANTS #######
PI = math.pi
PHI = 1.618    # golden ratio
DIAMETER = 53  # empirically measured by Nick, see blog
LENGTH = 43.5  # empirically measured by Nick, see blog

####### CALC f(x) #######
# x and y axis values
deg_list = range(0,90,1) # list of angles 0 - 90deg
vol_list = map(volume,deg_list) # perform vol calcs on each angle

####### PLOT VOLUME AS A FUNCTION OF ANGLE #######
# Create a new figure w/ 6 point height, using 80 dots per inch
plt.figure(num=1,figsize=(6*PHI,6), dpi=80)
# Create a new subplot from a grid of 1x1
#plt.subplot(1,1,1)
plt.plot(deg_list,vol_list,color='#bf4b48',linewidth=2.5,linestyle="-")

plt.title('Volume of my pleated cup', fontsize=18)
plt.ylim(0, 200000)
plt.yticks([0,20000,40000,60000,80000,100000,120000,140000,160000,180000,200000],
           ['0','20,000','40,000','60,000','80,000','10,000','120,000','140,000',
           '160,000','180,000','200,000'])
plt.xlim(0, 90)
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90],
           ['0$^\circ$','5$^\circ$','10$^\circ$','15$^\circ$','20$^\circ$',
           '25$^\circ$','30$^\circ$','35$^\circ$','40$^\circ$','45$^\circ$',
           '50$^\circ$','55$^\circ$','60$^\circ$','65$^\circ$','70$^\circ$',
           '75$^\circ$','80$^\circ$','85$^\circ$','90$^\circ$' ])

ax = plt.gca()
ax.set_xlabel('Angle of side (deg)', fontsize=16)
ax.set_ylabel('Volume (mm$^3$)', fontsize=16)
#ax.xaxis.set_major_locator(plt.MaxNLocator(19))
ax.yaxis.grid(True)
ax.xaxis.grid(False)

plt.show()
plt.savefig("ketchu_function.png",dpi=80)

####### PLOT NORMALIZED VOLUME @ DEFAULT ANGLE #######

norm_vol_list = [x/volume(15) for x in vol_list]

plt.figure(num=2,figsize=(6*PHI,6), dpi=80)
plt.plot(deg_list,norm_vol_list,color='#7570B3',linewidth=2.5,linestyle="-")

plt.title('Volume of my pleated cup', fontsize=18)
plt.ylim(0, 1.4)
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4],
           ['0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9',
            '1.0','1.1','1.2','1.3','1.4'])
plt.xlim(0, 90)
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90],
           ['0$^\circ$','5$^\circ$','10$^\circ$','15$^\circ$','20$^\circ$',
           '25$^\circ$','30$^\circ$','35$^\circ$','40$^\circ$','45$^\circ$',
           '50$^\circ$','55$^\circ$','60$^\circ$','65$^\circ$','70$^\circ$',
           '75$^\circ$','80$^\circ$','85$^\circ$','90$^\circ$' ])

##### Default angle lines #####
t = 15
plt.plot([t,t],[0,1],color='y',linewidth=2.5,linestyle="--")
plt.plot([0,t],[1,1],color='y',linewidth=2.5,linestyle="--")
plt.annotate('Volume at default angle',
         xy=(t, 1), xycoords='data',
         xytext=(10, -10), textcoords='offset points', fontsize=14)

##### Maximum volume angle lines #####
t = 41
plt.plot([t,t],[0,1.3],color='y',linewidth=2.5,linestyle="--")
plt.plot([0,t],[1.3,1.3],color='y',linewidth=2.5,linestyle="--")
plt.annotate('Maximum volume',
         xy=(t, 1.3), xycoords='data',
         xytext=(10, 5), textcoords='offset points', fontsize=14)


ax = plt.gca()
ax.set_xlabel('Angle of side (deg)', fontsize=16)
ax.set_ylabel('Normalized Volume', fontsize=16)

#ax.xaxis.set_major_locator(plt.MaxNLocator(19))
ax.yaxis.grid(True)
ax.xaxis.grid(False)

plt.show()
plt.savefig("ketchu_maximum.png",dpi=80)


