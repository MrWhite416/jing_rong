# 开发时间：2024/3/3  19:49
# The road is nothing，the end is all    --Demon
from comment.models import db
from sqlalchemy import ForeignKey


# 债权还款的模型类
class Debtor_repay(db.Model):
    __tablename__ = 't_debtor_record'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='主键')
    claimsId = db.Column(db.BIGINT, ForeignKey('t_debt_info.id'), comment='债权id')
    debtInfo = db.relationship('Debt_info', backref=db.backref('debtor_record', lazy=True))
    receivableDate = db.Column(db.DateTime, comment='应还日期')
    receivableMoney = db.Column(db.Float(8, 2), comment='应还余额')
    currentTerm = db.Column(db.Integer, comment='当前还款期')
    recordDate = db.Column(db.DateTime, comment='记录日期')
    isReturned = db.Column(db.Integer, default=0, comment='是否还款')  # 0未还款 1已还款