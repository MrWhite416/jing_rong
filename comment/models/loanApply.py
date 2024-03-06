# 开发时间：2024/3/3  19:37
# The road is nothing，the end is all    --Demon


from sqlalchemy import ForeignKey
from comment.models import db
from datetime import datetime


# 借款申请的模型类
class Loan(db.Model):
    __tablename__ = 't_loan'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    loanNum = db.Column(db.Float(8, 2), comment='借款金额')
    lUid = db.Column(db.BIGINT, ForeignKey('t_user.id'), comment='用户id')
    user = db.relationship('User', backref=db.backref('loanApply', lazy=True))
    duration = db.Column(db.Integer, comment='借款时长')
    lName = db.Column(db.String(64), comment='借款人姓名')
    lRepayType = db.Column(db.Integer, comment='还款模式', default=1)  # 1 等额本金 0 先息后本
    lRate = db.Column(db.Float(4, 2), comment='借款利率')
    lRepayDay = db.Column(db.Integer, comment='还款日', default=10)
    status = db.Column(db.Integer, comment='审批状态', default=0)  # 0未审批 1通过 2驳回
    applyDate = db.Column(db.DateTime, default=datetime.now(), comment='申请时间')




