import configparser
import json
# 获取同花顺指定分组的代码
def get_ths_data(option):
    config = configparser.ConfigParser()
    config.read('C:\同花顺软件\同花顺\mx_196347693\StockBlock.ini',encoding='GB18030')
    #获取ini配置中的section的某个option下的option的值
    # print(config.get('BLOCK_STOCK_CONTEXT','E9'))
    #获取ini配置中的section的所有option
    # print('sections ','',config.sections())

    str = config.get('BLOCK_STOCK_CONTEXT',option)
    strs = str.split(',')
    # print(strs)

    result = set()
    #获取指定分组的股票的编号
    for strss in strs:
        sss = strss.split(':')
        if sss[0] != '':
            if sss[0] == '17':
                result.add('sh'+sss[1])
            elif sss[0] == '33':
                result.add('sz'+sss[1])
    # print(result)
    return result

#获取自选数据
# json.dump()  把数据写入json文件
# json.load()  把json文件内容读入python
def get_self_data():
    self_jsons = json.load(open('C:\同花顺软件\同花顺\mx_196347693\SelfStockInfo.json'))
    result = set()
    for self_json in self_jsons:
        m = self_json['M']
        if '33' == m:
            result.add('sz'+ self_json['C'])
        elif '17' == m:
            result.add('sh'+ self_json['C'])
    return result


# 调用函数
# get_ths_data('ee')
get_self_data()