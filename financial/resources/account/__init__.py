# 开发时间：2024/2/27  12:15
# The road is nothing，the end is all    --Demon

from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

bp_account = Blueprint('account',__name__,url_prefix='/account')
account_api = Api(bp_account)

account_api.representation('application/json')(output_json)

from financial.resources.account.account_resource import *

account_api.add_resource(AccountInfo,'/funds',endpoint='funds')
account_api.add_resource(AccountExtract,'/extract',endpoint='extract')
account_api.add_resource(AccountRecharge,'/recharge',endpoint='recharge')

