from redisSelf import redisSelf
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer
import time
import tonghs
import timeApi
# 循环获取最近三天的redis的数据
# 解析redis数据中未操作的
#计算30分钟的10和5死叉。获取卖的价格然后计算收益
def Time_threading(inc):

    times = ['10:02','10:32','11:02','13:02','13:32','14:02','14:32']
    time_last = '14:48'
    connect = redisSelf.getRedisConnection()
    keys = get_need_redis_key('',connect,24)
    print(keys)
    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = timeApi.get_hource()
    if time_now == time_last:
        print(time_now)
        df = batch_stock_data('26',60,80,8,1)
        key = 'twenty:'+ timeApi.formart_date('','%Y%m%d')+':1500'
        conn = redisSelf.getRedisConnection()
        if(len(df) > 1):
            conn.set(key,df)
    i = 2
    for time in times:
        if time_now == time:
            print(time)
            df = batch_stock_data('26',60,(76+int((i-i%2)/2+i%2)),i,0)
            key = 'next:twenty:'+ timeApi.formart_date('','%Y%m%d:')+ stringApi.changeStr(time_now,'0')
            conn = redisSelf.getRedisConnection()
            print(len(df))
            if(len(df) > 1):
                conn.set(key,df)
        i = i+1



# 获取指定数量的redis缓存数据
def get_need_redis_key(now,connect,num):
    newkeys = [];
#   获取redis的keys进行排序。
    keys = connect.keys('twenty*')
    keys.sort(reverse=True)
    print(keys)
#     获取近三天24条的数据
    i = 0
    for key in keys:
        if  len(keys)<num:
            return keys
        else:
            if i<num:
                newkeys.append(key)
                i = i+1
    newkeys.sort(reverse=True)
    return newkeys



