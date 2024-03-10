# 开发时间：2024/3/8  21:27
# The road is nothing，the end is all    --Demon

from sqlalchemy import ForeignKey
from comment.models import db


# 待匹配资金表的模型类
class Funding_not_matched(db.Model):
    __tablename__ = 't_funding_not_matched'
    fId = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='主键')
    fInvestRecordId = db.Column(db.BIGINT, ForeignKey('t_invest_record.pId'), comment='投资记录')
    investRecord = db.relationship('Invest_record', backref=db.backref('fundsNotMatched', lazy=True))
    fNotMatchedMoney = db.Column(db.Float(8, 2), comment='待匹配金额')
    fFoundingType = db.Column(db.Integer, comment='资金类型', default=1)
    fFoundingWeight = db.Column(db.Float(8, 2), comment='资金')
    matchedStatus = db.Column(db.Integer, comment='匹配状态')  # 0 未匹配  1 部分匹配  2 完全匹配
    fCreateDate = db.Column(db.DateTime, comment='创建时间')
