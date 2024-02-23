# 开发时间：2024/2/23  15:26
# The road is nothing，the end is all    --Demon

from comment.utils.Serializers import BaseListSerializer

class ProductListSerializer(BaseListSerializer):
    '''产品列表的序列化'''

    def to_dict(self):
        lst = []
        for obj in self.data_list:
            lst.append(
                {
                    'id': obj.proId,
                    'proNum': obj.proNum,
                    'productName': obj.productName,
                    'minLimit': obj.lowerTimeLimit,
                    'maxLimit': obj.upperTimeLimit,
                    'earning': '年利率' if obj.earningType == 134 else '月利率',
                    'ReturnMoney': '一次性回款' if obj.wayToReturnMoney == 110 else '每月部分回款',
                    'closedPeriod': obj.closedPeriod,
                    'status': obj.status,
                    'proLowerInvest': obj.proLowerInvest
                }
            )
        return lst

class ProductRateListSerializer(BaseListSerializer):
    """产品利率的序列化"""

    def to_dict(self):
        lst = {}
        for obj in self.data_list:
            lst.update({
                obj.month:
                    {
                        'id': obj.id,
                        'proId': obj.productId,
                        'month': obj.month,
                        'incomeRate': float(obj.incomeRate)
                    }
            }
            )
        return lst