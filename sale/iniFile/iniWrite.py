import configparser
import os
def get_ths_data(option,needDeleteData):
    # 获取文件地址
    # path ='D:\\finance\gp\客户端\同花顺\同花顺金融大师20190707\同花顺金融大师\mx_196347693\StockBlock.ini'
    path ='C:\同花顺软件\同花顺\mx_196347693\StockBlock.ini'

    config = configparser.ConfigParser()
    # config.read('D:\it\\test\StockBlock.ini',encoding='GB18030')
    config.read(path,encoding='GB18030')
    # 'C:\同花顺软件\同花顺\mx_196347693\StockBlock.ini'
    #获取ini配置中的section的某个option下的option的值
    # print(config.get('BLOCK_STOCK_CONTEXT','E9'))
    #获取ini配置中的section的所有option
    # print('sections ','',config.sections())
    needDealData = config.get('BLOCK_STOCK_CONTEXT',option)
    result = deleteStrData(needDealData,needDeleteData)
    config.set('BLOCK_STOCK_CONTEXT',option,result)
    # r+更新指定一列的数据
    with open(path,'r+') as f:
        config.write(f)

# get_ths_data('25')

def deleteStrData(needDealData,needDeleteData):
    datas = needDealData.split(',')
    result=''
    i=0
    for data in datas:
        if data not in needDeleteData:
            if i == 0:
                result = data+','
            else:
                result = result+data+','
        i = i+1
    return result[:len(result)-1]

def tranName(datas):
    result = set()
    for data in datas:
        if 'sh' == data[:2]:
            newData = '17:'+data[2:]
            result.add(newData)
        elif 'sz' == data[:2]:
            newData = '33:'+data[2:]
            result.add(newData)
    return result