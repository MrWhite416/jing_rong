# 开发时间：2024/2/13  15:32
# The road is nothing，the end is all    --Demon
import os.path
import random
import json

from flask_restful import Resource
from flask import Response, current_app, request, g
from flask_restful.reqparse import RequestParser
from comment.models.user import User
from comment.models.account import Account
from comment.utils.limiter import limiter as lmt
from comment.utils.SMS import send_code
from comment.utils.Financial_Redis import fr
from comment.models import db
from financial.resources.user import constans
from flask_limiter.util import get_remote_address
from comment.utils.token_pyjwt import generate_tokens, verify_tokens
from comment.utils.decorators import login_required
from financial.resources.user.serializser import InvitedListSerializer,UserInfoSerializer
from financial.resources.account.serializer import AccountInfoSerializer


class TestUser(Resource):
    '''
    用于测试用户资源类
    '''

    def get(self):
        return {'test': 'get响应'}

    def post(self):
        return {'test': 'post响应'}

    def put(self):
        return {'test': 'put响应'}


class Login(Resource):
    '''
    登录
    '''

    def post(self):
        rp = RequestParser()
        rp.add_argument('username', required=True)
        rp.add_argument('password', required=True)
        args = rp.parse_args()
        username = args.get('username')
        password = args.get('password')

        user = User.query.filter(User.username == username).first()
        if user:
            # 验证密码是否正确
            if user.check_password(password):
                # 用户登录成功，之后产生一个token，以便于后面去认证token
                token = generate_tokens(user.id)
                current_app.logger.info(token)
                current_app.logger.info('测试token', verify_tokens(token))
                return {"token": token}
            return {'message': '用户名或者密码错误', 'code': 201}


class LoginOut(Resource):
    '''
    退出登录
    '''

    # flask中使用装饰器是，直接将装饰器添加到给method_decorators列表
    method_decorators = [login_required]

    # 如果想给当前类的某个视图函数个性化的使用装饰器
    # 不写就是不加装饰器
    # method_decorators = {
    #     '函数名':['装饰器'],
    #     'post':[login_required],
    #     'get':[]
    # }

    # 具体删除token操作在前端实现
    def post(self):
        if g.user_id:
            g.user_id = None
        return {'msg': '成功退出登录'}


class UserAvatar(Resource):
    '''
    管理用户的头像
    '''

    # 需要验证登录与否
    method_decorators = [login_required]

    def post(self):
        '''
        上传用户头像图片
        :return:
        '''

        # 用户上传的图片数据
        # files获取用户上传的所有文件，是字典类型
        img_data = request.files['file']

        u_id = g.user_id
        user = User.query.filter(User.id == u_id).first()

        # 设置用户头像图片保存路径
        img_dir = current_app.config['AVATAR_DIR']
        # 设置头像文件的名字，img_data.filename 原始的文件名
        img_name = str(u_id) + '_' + img_data.filename

        file_path = img_dir + '\\' + img_name

        # 保存文件
        try:
            img_data.save(file_path)
        except Exception as e:
            current_app.logger.error(e)
            return {'message':'头像文件上传失败'}


        # 在数据库中保存用户头像图片的文件名
        if user:
            user.avatar = img_name
            db.session.commit()
            return {'msg': '上传头像图片成功', 'avatar': img_name}


