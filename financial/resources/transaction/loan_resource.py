# 开发时间：2024/3/3  21:23
# The road is nothing，the end is all    --Demon

from datetime import datetime, timedelta
from dateutil import relativedelta
from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from financial.resources.transaction.const import LoanConfig
from financial.resources.transaction.serializer import LoanPaginateSerializer
from comment.models import db
from comment.models.debt_info import Debt_info
from comment.models.debt_repay import Debtor_repay
from comment.models.loanApply import Loan
from comment.models.user import User
from comment.utils.Financial_redis import fr
from comment.utils.generate_trad_id import gen_trad_id, decimal_truncation


# 借款
class LoanApply(Resource):

    # 借款申请
    def post(self):
        rp = RequestParser()
        rp.add_argument('holder', required=True)  # 借款人
        rp.add_argument('amount', required=True)  # 金额
        rp.add_argument('code', required=True)  # 电话
        rp.add_argument('loanMonth', required=True)  # 借款期数

        user_id = g.user_id
        cur_user = User.query.filter(User.id == user_id).first()

        args = rp.parse_args()
        amount = args.amount
        loan_month = args.loanMonth
        code = args.code
        username = cur_user.username


        # 验证传入的验证码是否正确
        # 从redis中获取之前保存的验证码
        try:
            real_code= fr.get('registerCode:{}'.format(cur_user.phone))
            if not real_code or real_code.decode != code:  # 数据库中没有code
                current_app.logger.info('验证码错误或失效')
                return {'message':'验证码错误或失效','code':201}
        except ConnectionError as e:
            current_app.logger.error(e)
            return {'message':'验证码判断的时候，数据库连接错误','code':201}

            # 创建借款记录
            apply = Loan(loanNum=amount, lUid=user_id, duration=loan_month, lName=username, lRate=LoanConfig.YEAR_RATE,
                         lRepayDay=datetime.now().day)
            db.session.add(apply)
            db.session.commit()
            return {'msg': 'success'}

        # 获取借款列表

    def get(self):
        '''管理员看到的借款列表'''
        rp = RequestParser()
        rp.add_argument('start')  # 开始时间
        rp.add_argument('end')  # 结束时间
        rp.add_argument('curPage')  # 当前页
        rp.add_argument('perPage')  # 每页数量
        rp.add_argument('approve_status')  # 审批状态

        args = rp.parse_args()
        start = args.get('start')
        end = args.get('end')
        curPage = int(args.get('curPage'))
        perPage = int(args.get('perPage'))
        status = int(args.get('approve_status'))

        # 根据status审批状态来筛选
        applyList = Loan.query.filter(Loan.status == status)
        if start and end:
            # 如果有时间筛选
            applyList = (applyList.filter(db.cast(Loan.applyDate, db.DATE) >=
                                          db.cast(start, db.DATE)).filter(
                db.cast(Loan.applyDate, db.DATE) <= db.cast(end, db.DATE)).
                         paginate(curPage, perPage, error_out=False))
        else:
            applyList = applyList.paginate(curPage, perPage, error_out=False)
        # 分页序列化
        data = LoanPaginateSerializer(applyList).to_dict()

        return {'msg': 'success', 'data': data}

    def put(self):
        '''审批借款'''
        '''修改借款的状态，产出债权，创建还款计划'''
        rp = RequestParser()
        rp.add_argument('applyId')  # 借款申请
        rp.add_argument('status')  # 借款状态
        args = rp.parse_args()
        loan_id = args.appluId
        status = args.status

        #  查询借款对象
        loan = Loan.query.filter(Loan.id == loan_id).filter()
        # 第一步：更新借款申请状态
        loan.update({'status':status})

        if status == '1':
            # 第二步：产生债权数据
            debt_no = gen_trad_id('debt')
            debtors_id=loan.user.idNum
            # 还款的最后时间
            end_date = datetime.now() + relativedelta(month=loan.duration)
            # 创建债权
            new_debt = Debt_info(debtNo=debt_no, debtorsName=loan.lName, loanNo=debt_no,
                                debtorsId=debtors_id, loanStartDate=datetime.now(), loanPeriod=loan.duration,
                                loanEndDate=end_date, repaymentStyle=loan.lRepayType, matchedMoney=0,
                                repaymenDate=loan.lRepayDay, repaymenMoney=loan.loanNum, matchedStatus=0,
                                debtMoney=loan.loanNum, debtYearRate=loan.lRate, debtTransferredMoney=0)
            db.session.add(new_debt)
            db.session.flush()  # 根据数据库主键自增机制，生成一个新的主键值

            # 第三步：创建还款计划
            self.create_repay_list(new_debt)
            # 一次性提交事务
            db.session.commit()

    def create_repay_list(self,new_debt):
        '''创建当前债权的还款计划'''

        # 月还款本金：借款的金额 / 借款的期数
        mount_cost = round(new_debt.repaymenMony / new_debt.loanPeriod,2)  # 四舍五入小数点后后两位
        # 月利息= 年利息/12
        mount_rate = round(LoanConfig.YEAR_RATE / 12,4)

        for m in range(1,new_debt.loanPeriod+1):
            # 每一期要还的利息 = 剩下的本金*月利息
            interest = round(new_debt.repaymenMony - mount_cost*
                             (m-1)*mount_rate,2)
            # 每一期要还款的总金额=每月本金+每月利息
            total = round(interest + mount_cost,2)
            # 创建每一期的还款计划对象
            repay_plan = Debtor_repay(claimsId=new_debt.id, receivableMoney=total,
                                      currentTerm=m, recordDate=datetime.now())
            db.session.add(repay_plan)









class MyLoanApply(Resource):
    '''用户看到的借款列表'''

    def get(self):

        rp = RequestParser()
        rp.add_argument('curPage')  # 当前页
        rp.add_argument('perPage')  # 每页数量

        args = rp.parse_args()
        curPage = int(args.get('curPage'))
        perPage = int(args.get('perPage'))

        u_id = g.user_id
        loan_list = Loan.query.filter(Loan.lUid==u_id).paginate(curPage)

        # 分页序列化
        data = LoanPaginateSerializer(loan_list).to_dict()

        return {'msg': 'success', 'data': data}
