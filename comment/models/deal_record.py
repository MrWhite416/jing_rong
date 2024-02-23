# 开发时间：2024/2/23  15:23
# The road is nothing，the end is all    --Demon
from datetime import datetime
from comment.models import db
from sqlalchemy import ForeignKey


# 交易记录的模型类
class DealRecord(db.Model):
    __tablename__ = 't_deal_log'
    aId = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='主键')
    aUserId = db.Column(db.BIGINT, ForeignKey('t_user.id'), comment='用户id')
    user = db.relationship('User', backref=db.backref('deal_log', lazy=True))
    pId = db.Column(db.BIGINT, ForeignKey('t_invest_record.pId'), comment='投资记录主键')
    investRecord = db.relationship('Invest_record', backref=db.backref('deal_log', lazy=True))
    aCurrentPeriod = db.Column(db.Integer, comment='当前期')
    aReceiveOrPay = db.Column(db.Float(8, 2), comment='收付')
    aTransferSerialNo = db.Column(db.String(128), comment='交易流水号')
    aDate = db.Column(db.DateTime, default=datetime.now(), comment='交易时间')
    aType = db.Column(db.Integer, comment='交易类型', default=0)
    aTransferStatus = db.Column(db.Integer, comment='交易状态', default=0)
    aBeforeTradingMoney = db.Column(db.Float(8, 2), comment='交易前金额', default=0)
    aAmount = db.Column(db.Float(8, 2), comment='金额', default=0)
    aAfterTradingMoney = db.Column(db.Float(8, 2), comment='交易后金额', default=0)
    aDescreption = db.Column(db.String(128), comment='交易详情')