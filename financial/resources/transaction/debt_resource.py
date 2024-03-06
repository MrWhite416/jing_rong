# 开发时间：2024/3/6  23:06
# The road is nothing，the end is all    --Demon

from datetime import datetime, timedelta
from dateutil import relativedelta
from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from financial.resources.transaction.const import LoanConfig
from financial.resources.transaction.serializer import DebtPaginateSerializer
from comment.models import db
from comment.models.debt_info import Debt_info
from comment.models.debt_repay import Debtor_repay
from comment.models.loanApply import Loan
from comment.models.user import User
from comment.utils.decorators import login_required
from comment.utils.generate_trad_id import gen_trad_id, decimal_truncation



class Debt(Resource):

    method_decorators = [login_required]

    def get(self):
        '''
        管理员查询所有的债权列表
        :return:
        '''
        rp = RequestParser()
        rp.add_argument('start')  # 起始时间
        rp.add_argument('end')  # 结束时间
        rp.add_argument('curPage', required=True)  # 当前页码
        rp.add_argument('pageSize', required=True)  # 每页显示数据条数

        args = rp.parse_args()
        start = args.get('start')
        end = args.get('end')
        curPage = args.get('curPage')
        pageSize = args.get('pageSize')

        u_id = g.user_id
        user = User.query.filter(User.id == u_id).first()

        # 得到一个查询对象
        i_query = Debt_info.query

        # 1. 根据起始时间和结束时间过滤
        if start and end:
            # cast，转化数据类型，参1：被转化的字段，参2：转化为什么类型
            i_query = i_query.filter(db.cast(Debt_info.loanStartDate, db.DATE) >= db.cast(start, db.DATE)).filter(
                db.cast(Debt_info.loanStartDate, db.DATE) <= db.cast(end, db.DATE)
            ).paginate(curPage,pageSize)
        else:
            data = i_query.paginate(curPage, pageSize, error_out=False)

        # 分页数据的序列化
        data = DebtPaginateSerializer(data).to_dict()
        return {'msg': 'success', 'data': data}








