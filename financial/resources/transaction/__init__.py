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
from financial.resources.transaction.debt_resource import *
from financial.resources.transaction.debt_repay_resource import *
from financial.resources.transaction.loan_resource import *
from financial.resources.transaction.match_resource import *
from financial.resources.transaction.all_matched_resource import *
from financial.resources.transaction.investIncome_resource import *
from financial.resources.transaction.matched_result_resourse import *
from financial.resources.transaction.expectReturn_resource import *


tran_api.add_resource(InvestResource,'/invest',endpoint='invest')  #
tran_api.add_resource(DealResource,'/deal',endpoint='deal')
tran_api.add_resource(Debt,'/debt',endpoint='debt')
tran_api.add_resource(RepayPlan,'/repay_plan',endpoint='repay_plan')
tran_api.add_resource(LoanApply,'/loan_apply',endpoint='loan_apply')
tran_api.add_resource(MatchUp,'/match_up',endpoint='match_up')
tran_api.add_resource(AllMatchedResource,'/all_matched',endpoint='all_matched')
tran_api.add_resource(ExpectedReturnResource,'/exceptedReturn',endpoint='exceptedReturn')
tran_api.add_resource(InvestIncomeResource,'/getIncome',endpoint='getIncome')
tran_api.add_resource(MatchedResultResource,'/matchedResult',endpoint='matchedResult')







