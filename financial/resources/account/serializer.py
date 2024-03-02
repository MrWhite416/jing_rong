# 开发时间：2024/2/27  12:15
# The road is nothing，the end is all    --Demon

from comment.utils.Serializers import BaseSerializer

class AccountInfoSerializer(BaseSerializer):
    '''
    用户资金账户的序列化
    '''

    def to_dict(self):
        obj = self.data
        return {
            'total':float(obj.total),  # 账户总额
            'balance':float(obj.balance),  # 账户可用金额
            'profit':float(obj.interestA),  # 已投资金额
            'inverstmentW':float(obj.inverstmentW),  # 总计代收本金
            'interestTotal':float(obj.interestTotal),  # 总计代收利息
            'discount':float(obj.discount)  # 代金券
         }

