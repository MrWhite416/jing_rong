# 开发时间：2024/2/23  14:34
# The road is nothing，the end is all    --Demon


from comment.models import db
from sqlalchemy import ForeignKey


# 理财产品利率表
class Product_rate(db.Model):
    '''
    与产品表是多对一的关系
    '''

    __tablename__ = 't_product_rate'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='编号')
    incomeRate = db.Column(db.Float(4, 2), comment='利率值')
    month = db.Column(db.Integer, comment='月份', default=12)
    productId = db.Column(db.BIGINT, ForeignKey('t_product.proId'), comment='产品编号')
    product = db.relationship('Product', backref=db.backref('rateInfo', lazy=True))
