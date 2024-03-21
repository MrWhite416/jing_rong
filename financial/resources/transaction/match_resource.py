# 开发时间：2024/3/10  19:02
# The road is nothing，the end is all    --Demon

from collections import deque
from datetime import datetime
from flask_restful import Resource
from comment.models.debt_info import Debt_info
from comment.models.matched_result import Matched_result
from comment.models.expected_return import Expected_return
from comment.models.funding_not_matched import Funding_not_matched
from comment.utils.generate_trad_id import gen_trad_id
from financial.resources.transaction.const import DealType
from sqlalchemy import or_
from flask import current_app
from comment.models import db
from dateutil.relativedelta import relativedelta


class MatchDequeue:
    """
    采用deque构建栈。
    deque是一个双端队列，把右侧禁用（只使用左端），即可作为栈来使用。
    """

    def __init__(self, item_list):
        """ 初始化栈 """
        self.items = deque(item_list)

    # 从栈中取一条待匹配的数据
    def get_item(self):
        return self.items.popleft()

    # 将一条待匹配的数据放入栈中
    def push(self, item):
        return self.items.appendleft(item)

    # 判断栈是否为空
    @property
    def empty(self):
        return len(self.items) == 0


class Match(object):
    """
    正式开始撮合匹配
    """

    def __init__(self):
        """
        初始化，把所有待匹配的债权和待匹配的资金都从数据库中取出来，
        并放入栈中
        """
        # 查询未匹配或者部分匹配的债权列表
        # order_by默认升序
        debt_list = Debt_info.query.filter(or_(Debt_info.matchedStatus == 0, Debt_info.matchedStatus == 1)).order_by(
            Debt_info.id).all()
        self.debt_deque = MatchDequeue(debt_list)

        # 未匹配或部分匹配的资金列表
        fund_list = Funding_not_matched.query.filter(
            or_(Funding_not_matched.matchedStatus == 0, Funding_not_matched.matchedStatus == 1)
        ).order_by(Funding_not_matched.fId).all()

        self.funds_Deque = MatchDequeue(fund_list)

    def start_match(self):
        """正式开始撮合匹配"""
        try:
            while (not self.funds_Deque.empty) and (not self.debt_deque.empty):
                debt_item = self.debt_deque.get_item()
                fund_item = self.funds_Deque.get_item()

            # 匹配的三种情况
            # 1.债权资金金额 大于 理财金额；2.债权资金金额 小于 理财金额；3.债权资金金额 等于 理财金额
            if debt_item.debtMoney > fund_item.fNotMatchedMoney:
                self.debtMoneyMoreThanFunds(debt_item, fund_item)
            elif debt_item.debtMoney < fund_item.fNotMatchedMoney:
                self.debtMoneyLessThanFunds(debt_item, fund_item)
            else:
                self.debtMoneyEqualFunds(debt_item, fund_item)

            db.session.commit()

            return {'msg':'匹配完成'}
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()  # 将数据库恢复到事务开始之前的状态
            return {'message': '服务器忙'}, 500

    # 债权资金部分匹配的业务逻辑
    def debtMoneyMoreThanFunds(self, debt_item, fund_item):
        """
        债权资金 大于 投资资金的情况， 新增一条匹配结果
        """
        self.createMatchedResult(debt_item, fund_item, fund_item.fNotMatchedMoney)
        debt_item.debtMoney -= fund_item.fNotMatchedMoney  # 债权剩下未匹配的金额
        debt_item.matchedStatus = 1  # 修改债权的匹配状态为1（部分匹配）
        debt_item.matchedMoney += fund_item.fNotMatchedMoney

        fund_item.fNotMatchedMoney = 0
        fund_item.matchedStatus = 2  # 修改债权的匹配状态为2（全部匹配）
        # 债权还剩下一点资金没有匹配，马上重新插入到栈里
        self.debt_deque.push(debt_item)
        # 投资理财的金额全部匹配完了，所以可以开始产生收益
        self.createExpectedReturn(fund_item)

    def debtMoneyLessThanFunds(self,debt_item, fund_item):
        """待匹配的债权资金 小于 投资理财资金的情况"""
        fund_item.fNotMatchedMoney -= debt_item.debtMoney  # 投资资金剩余未匹配的金额
        fund_item.matchedStatus = 1
        self.createMatchedResult(debt_item,fund_item,debt_item.debtMoney)
        debt_item.matchedMoney += debt_item.debtMoney  # 修改债权中已经匹配的金额
        debt_item.debtMoney = 0  # 匹配完成之后，修改债权的待匹配金额
        debt_item.user.accountInfo.balance += debt_item.repaymenMoney
        debt_item.matchedStatus = 2
        self.startRepayplay(debt_item)  # 正式开始还款计划
        self.funds_Deque.push(fund_item)  # 把剩余没有匹配的资金放入栈顶

    def debtMoneyEqualFunds(self,debt_item,fund_item):
        """
        第三种情况：投资金额 等于 债权金额
        :param debt:
        :param funds:
        :return:
        """
        debt_item.matchedStatus = 2  # 债权匹配状态 0未匹配 1部分匹配 2完全匹配
        debt_item.macthedMoney += debt_item.debtMoney   # 修改债权中已经匹配的金额
        self.createMatchedResult(debt_item,fund_item,debt_item.debtMoney)
        debt_item.debtMoney = 0  # 债权待匹配的金额

        fund_item.matchedStatus = 2
        fund_item.fNotMacthedMoney = 0
        self.createExpectedReturn(fund_item)
        self.startRepayPlay(debt_item)










    def startRepayPlay(self,debt):
        """正式生效还款计划"""
        repay_list = debt.debtor_record
        for i in range(len(repay_list)):
            repay_date = datetime.now() + relativedelta(months=(i+1))
            # 修改还款计划中还款时间
            repay_list[i] = receivableDate = repay_date


    def createMatchedResult(self, debt, funds, match_money):
        """
        创建一条匹配结果数据，并保存到数据库中
        :param debt:
        :param funds:
        :param funds_money:
        :return:
        """
        match_num = gen_trad_id(DealType.match.name)
        result = Matched_result(userId=funds.investRecord.pUid, debtId=debt.id, investId=funds.investRecord.pId,
                       transferSerialNo=match_num, purchaseMoney=match_money,
                       confirmedDate=funds.investRecord.pDate,
                       isConfirmed=1, matchDate=datetime.now())

        db.session.add(result)

    def createExpectedReturn(self, funds):
        """创建一条预期收益的记录"""
        ex_return = Expected_return(userId=funds.investRecord.pUid, productId=funds.investRecord.pProductId,
                                    investRecord=funds.investRecord.pId,
                                    expectedDate=datetime.now() + relativedelta(months=funds.investRecord.pDeadline),
                                    expectedMoney=funds.investRecord.pProspectiveEarnings)
        funds.investRecord.pStatus = 1
        # 修改 投资记录的开始计息时间
        funds.investRecord.pInterestStartDate = datetime.now()
        db.session.add(ex_return)


class MatchUp(Resource):
    def post(self):
        match = Match()
        return match.start_match()


