# 开发时间：2024/2/13  15:32
# The road is nothing，the end is all    --Demon
import random
import json

from flask_restful import Resource
from flask import Response,current_app,request,g
from flask_restful.reqparse import RequestParser
from comment.models.user import User
from comment.models.account import Account
from comment.utils.limiter import limiter as lmt
from comment.utils.SMS import send_code
from comment.utils.Flnancial_Redis import fr
from comment.models import db
from financial.resources.user import constans
from flask_limiter.util import get_remote_address



class TestUser(Resource):
    '''
    用于测试用户资源类
    '''

    def get(self):
        return {'test':'get响应'}

    def post(self):
        return {'test':'post响应'}


    def put(self):
        return {'test':'put响应'}


class RegisterUser(Resource):
    '''
    用户注册的资源
    '''
    def get(self):
        pass

    def post(self):
        rp = RequestParser()
        rp.add_argument('phone',required=True)
        rp.add_argument('code',required=True)
        rp.add_argument('password',required=True)
        rp.add_argument('username',required=True)
        rp.add_argument('invite_code')

        args = rp.parse_args()  # 验证参数

        # 获取参数
        username = args.username
        password = args.password
        phone = args.phone
        code = args.code
        invite_code = args.invite_code

        # 验证用户是否唯一
        u = User.query.filter(User.username == username).first()
        if u:
            return {'message':'用户名重复，请更换','code':201}

        # 从redis中获取之前保存的验证码
        real_code = fr.get(f'registerCode:{phone}')
        if not real_code or code != real_code.decode():
            current_app.logger.info('验证码错误或者失效！')
            return {'message':'验证码错误或者失效！','code':201}

        # 保存用户到数据库
        user = User(username=username,phone=phone,pwd=password)

        try:  # 需要用到数据库的事务处理
            db.session.add(user)
            db.session.flush()  # 把数据插入数据库的缓冲区（得到自增的id），并不是真正的插入数据
            account = Account(userId=user.id)  # 创建当前用户的账户对象
            db.session.add(account)
            db.session.commit()


        except Exception as e:
            current_app.logger.error(e)



class SendSMS(Resource):
    '''
    发送短信的资源
    '''

    error_message = 'Luoluoluoya many requests.'

    # 限流器列表
    decorators = [
        # 三个参数：限流速率，限制条件，超出限制条件的提示
        lmt.limit(constans.LIMIT_SMS_CODE_BY_MOBILE,
                  key_func=lambda: request.args.get('phone').strip(),
                  error_message=error_message),
        lmt.limit(constans.LIMIT_SMS_CODE_BY_IP,
                  key_func=get_remote_address,
                  error_message=error_message)
    ]

    def post(self):
        rp = RequestParser()
        rp.add_argument('phone',required=True)

        # 验证参数
        args = rp.parse_args()

        # 获取参数
        phone = args.get('phone')

        # 设置验证码
        code = random.randint(000000,999999)
        sms = send_code(phone,str(code))
        sms = json.loads(sms)  # 把json转为字典
        if sms['code'] == 2:
            current_app.logger.info(f'给手机号为：{phone}，发送短信成功！')

            # 验证码需要存放起来，存放在redis数据库中（redis快、适合缓存）
            # 需要用验证码和用户输入的进行验证
            # setex参数：1.key 2.时效 3.vlue
            # 时效单位是s
            fr.setex(f'registerCode:{phone}',constans.SMS_CODE_EXPIRES,code)


        # sms['phone'] = phone

            return {'msg':'success','smsCode':code}
        else:
            return {'message':'发送短信失败','code':201}


class IsExistPhone(Resource):
    '''
    验证手机号是否存在
    '''

    def post(self):  # post 请求中，请求的参数往往会封装成一个json对象
        phone = request.json.get('phone')
        user = User.query.filter(User.phone == phone).first()
        if user:
            return {'isExist':True,'message':'此手机号已经注册','code':203}
        return {'msg':'success'}

















