# 开发时间：2024/2/16  14:37
# The road is nothing，the end is all    --Demon

from flask import g,current_app,request
from comment.utils.token_pyjwt import verify_tokens


def jwt_request_authorization():
    '''
    自定义一个请求钩子，验证token，并把验证成功之后的
    用户id保存到全局变量g中
    :return:
    '''
    g.user_id = None  # 定义一个变量user
    try:
        # 前端代码把token携带在请求头中
        token = request.headers.get('token')

    except Exception as e:
        current_app.logger.info('请求头中没有token')
        return
    if token is not None:
        result = verify_tokens(token)
        if 'id' in result:  # 如果验证成功，那么字典中一定有用户id
            g.user_id = result['id']


















