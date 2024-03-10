# 开发时间：2024/3/8  21:22
# The road is nothing，the end is all    --Demon


from datetime import datetime
from sqlalchemy import ForeignKey
from comment.models import db


# 预期收益表的模型类
class Expected_return(db.Model):
    __tablename__ = 't_expected_return'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.BIGINT, ForeignKey('t_user.id'), comment='用户ID')
    productId = db.Column(db.BIGINT, ForeignKey('t_product.proId'), comment='产品ID')
    investRecord = db.Column(db.BIGINT, ForeignKey('t_invest_record.pId'), comment='投资记录ID')
    expectedDate = db.Column(db.DateTime, comment='收益日期')
    expectedMoney = db.Column(db.Float(8, 2), comment='收益金额', default=0)
    createDate = db.Column(db.DateTime, default=datetime.now(), comment='创建日期')