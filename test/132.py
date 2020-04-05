
# -*- coding: utf-8 -*-
'''
-------------------------------------------------------------------------------
Filename   : SUNRISE_SUNSET.py
Date       : 2013-01-07
Author     : Joe Lotz
Purpose    : Trying to recreate a graphic using matplotlib.
Data       : sunrise_sunset.csv
Sources    : [1] http://visual.ly/daylight-saving-time-explained
             [2] http://aa.usno.navy.mil/data/docs/RS_OneYear.php
-------------------------------------------------------------------------------
'''
import matplotlib.pyplot as plt
import matplotlib as mpl
#import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import datetime as dt
from matplotlib.dates import MonthLocator, DateFormatter

plt.close()

def getDay(x): return int(x[-2:])
def getMonth(x): return int(x[-5:-3])
def getYear(x): return int(x[:4])
def convertTime(x):
    hour,mins = x.split(':')
    return int(hour)+float(mins)/60
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
def format_date(t, pos=None):
    date = t
    if date.month == 1: 
      return date.strftime('%b %Y')
    else: return date.strftime('%b')


PHI = 1.618  # golden ratio
ORANGE = rgb_to_hex((254,177,99))
PURPLE = rgb_to_hex((255,100,200))
GREY   = rgb_to_hex((20,20,20))


data = pd.read_csv('Seattle_sunrise_sunset.csv', sep=',')

# Make a series of events 1 day apart
x = mpl.dates.drange(dt.datetime(2013,1,1),
                     dt.datetime(2013,12,31),
                     dt.timedelta(days=1))

day = map(getDay,data.Date)
month = map(getMonth,data.Date)
year = map(getYear,data.Date)

#date = data.Date
#sunrise = data.Sunrise
#sunset = data.Sunset

t = []
for index in range(len(day)):
    t.append(dt.date(year[index],month[index],day[index]))

sunrise = map(convertTime,data.Sunrise)
sunset = map(convertTime,data.Sunset)
#daylength = map(convertTime,data.Daylength)
avg_sunrise = np.ones(len(sunrise))*np.mean(sunrise)
avg_sunset = np.ones(len(sunset))*np.mean(sunset)

# Create a new figure w/ 6 point height, using 80 dots per inch
plt.figure(figsize=(6*PHI,6), dpi=80)
plt.subplot(1,1,1)

# Plot data
plt.plot(t,sunrise,color=PURPLE, linewidth=2.5, linestyle="-", label="Sunrise")
plt.plot(t,avg_sunrise,color=PURPLE,linewidth=3, linestyle=":", label="Average sunrise")
plt.plot(t,sunset, color=ORANGE, linewidth=2.5, linestyle="-", label="Sunset")
plt.plot(t,avg_sunset,color=ORANGE,linewidth=3, linestyle=":", label="Average sunset")

#
#ax1.plot(r.date, r.close, lw=2)
plt.fill_between(t, sunrise, np.zeros(len(t)), facecolor=GREY, alpha=0.5)
plt.fill_between(t, sunset, np.ones(len(t))*24, facecolor=GREY, alpha=0.5)

plt.legend(loc='upper right')

# Set y limits
plt.ylim(0, 24)
plt.yticks([0,2,4,6,8,10,12,14,16,18,20,22,24], 
           ['12 am','2 am','4 am','6 am','8 am','10 am','12 pm','2 pm','4 pm',
            '6 pm','8 pm','10 pm','12 am'])

ax = plt.gca()
ax.set_xlabel('Month', fontsize=20)
ax.set_ylabel('Sunrise / sunset times', fontsize=20)

months    = MonthLocator(range(1,13), bymonthday=1, interval=1)
monthsFmt = DateFormatter("%b")
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)

#for label in ax.get_xticklabels() :
#    label.set_fontproperties('sans-serif')

      
plt.show()

#savefig("sunrise_sunset.png",dpi=80)