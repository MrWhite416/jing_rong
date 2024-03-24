# 开发时间：2024/3/24  22:38
# The road is nothing，the end is all    --Demon
from flask import g
from financial.resources.transaction.const import DealType
from flask_restful import current_app
from flask_restful import Resource
from comment.utils.generate_trad_id import gen_trad_id
from flask_restful.reqparse import RequestParser
from comment.utils.decorators import login_required
from comment.models.expected_return import Expected_return
from comment.models.product_rate import Product_rate
from comment.models.user import User
from comment.models.matched_result import Matched_result
from comment.models.account import Account
from comment.models.funding_not_matched import Funding_not_matched
from comment.models.invest_record import Invest_record
from comment.models import db
from financial.resources.transaction.serializer import MatchedResultPaginateSerializer
from dateutil.relativedelta import relativedelta
from datetime import datetime

class MatchedResultResource(Resource):
    '''
    匹配结果列表的搜索查询
    '''

    def get(self):
        rp = RequestParser()
        rp.add_argument('start')
        rp.add_argument('end')
        rp.add_argument('cur_page')
        rp.add_argument('per_page')

        args = rp.parse_args()

        cur_page = int(args.get('cur_page'))
        per_page = int(args.get('per_page'))
        start = args.get('start')
        end = args.get('end')

        query = Matched_result.query
        if start and end:
            query = query.filter(db.cast(Matched_result.matchDate,db.DATE) >= db.cast(start,db.DATE))\
                    .filter(db.cast(Matched_result.matchDate,db.DATE) <= db.cast(end,db.DATE))

        result_list = query.paginate(cur_page,per_page,error_out=False)

        data = MatchedResultPaginateSerializer(result_list).to_dict()

        return {'msg':'success','data':data}








