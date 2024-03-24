# 开发时间：2024/3/24  18:24
# The road is nothing，the end is all    --Demon

from flask import g
from financial.resources.transaction.const import DealType
from flask_restful import current_app
from flask_restful import Resource
from comment.utils.generate_trad_id import gen_trad_id
from flask_restful.reqparse import RequestParser

from comment.models.expected_return import Expected_return

from comment.models.deal_record import DealRecord
from comment.models.account import Account

from comment.models.invest_record import Invest_record
from comment.models import db

from datetime import datetime


class InvestIncomeResource(Resource):
    '''
    某个预期收益到期之后，获取当前的收益
    '''

    def get(self):
        rp = RequestParser()
        rp.add_argument('return_id')  # 指定预期收益的ID
        args = rp.parse_args()
        return_id = int(args.return_id)

        uid = g.user_id

        # 根据登录的用户查询资金账户对象
        account = Account.query.filter(Account.userId == uid).first()
        # 查询当前指定的预期收益对象
        expected_income = Expected_return.query.filter(Expected_return.id == return_id).first()

        if expected_income:
            # 判断当前的预期收益是否可以 开始获取收益
            cur_date = datetime.now()
            expected_date = expected_income.expectedDate.date()
            if cur_date >= expected_date:  # 如果当前日期大于投资到期的日期
                try:
                    # 查询对应的投资记录对象
                    invest = Invest_record.query.filter(Invest_record.pId == expected_income.investRecord).first()
                    invest.pStatus = 2  # 修改投资记录的状态

                    # 修改用户的资金账户
                    account.interestA += expected_income.expectedMoney  # 修改已经赚取的利息
                    account.interestTotal -= expected_income.expectedMoney  # 修改待收利息总额
                    account.investmentW -= invest.pAmount  # 修改待收本金总额
                    account.frozen -= invest.pAmount  # 修改冻结资金总额
                    before_balance = account.balance
                    account.balance += (invest.pAmount + expected_income.expectedMoney)  # 修改账户余额
                    account.total += expected_income.expectedMoney  # 修改账户总金额

                    # 生成交易流水号
                    del_num = gen_trad_id(DealType.income)
                    # 生成交易记录
                    deal_log = DealRecord(aUserId=uid, aReceiveOrPay=1, aTransferSerialNo=del_num,
                                          aTransferStatus=1, aBeforeTradingMoney=before_balance,
                                          aAmount=expected_income.expectedMoney, aAfterTradingMoney=account.balance,
                                          aDescreption='提取收益', aType=DealType.income.value)
                    db.session.add(deal_log)
                    db.session.commit()

                    return {'msg':'success'}
                except Exception as e:
                    current_app.logger.error(e)
                    db.session.rollback()

                    return {'message': '系统出错'}, 500
            else:
                return {'message': '投资未到期', 'code': 201}
        else:
            return {'message': '没有找到对应的预期收益'}
