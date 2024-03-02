# 开发时间：2024/2/23  15:26
# The road is nothing，the end is all    --Demon

from comment.utils.Serializers import BasePaginateSerializer

class InvestRecordPaginateSerializer(BasePaginateSerializer):
    """投资记录列表的分页序列化"""

    def get_object(self, obj):
        return {
            'pId': obj.pId,
            'plan_name': obj.product.productName,
            'invest_amount': float(obj.pAmount),
            "yearRate": float(obj.pEarnings),
            "totalIncome": float(obj.pMonthInterest),
            'month_Income': float(obj.pMonthlyExtractInterest),
            'deal_date': obj.pBeginDate.strftime("%Y-%m-%d"),
            'period': obj.pDeadlineAsDay / 30,
            'status': obj.pStatus
        }



class DealRecordPaginateSerializer(BasePaginateSerializer):
    """交易记录列表的分页序列化"""

    def get_object(self, obj):
        return {
            'deal_date': obj.aDate.strftime("%Y-%m-%d"),
            'deal_type': obj.aType,
            "descrp": obj.aDescreption,
            "deal_amount": float(obj.aAmount),
            'aAfter_Money': float(obj.aAfterTradingMoney),
            'deal_status': '交易成功' if obj.aTransferStatus else '交易失败'
        }