# 开发时间：2023/9/6  22:12
# The road is nothing，the end is all    --Demon

from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

'''用户蓝图'''

# 创建蓝图
bp_user = Blueprint('user',__name__,url_prefix='/user')

# 创建蓝图API
user_api = Api(bp_user)

# 使用自定义的json格式返回数据
user_api.representation('application/json')(output_json)


# 加载当前模块的资源
from financial.resources.user.user_resource import *

# 测试资源
# endpoint参数用于唯一的标识路由
user_api.add_resource(TestUser,'/test',endpoint='test')
user_api.add_resource(IsExistPhone,'/isExist',endpoint='isExist')
user_api.add_resource(SendSMS,'/sendSMS',endpoint='sendSMS')












