# 开发时间：2024/2/25  14:53
# The road is nothing，the end is all    --Demon
from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

bp_tran = Blueprint('tran',__name__,url_prefix='/tran')
tran_api = Api(bp_tran)

tran_api.representation('application/json')(output_json)

from financial.resources.transaction.invest_resource import *
from financial.resources.transaction.deal_record_resource import *


tran_api.add_resource(InvestResource,'/invest',endpoint='invest')
tran_api.add_resource(DealResource,'/deal',endpoint='deal')







