# 开发时间：2024/2/27  12:09
# The road is nothing，the end is all    --Demon

from enum import Enum  # 枚举类


class DealType(Enum):
    '''
    交易类型的枚举类
    '''
    all = 0  # 全部类型
    recharge = 1  # 充值
    extract = 2  # 提现
    invest = 3  # 投资
    income = 4  # 收益
    recycle = 5  # 回收本金
    match = 6  # 匹配结果


class LoanConfig(Enum):
    '''
    借款的年利率
    '''

    YEAR_RATE = 0.055