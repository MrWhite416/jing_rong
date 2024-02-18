# 开发时间：2024/2/15  14:45
# The road is nothing，the end is all    --Demon
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from comment.utils import const
from flask import current_app
from comment.models.user import User


def generate_tokens(u_id):
    '''
    一个用户在一次会话中生成后一个token
    :param u_id:
    :return:
    '''

    params = {
        'id': u_id,
        # exp 代表token的到期时间，必须传一个标准时间（类型是时间类型，单位是毫秒）
        # utcnow()当前系统时间，utc北京时区
        # 把秒转换为毫秒
        'exp': datetime.utcnow() + timedelta(seconds=const.JWT_EXPIRY_SECOND)
    }

    # 参数2：秘钥，参数3：算法
    # token的算法越复杂越好，并且必须不可逆
    # HA-256全称是SHA-256：密码散列函数算法。产生一个256bit长的哈希值，即密文（学名信息摘要）
    # 解码后是16进制的字符串
    return jwt.encode(payload=params, key=const.SECRET_KEY, algorithm='HS256')


def verify_tokens(token_str):
    '''
    验证token，如果验证成功，返回用户ID
    :param token_str:
    :return:
    '''
    try:
        # 返回之前生成token时传入的字典
        data = jwt.decode(token_str, key=const.SECRET_KEY, algorithms='HS256')
        current_app.logger.info(data)
        user = User.query.filter(User.id == data['id']).first()
        if user and user.onlock != 0:
            return {'id': user.id}
        else:
            return {'message': '数据库中不存在该用户，或者用户已过期'}

    except PyJWTError as e:
        current_app.logger.error(e)
        return {'message': 'token 验证识别'}
