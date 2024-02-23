# 开发时间：2024/2/22  21:58
# The road is nothing，the end is all    --Demon


from comment.utils.Serializers import BaseListSerializer

class BankCardListSerializer(BaseListSerializer):
    '''

    银行卡列表数据，序列化的类
    '''

    def to_dict(self):
        lst = []
        for card in self.data_list:
            lst.append({
                'cardId':card.bankInfoId,
                'cardNum':card.bankCardNum,
                'bankName':card.openingBank
            })

        return lst