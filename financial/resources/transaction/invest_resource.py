# 开发时间：2024/2/25  15:05
# The road is nothing，the end is all    --Demon

from flask import g
from financial.resources.transaction.const import DealType
from flask_restful import current_app
from flask_restful import Resource
from comment.utils.generate_trad_id import gen_trad_id
from flask_restful.reqparse import RequestParser
from comment.utils.decorators import login_required
from comment.models.product import Product
from comment.models.product_rate import Product_rate
from comment.models.user import User
from comment.models.deal_record import DealRecord
from comment.models.account import Account
from comment.models.funding_not_matched import Funding_not_matched
from comment.models.invest_record import Invest_record
from comment.models import db
from financial.resources.transaction.serializer import InvestRecordPaginateSerializer
from dateutil.relativedelta import relativedelta
from datetime import datetime


def calculate_income(rate, amount):
    '''计算每期的收益'''
    return round(rate / 100 / 12 * amount, 2)


class InvestResource(Resource):
    '''
    投资记录的资源类
    '''

    def get(self):
        '''
        投资记录的列表
        :return:
        '''

        rp = RequestParser()
        rp.add_argument('start')  # 起始时间
        rp.add_argument('end')  # 结束时间
        rp.add_argument('investType')  # 投资类型，初始值为0，表示‘购买中的计划’
        rp.add_argument('curPage', required=True)  # 当前页码
        rp.add_argument('pageSize', required=True)  # 每页显示数据条数

        args = rp.parse_args()
        start = args.get('start')
        end = args.get('end')
        investType = 0 if args.get('investType') == None else int(args.get('investType'))
        curPage = args.get('curPage')
        pageSize = args.get('pageSize')

        u_id = g.user_id

        # 当过滤逻辑较复杂时，建议分开写
        # 得到一个查询对象
        i_query = Invest_record.query
        # 开始过滤:1. 根据用户ID过滤
        i_query = i_query.filter(Invest_record.pUid == u_id)
        # 2. 根据投资类型过滤
        i_query = i_query.filter(Invest_record.pStatus == investType)
        # 3. 根据起始时间和结束时间过滤
        if start and end:
            # cast，转化数据类型，参1：被转化的字段，参2：转化为什么类型
            i_query = i_query.filter(db.cast(Invest_record.pDate, db.DATE) <= db.cast(start, db.DATE)).filter(
                db.cast(Invest_record.pDate, db.DATE) >= db.cast(end, db.DATE)
            )
        data = i_query.paginate(curPage, pageSize, error_out=False)

        data = InvestRecordPaginateSerializer(data).to_dict()
        return {'msg': 'success', 'data': data}

    def post(self):
        '''新增投资或者购买理财产品'''
        rp = RequestParser()
        rp.add_argument('productId', required=True)  # 产品ID
        rp.add_argument('pAmount', required=True)  # 金额
        rp.add_argument('period', required=True)  # 期数
        # rp.add_argument('discount', required=True)  # 抵扣金额

        args = rp.parse_args()
        product_id = int(args.productId)
        p_amount = int(args.pAmount)
        period = int(args.period)
        # discount = int(args.discount)

        user_id = g.user_id
        user = User.query.filter(User.id == user_id).first()

        # 查询产品对象
        product = Product.query.filter(Product.proId == product_id).first()

        # 查询产品对应的理财收益年利率，根据产品id和理财的期数
        pro_rate = Product_rate.query.filter(Product_rate.productId == product_id) \
            .filter(Product_rate.month == period).first()

        # 计算每期的收益
        income = calculate_income(pro_rate.incomeRate, amount=p_amount)

        # try:
        # 修改用户的资金账户 数据
        user_account_query = Account.query.filter(Account.userId == user_id)
        user_account = user_account_query.first()
        # 修改前的账户余额
        before_balance = user_account.balance
        print(before_balance,'==')
        # 判断是否可以抵扣金额，每邀请一个人可以得到50抵扣金额，每次投资只能最多抵扣五十元
        cur_discount = 50 if user_account.discount >= 50 else 0
        _p_amount = p_amount - cur_discount  # 得到真正要支付的金额
        print(_p_amount)
        if user_account.balance >= _p_amount:  # 账户余额足够
            before_balance = user_account.balance
            cur_balance = user_account.balance - _p_amount
            discount_balance = user_account.discount - cur_discount
        else:  # 账户余额不够
            return {'message': '可用余额不足'}

        interestTotal = income * period  # 当前这一次的投资总共要收到的利息
        # 修改
        user_account_query.update({
            'balance': cur_balance,
            'inverstmentA': user_account.inverstmentA + p_amount,
            'inverstmentW': user_account.inverstmentW + p_amount,
            'frozen': user_account.frozen + p_amount,
            'interestTotal': user_account.interestTotal + interestTotal,
            'discount': discount_balance
        })

        # 新增投资记录
        # 生车投资记录的流水号
        invest_num = gen_trad_id(DealType.invest.value)
        remark = '使用了50元的代金券' if cur_discount == 50 else '没有使用代金券'
        # 投资结束时间
        p_end_date = datetime.now() + relativedelta(months=period)
        # 精确的投资天数
        invest_days = (p_end_date - datetime.now()).days
        invest_record = Invest_record(pProductId=product_id, pUid=user_id, pBeginDate=datetime.now(),
                                      pEndDate=p_end_date, pSerialNo=invest_num, pAmount=p_amount,
                                      pEarnings=pro_rate.incomeRate,
                                      pDeadline=period, pMonthInterest=income,
                                      pMonthlyExtractInterest=income,
                                      pAvailableBalance=user.accountInfo.balance,
                                      pFrozenMoney=_p_amount, pProductName=product.productName,
                                      pDeadlineAsDay=invest_days, username=user.username,
                                      pProspectiveEarnings=interestTotal, pStatus=0, pRemark=remark)

        db.session.add(invest_record)
        db.session.flush()  # 得到id

        # 新增待匹配资金
        not_matched = Funding_not_matched(fInvestRecordId=invest_record.pId, fNotMatchedMoney=p_amount
                                          , fFoundingWeight=1, matchedStatus=0)
        db.session.add(not_matched)
        # 新增交易记录
        deal_num = gen_trad_id(DealType.invest.name)  # 交易流水号
        deal_record = DealRecord(aUserId=user_id, pId=invest_record.pId, aReceiveOrPay=1,
                                 aTransferSerialNo=deal_num,
                                 aTransferStatus=1, aBeforeTradingMoney=before_balance, aAmount=p_amount,
                                 aAfterTradingMoney=cur_balance, aDescreption='投资产品购买',
                                 aType=DealType.invest.value)
        db.session.add(deal_record)
        db.session.commit()
        return {'msg': 'success', 'data': ''}
        # except Exception as e:
        #     current_app.logger.error(e)
        #     db.session.rollback()
        #     print(e)
