# 开发时间：2024/3/10  18:54
# The road is nothing，the end is all    --Demon

from sqlalchemy import ForeignKey
from comment.models import db


# 匹配结果表的模型类
class Matched_result(db.Model):
    __tablename__ = 't_matched_result'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='主键')
    userId = db.Column(db.BIGINT, ForeignKey('t_user.id'), comment='用户id')
    user = db.relationship('User', backref=db.backref('matched_result', lazy=True))
    debtId = db.Column(db.BIGINT, ForeignKey('t_debt_info.id'), comment='债权id')
    debt_info = db.relationship('Debt_info', backref=db.backref('matched_result', lazy=True))
    investId = db.Column(db.BIGINT, ForeignKey('t_invest_record.pId'), comment='投资记录主键')
    investRecord = db.relationship('Invest_record', backref=db.backref('matched_result', lazy=True))
    transferSerialNo = db.Column(db.String(100), comment='交易流水号')
    purchaseMoney = db.Column(db.Float(8, 2), comment='购买金额（匹配金额）', default=0)
    confirmedDate = db.Column(db.DateTime, comment='购买日期（匹配日期）')
    isConfirmed = db.Column(db.Integer, comment='是否确认', default=0)
    matchDate = db.Column(db.DateTime, comment='匹配上的日期', default=3)
    fundType = db.Column(db.Integer, comment='资金类型')
    debtType = db.Column(db.Integer, comment='债权类型')
    isExecuted = db.Column(db.Integer, comment='是否清算过')
