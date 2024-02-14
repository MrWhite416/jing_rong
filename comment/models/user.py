# 开发时间：2024/2/11  20:20
# The road is nothing，the end is all    --Demon

'''
用户资源
'''

from comment.models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 用户的模型类
class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), comment='用户名')
    password = db.Column(db.String(128), comment='密码')
    payPassword = db.Column(db.String(128), comment='支付密码')
    payPwdStatus = db.Column(db.Integer, comment='支付密码验证', default=0)
    email = db.Column(db.String(100), comment='邮箱')
    emailStatus = db.Column(db.Integer, comment='邮箱验证', default=0)  # 1代码正常
    inviteId = db.Column(db.Integer, comment='邀请码')
    ip = db.Column(db.String(128), comment='ip')
    phone = db.Column(db.String(11), comment='手机号')
    onlock = db.Column(db.Integer, comment='用户状态')  # 0代码正常
    phoneStatus = db.Column(db.Integer, comment='手机验证', default=1)  # 1代码正常
    realName = db.Column(db.String(64), comment='真实姓名')
    remark = db.Column(db.String(500), comment='备注')
    realNameStatus = db.Column(db.Integer, comment='实名认证', default=0)  # 代表已认证
    nick_name = db.Column(db.String(200), comment='昵称')
    avatar = db.Column(db.String(128), comment='头像')
    idNum = db.Column(db.String(64), comment='身份证号码')
    sumFriends = db.Column(db.Integer, comment='邀请数量统计')
    role = db.Column(db.Integer, comment='是否管理员', default=0)  # 0普通用户 1管理员

    loginTime = db.Column(db.DateTime, default=datetime.now(), comment='登录时间')
    registerTime = db.Column(db.DateTime, default=datetime.now(), comment='用户注册的时间')

    # 定义pwd的getter函数
    @property
    def pwd(self):
        return self.password  # 密文的密码

    @pwd.setter
    # 定义pwd的setter函数
    def pwd(self, x_password):
        '''
        根据明文的密码，加密得到密文
        :param x_password: 密码的明文
        :return: 加密之后的密文
        '''
        self.password = generate_password_hash(x_password)  # 加密

    def check_password(self, x_password):
        '''
        验证密码是否正确
        :param x_password: 明文的密码
        :return: 验证是否成功的bool值
        '''

        return check_password_hash(self.password, x_password)

    @property
    def pay_pwd(self):
        """
        支付密码
        """
        return self.payPassword

    @pay_pwd.setter
    def pay_pwd(self, p_password):
        self.payPassword = generate_password_hash(p_password)  # 根据flask提供的算法来加密

    def check_pay_password(self, p_password):
        return check_password_hash(self.payPassword, p_password)
