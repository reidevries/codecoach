# encoding=utf-8

__author__ = 'liuqianchao'
class Staion:
    stationID=0
    parking=[]
    berthnumber=1
    waitingtime=0
    waitingpassenger=0
    passenger=[]
    stopstate=[]
    def __init__(self,id,berth_number):
        self.stationID=id
        self.passenger=[]
        self.parking=[]
        self.stopstate=[]
        self.berthnumber=berth_number
    def setwaitingpassenger(self,num):
        self.waitingpassenger=num
        self.waitingtime=int(self.waitingpassenger*1.5)

