import tushare as ts
# d = ts.get_tick_data('603335',date='2021-12-16')
# print (d)
e = ts.get_hist_data('603335',start='2021-12-14',end='2021-12-16')
print (e)

token = '90e452d90760cd2625d813e6bb486c60822b93220ce3518bcd449cb1'
pro = ts.pro_api(token)
