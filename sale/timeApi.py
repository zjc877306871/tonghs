from datetime import datetime
import pandas as pd
def get_hource():
    hour = datetime.now().hour
    minute = datetime.now().minute
    # print(datetime.now())
    h = str(hour)
    m = str(minute)
    if 1 == len(m):
        m = '0'+ m
    mm = h + ':' + m
    print(mm)
    return mm

# get_hource()

def formart_date(time, formart):
    timeStr = ''
    if(len(time) > 0 ):
        timeStr = time.strftime(formart)
    else:
        timeStr = datetime.now().strftime(formart)

    return timeStr

formart_date('','%Y-%m-%d %H:%M')