class RegisterUser(Resource):
    '''
    用户注册的资源
    '''

    def get(self):
        pass

    def post(self):
        rp = RequestParser()
        rp.add_argument('phone', required=True)
        rp.add_argument('code', required=True)
        rp.add_argument('password', required=True)
        rp.add_argument('username', required=True)
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
            return {'message': '用户名重复，请更换', 'code': 201}

        # 从redis中获取之前保存的验证码
        # real_code = fr.get(f'registerCode:{phone}')
        # print(real_code, '++++++++++++++')
        # print(code, real_code.decode())
        # if not real_code or code != real_code.decode():
        #     current_app.logger.info('验证码错误或者失效！')
        #     return {'message': '验证码错误或者失效！', 'code': 201}

        user = User(username=username, phone=phone, pwd=password)

        # 验证和关联邀请码
        if invite_code:
            self.check_invite(user, invite_code)

        # 保存用户到数据库
        try:  # 需要用到数据库的事务处理
            db.session.add(user)
            db.session.flush()  # 把数据插入数据库的缓冲区（得到自增的id），并不是真正的插入数据
            account = Account(userId=user.id)  # 创建当前用户的账户对象
            db.session.add(account)
            db.session.commit()  # 真正的插入数据操作
            return {'msg': 'success'}

        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()  # 回滚，哪一步报错就回到哪一步
            return {'message': '用户注册时，插入数据库失败', 'code': 201}

    def check_invite(self, user, invite_code):
        code = invite_code.strip()
        invite_user = User.query.filter(User.inviteId == code).first()
        if invite_user:
            user.invite_user_id = invite_user.id  # 如果邀请码有效，则把这两个用户关联一下
            invite_user.accountInfo.discount += constans.INVITE_MONEY  # 邀请用户的账户中增加50元的代金券
            invite_user.sumFriends = invite_user.sumFriends + 1 if invite_user.sumFriends else 1  # 邀请新用户的数量加一


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
        rp.add_argument('phone', required=True)

        # 验证参数
        args = rp.parse_args()

        # 获取参数
        phone = args.get('phone')

        # 设置验证码
        code = random.randint(000000, 999999)
        sms = send_code(phone, str(code))
        sms = json.loads(sms)  # 把json转为字典
        if sms['code'] == 2:
            current_app.logger.info(f'给手机号为：{phone}，发送短信成功！')

            # 验证码需要存放起来，存放在redis数据库中（redis快、适合缓存）
            # 需要用验证码和用户输入的进行验证
            # setex参数：1.key 2.时效 3.vlue
            # 时效单位是s
            fr.setex(f'registerCode:{phone}', constans.SMS_CODE_EXPIRES, code)

            # sms['phone'] = phone

            return {'msg': 'success', 'smsCode': code}
        else:
            return {'message': '发送短信失败', 'code': 201}


class IsExistPhone(Resource):
    '''
    验证手机号是否存在
    '''

    def post(self):  # post 请求中，请求的参数往往会封装成一个json对象
        phone = request.json.get('phone')
        user = User.query.filter(User.phone == phone).first()
        if user:
            return {'isExist': True, 'message': '此手机号已经注册', 'code': 203}
        return {'msg': 'success'}


class Invite(Resource):
    '''
    邀请码奖励管理的资源
    '''

    def post(self):
        '''
        生成邀请码
        :return:
        '''
        u_id = g.user_id
        user = User.query.filter(User.id == u_id).first()
        # 根据用户名，采用uuid算法生成一个唯一邀请码
        import uuid
        invite_code = str(uuid.uuid5(uuid.NAMESPACE_DNS, user.username))
        user.inviteId = invite_code
        db.session.commit()  # 保存到数据库中
        return {'message': 'success', 'invite_code': invite_code}

    def get(self):
        '''
        查询被邀请人的列表
        :return:
        '''
        u_id = g.user_id

        # 查询被邀请的人
        invited_list = User.query.filter(User.invite_user_id == u_id).all()
        if invited_list:
            data = InvitedListSerializer(invited_list).to_dict()
            return {'message': 'success', 'list': data}
        return {}


class UserInfo(Resource):
    '''
    用户信息的资源类
    '''

    method_decorators = [login_required]

    def get(self):
        '''
        当前登录用户的查询，包括所关联的账户信息
        :return:
        '''
        u_id = g.user_id
        user = User.query.filter(User.id == u_id).first()
        user_info_data = UserInfoSerializer(user).to_dict()

        # 查询当前账户所对应的账户信息
        acc = Account.query.filter(Account.userId == u_id).first()

        acc_data = {}
        if acc:
            acc_data = AccountInfoSerializer(acc).to_dict()

        return {'roles':['admin'] if user.role else ['user'],
                'name':user.username,
                'userInfoData':user_info_data,
                'accountInfo':acc_data
                }




