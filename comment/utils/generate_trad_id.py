# 开发时间：2024/2/26  21:20
# The road is nothing，the end is all    --Demon

'''
生成流水号的工具
'''

import random
import datetime



def gen_trad_id(trad_type='',date=None):
    '''
    生成资金交易的流水号
    规则：交易类型 + 4位的随机数 + 交易时间（年月日）组成的流水号
    :param trad_type:
    :param date:
    :return:
    '''

    if date is None:
        date = datetime.datetime.now()
    str_date = date.strftime('%Y-%m-%d')

    str_random = random.randint(1000,9999)

    return '{}{}{}'.format(trad_type,str_random,str_date)

