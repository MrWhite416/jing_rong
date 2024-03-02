# 开发时间：2024/2/27  13:24
# The road is nothing，the end is all    --Demon

from flask import g
from flask_restful import Resource
from financial.resources.transaction.const import DealType
from comment.models import db
from flask_restful.reqparse import RequestParser
from comment.utils.generate_trad_id import gen_trad_id
from comment.models.user import User
from comment.models.deal_record import DealRecord
from financial.resources.account.serializer import AccountInfoSerializer
from comment.utils.decorators import login_required
from comment.models.account import Account

class AccountInfo(Resource):

    method_decorators=[login_required]
    def get(self):
        '''
        查询当前用户的资金账户
        :return:
        '''
        u_id = g.user_id
        acc = Account.query.filter(Account.userId==u_id).first()

        if acc:
            return AccountInfoSerializer(acc).to_dict()
        else:
            return {'message':'账户资金不存在'},400


class AccountExtract(Resource):
    # 使用了登录拦截器
    method_decorators = [login_required]

    def post(self):
        '''
        提现的接口
        :return:
        '''
        rp = RequestParser()
        rp.add_argument('amount',required=True)  # 金额
        rp.add_argument('card_id',required=True)  # 卡号
        rp.add_argument('payPwd',required=True)  # 支付密码

        args = rp.parse_args()
        amount = float(args.amount)
        card_id = args.card_id
        pay_pwd = args.payPwd

        u_id = g.user_id
        # 查询当前登录的用户
        user = User.query.filter(User.id==u_id).first()

        if not user.check_pay_password(pay_pwd):
            return {'code':201,'message':'支付密码错误'}

        # 查询用户资金账户
        acc = Account.query.filter(Account.userId==u_id).first()

        if acc:
            if acc.balance<amount:  # 当前账户资金超出提现金额
                return {'message':'超出了可提取的金额'}
            else:
                # 交易之前的可用余额
                before_balance = acc.balance
                # 修改新的余额
                acc.balance= float(acc.balance) - amount
                # 修改新的总金额
                acc.total = float(acc.tatal) - amount
                # 生成流水号
                deal_id = gen_trad_id(DealType.extract.name)
                '''提现： 调用银行的接口实现真正的提现'''

                # 新增一条交易记录对象
                deal_log= DealRecord(aUserId=u_id,aReceiveOrpay=1,aTransferSerialNo=deal_id,
                                     aTransfersattus=1,aBeforeTradingMoney=before_balance,
                                     aAmount=amount,aDescreption='提现',aType=DealType.extract.value)
                db.session.add(deal_log)
                db.session.commit()
                return {'message':'success'}


# 充值
class AccountRecharge(Resource):
    '''
    账户资金的充值
    '''


    def post(self):
        rp = RequestParser()
        rp.add_argument('amount',required=True)
        rp.add_argument('selectedIndex',required=True)

        args = rp.parse_args()
        amount = float(args.amount)
        selected_bank_id = args.selectedIndex

        u_id = g.user_id
        # 查询当前登录的用户
        user = User.query.filter(User.id == u_id).first()

        # 查询用户资金账户
        acc = Account.query.filter(Account.userId == u_id).first()

        if acc:

            # 交易之前的可用余额
            before_balance = acc.balance
            # 修改新的余额
            acc.balance = float(acc.balance) + amount
            # 修改新的总金额
            acc.total = float(acc.total) + amount
            # 生成流水号
            deal_id = gen_trad_id(DealType.recharge.name)
            '''充值 ： 调用银行的接口实现真正的提现'''

            # 新增一条交易记录对象
            deal_log = DealRecord(aUserId=u_id, aReceiveOrPay=0, aTransferSerialNo=deal_id,
                                  aTransferStatus=1, aBeforeTradingMoney=before_balance,
                                  aAmount=amount,aDescreption='充值', aType=DealType.recharge.value)
            db.session.add(deal_log)
            db.session.commit()
            return {'message': 'success'}



















