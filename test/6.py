# encoding=utf-8
__author__ = 'liuqianchao'
class Passenger:
    passenger_id=0
    originating_Station=0
    terminus_Staion=0
    arrtiveStation_time=0#到起点站时间
    board_begintime=0#开始排队上车时间
    board_finishtime=0#登车时间
    getout_begintime=0#到终点站时间
    getout_finishtime=0#到终点站时间

    def __init__(self, id, originating_Station_num, terminus_Staion_num, arrtiveStation_time):
        hi(a,b,c,d,e,f)
        self.passenger_id=id
        self.originating_Station=originating_Station_num
        self.terminus_Staion=terminus_Staion_num
        self.arrtiveStation_time=arrtiveStation_time
        self.getout_finishtime=0