# 开发时间：2024/3/3  19:47
# The road is nothing，the end is all    --Demon


from sqlalchemy import ForeignKey
from comment.models import db


# 债权表的模型类
class Debt_info(db.Model):
    __tablename__ = 't_debt_info'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    debtNo = db.Column(db.String(128), comment='债权编号')
    loanNo = db.Column(db.BIGINT, ForeignKey('t_loan.id'), comment='借款id')
    loanApply = db.relationship('Loan', backref=db.backref('debt_info', lazy=True, uselist=False))
    debtorsName = db.Column(db.String(64), comment='债务人名称')
    debtorsId = db.Column(db.String(128), comment='债务人身份证号')
    loanPurpose = db.Column(db.String(128), comment='借款用途')
    loanType = db.Column(db.Integer, comment='借款类型')
    loanStartDate = db.Column(db.DateTime, comment='原始借款开始日期')
    loanPeriod = db.Column(db.Integer, comment='原始借款期限')
    loanEndDate = db.Column(db.Date, comment='原始借款到期日期')
    repaymentStyle = db.Column(db.Integer, comment='还款方式')
    repaymenDate = db.Column(db.Integer, comment='还款日')
    repaymenMoney = db.Column(db.Float(8, 2), comment='还款金额')
    debtMoney = db.Column(db.Float(8, 2), comment='债权金额')
    debtYearRate = db.Column(db.Float(4, 2), comment='债权年化利率')
    debtMonthRate = db.Column(db.Float(4, 2), comment='债权月利率')
    debtTransferredMoney = db.Column(db.Float(8, 2), comment='债权转入金额')
    debtTransferredDate = db.Column(db.Date, comment='债权转入日期')
    debtTransferredPeriod = db.Column(db.Date, comment='债权转入期限')
    debtRansferOutDate = db.Column(db.Date, comment='债权转出日期')
    creditor = db.Column(db.String(64), comment='债权人')
    debtStatus = db.Column(db.Integer, comment='债权状态')
    borrowerId = db.Column(db.BIGINT, ForeignKey('t_user.id'),comment='借款人ID')
    user = db.relationship('User', backref=db.backref('debt_info', lazy=True))
    availablePeriod = db.Column(db.Date, comment='可用期限')
    availablePeriod = db.Column(db.Integer, comment='可用金额')
    matchedMoney = db.Column(db.Float(8, 2), comment='已匹配金额')
    matchedStatus = db.Column(db.Integer, comment='匹配状态')  # 0 未匹配  1 部分匹配  2 完全匹配
    repaymentStyleName = db.Column(db.String(64), comment='还款方式名称')
    debtStatusName = db.Column(db.String(64), comment='债权状态名字')
    matchedStatusName = db.Column(db.String(64), comment='匹配状态名称')
    debtType = db.Column(db.Integer, comment='标的类型')
    debtTypeName = db.Column(db.String(64), comment='标的类型名称')
