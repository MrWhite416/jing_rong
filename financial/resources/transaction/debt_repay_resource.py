# 开发时间：2024/3/6  23:06
# The road is nothing，the end is all    --Demon

from datetime import datetime, timedelta
from dateutil import relativedelta
from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from financial.resources.transaction.const import LoanConfig
from financial.resources.transaction.serializer import RepayPlanSerializer
from comment.models import db
from comment.models.debt_info import Debt_info
from comment.models.debt_repay import Debtor_repay
from comment.models.loanApply import Loan
from comment.models.user import User
from comment.utils.decorators import login_required
from comment.utils.generate_trad_id import gen_trad_id


class RepayPlan(Resource):
    '''
    还款的资源类
    '''
    method_decorators = [login_required]

    def get(self):
        '''
        查询某一个（匹配成功的）债权所对应的还款计划
        :return:
        '''
        rp = RequestParser()
        rp.add_argument('debt_id', required=True)

        args = rp.parse_args()
        debt_id = int(args.get('debt_id'))

        repay_list = Debtor_repay.query.filter(Debtor_repay.claimsId == debt_id).all()

        data = RepayPlanSerializer(repay_list).to_dict()

        return {'msg': 'success', 'data': data}

    def post(self):
        '''
        还款到指定某个还款计划的某一期
        :return:
        '''
        rp = RequestParser()
        rp.add_argument('repay_id')  # 还款计划的id
        rp.add_argument('repay_amount')  # 该期应还款的金额

        args = rp.parse_args()
        repay_id = int(args.repay_id)
        repay_money = float(args.get('repay_amount'))


        user_id = g.user_id
        user = User.query.filter(User.id == user_id).filter()

        # 判断用户的账户余额是否足够还款
        if user.accountInfo.balance<repay_money:
            return {'message':'可用余额不足','code':201}
        else:
            # 扣除余额
            user.accountInfo.balance = user.accountInfo.balance - repay_money
            repay = Debtor_repay.query.filter(Debtor_repay.id == repay_id).first()
            # 更改还款状态
            repay.isReturned = 1
            # 记录还款的日期
            repay.recordDate = datetime.now()
            return {'msg':'success'}







