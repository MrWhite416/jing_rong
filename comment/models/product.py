# 开发时间：2024/2/23  14:16
# The road is nothing，the end is all    --Demon

from comment.models import db


# 理财产品的模型类
class Product(db.Model):
    __tablename__ = 't_product'
    proId = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='产品id')
    productName = db.Column(db.String(100), comment='产品名称')
    closedPeriod = db.Column(db.BIGINT, comment='转让封闭期', default=12)
    earlyRedeptionType = db.Column(db.Integer, comment='提前赎回类型', default=1)
    earningType = db.Column(db.Integer, comment='收益利率类型', default=134)
    investRule = db.Column(db.Integer, comment='数量规则', default=10)
    isAllowTransfer = db.Column(db.Integer, comment='是否可转让', default=0)
    isRepeatInvest = db.Column(db.Integer, comment='是否复投', default=0)
    lowerTimeLimit = db.Column(db.Integer, comment='产品最低期限', default=3)
    proLowerInvest = db.Column(db.BIGINT, comment='产品起投金额', default=1000)
    proNum = db.Column(db.String(100), comment='产品编号')
    proUpperInvest = db.Column(db.BIGINT, comment='产品投资上限', default=300000)
    proTypeId = db.Column(db.Integer, comment='产品投资上限', default=1)  # (1:表示正常；0：表示停用)
    status = db.Column(db.Integer, comment='状态', default=1)
    upperTimeLimit = db.Column(db.Integer, comment='产品最大期限', default=36)
    wayToReturnMoney = db.Column(db.Integer, comment='回款方式', default=109)  # （109：表示一次性回款 ，110：每月提取，到期退出）






