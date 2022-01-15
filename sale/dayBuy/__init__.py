# import time
import pandas as pd
#
# # 格式化成2016-03-20 11:45:39形式
# print (time.strftime("%Y%m%d %H:%M:%S", time.localtime())[:8])
#
# str = "2021-12-17 15:00:00"
# print(str[11:])
# data_len = 23
# print((data_len -(data_len%4))-16)
#
# def compareInt(setInts):
#     maxInt = 0
#     for setInt in setInts:
#         if setInt>maxInt:
#             maxInt = setInt
#     return maxInt
#
# setInts = {2}
# setInts.add(int(3))
# setInts.add(int(2))
# print(compareInt(setInts))
bar_list = ['333','444']
df = pd.DataFrame(data=bar_list)
print(df)
if(len(df) > 0) :
    print(1)