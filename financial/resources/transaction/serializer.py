# 开发时间：2024/2/23  15:26
# The road is nothing，the end is all    --Demon
from datetime import datetime

from comment.utils.Serializers import BasePaginateSerializer,BaseListSerializer
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

class DebtPaginateSerializer(BasePaginateSerializer):
    """债权的分页序列化"""

    def get_object(self, obj):
        return {
            'debtNo': obj.debtNo,
            'loanNo': obj.loanNo,
            "loanStartDate": obj.loanStartDate.strftime("%Y-%m-%d"),
            "repaymenDate": obj.repaymenDate,
            'debtYearRate': float(obj.debtYearRate),
            'debtMoney': float(obj.debtMoney),
            'debtOriginalMoney': float(obj.debtTransferredMoney),
            'matchedStatus': obj.matchedStatus,
            'matchedMoney': float(obj.matchedMoney),
            'debtStatus': obj.matchedStatus,
        }

class LoanApplyListSerializer(BaseListSerializer):
    """借款申请列表的序列化"""

    def to_dict(self):
        list = []
        for obj in self.data_list:
            list.append(
                {
                    'loanApplyId': obj.id,
                    'name': obj.lName,
                    "applyTime": obj.applyDate.strftime("%Y-%m-%d %H:%M:%S"),
                    "amount": float(obj.loanNum),
                    'duration': obj.duration,
                    'loanRate': float(obj.lRate),
                    'repayDay': obj.lRepayDay,
                    'repayType': obj.lRepayType,
                    'status': obj.status,
                    'matchedStatus': obj.debt_info.matchedStatus if obj.debt_info else None
                }
            )
        return list

class LoanPaginateSerializer(BasePaginateSerializer):
    """ 借款列表分页序列化"""

    def get_object(self, obj):
        return {
            'loanApplyId': obj.id,
            'name': obj.lName,
            "applyTime": obj.applyDate.strftime("%Y-%m-%d %H:%M:%S"),
            "amount": float(obj.loanNum),
            'duration': obj.duration,
            'loanRate': float(obj.lRate),
            'repayDay': obj.lRepayDay,
            'repayType': obj.lRepayType,
            'status': obj.status,
            'debt_match_status': obj.debt_info.matchedStatus if obj.debt_info else '',
            'debt_id': obj.debt_info.id if obj.debt_info else '',

        }

class RepayPlanSerializer(BaseListSerializer):
    """还款计划的序列化"""

    def to_dict(self):
        list = []
        for obj in self.data_list:
            list.append(
                {
                    'id': obj.id,
                    'currentTerm': obj.currentTerm,
                    'receivableDate': obj.receivableDate.strftime("%Y-%m-%d"),
                    "receivableMoney": float(obj.receivableMoney),
                    'isReturned': obj.isReturned,
                }
            )
        return list


class AllMatchedPaginateSerializer(BasePaginateSerializer):
    """
    所有的待匹配资金 和 已经匹配资金的序列化
    """

    def get_object(self, obj):
        return {
            'weigh': 0,
            'username': obj.investRecord.user.username,
            "InvestRecordNum": obj.investRecord.pSerialNo,
            "productName": obj.investRecord.product.productName,
            'investDate': obj.investRecord.pDate.strftime("%Y-%m-%d"),
            'period': obj.investRecord.pDeadlineAsDay / 30,
            'notMatchedMoney': float(obj.fNotMatchedMoney),
            'matchStatus': obj.matchedStatus,
        }


class ExpectedReturnPaginateSerializer(BasePaginateSerializer):
    """预期收益表的分页序列化"""

    def get_object(self, obj):
        return {
            'return_id': obj.id,
            'userId': obj.userId,
            'productId': obj.product.productName,
            "investRcordID": obj.investRecord,
            "expectedDate": obj.expectedDate.strftime("%Y-%m-%d"),
            # date 日期的 时间戳
            'expectedStamp': datetime.timestamp(datetime(obj.expectedDate.date().year, obj.expectedDate.date().month,
                                                         obj.expectedDate.date().day)),
            'return_Money': float(obj.expectedMoney),

        }


class MatchedResultPaginateSerializer(BasePaginateSerializer):
    """ 匹配结果分页 序列化"""

    def get_object(self, obj):
        return {
            'userId': obj.userId,
            'debtId': obj.debtId,
            "investId": obj.investId,
            "transNo": obj.transferSerialNo,
            'Money': float(obj.purchaseMoney),
            'matchDate': obj.matchDate.strftime("%Y-%m-%d %H:%M:%S")
        }


