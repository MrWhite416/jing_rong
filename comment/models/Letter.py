# 开发时间：2024/2/19  19:30
# The road is nothing，the end is all    --Demon
from comment.models import db
from sqlalchemy import ForeignKey
from datetime import datetime

# 站内信的模型类
class Letter(db.Model):
    '''
    收发消息的模型类
    '''
    __tablename__ = 't_letter'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    sendID = db.Column(db.String(64), doc='发送者名字')
    recID = db.Column(db.BIGINT, doc='接受者ID')
    detail_id = db.Column(db.BIGINT, ForeignKey('t_letter_detail.id'), doc='消息详情主键')
    letter_detail = db.relationship('Letter_Detail', backref=db.backref('letter',lazy=True))
    state = db.Column(db.Integer, doc='持否已读（0未读；1已读）')


# 站内信详情的模型类
class Letter_Detail(db.Model):
    '''
    消息详情的模型类，和 收发消息模型类 是 一对多 的关联关系
    '''

    __tablename__ = 't_letter_detail'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), doc='消息标题')
    detail = db.Column(db.String(256), doc='消息内容')
    pDate = db.Column(db.DateTime, default=datetime.now(), doc='发送时间')