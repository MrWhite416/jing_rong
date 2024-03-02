# 开发时间：2024/2/25  15:05
# The road is nothing，the end is all    --Demon

from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from comment.utils.decorators import login_required
from comment.models.product import Product
from comment.models.product_rate import Product_rate
from comment.models.invest_record import Invest_record
from comment.models import db
from financial.resources.transaction.serializer import InvestRecordPaginateSerializer


class InvestResource(Resource):
    '''
    投资记录的资源类
    '''

    def get(self):
        '''
        投资记录的列表
        :return:
        '''

        rp = RequestParser()
        rp.add_argument('start')  # 起始时间
        rp.add_argument('end')  # 结束时间
        rp.add_argument('investType')  # 投资类型，初始值为0，表示‘购买中的计划’
        rp.add_argument('curPage',required=True)  # 当前页码
        rp.add_argument('pageSize',required=True)  # 每页显示数据条数

        args = rp.parse_args()
        start = args.get('start')
        end = args.get('end')
        investType = 0 if args.get('investType')==None else int(args.get('investType'))
        curPage = args.get('curPage')
        pageSize = args.get('pageSize')

        u_id = g.user_id

        # 当过滤逻辑较复杂时，建议分开写
        # 得到一个查询对象
        i_query = Invest_record.query
        # 开始过滤:1. 根据用户ID过滤
        i_query = i_query.filter(Invest_record.pUid == u_id)
        # 2. 根据投资类型过滤
        i_query = i_query.filter(Invest_record.pStatus == investType)
        # 3. 根据起始时间和结束时间过滤
        if start and end:
            # cast，转化数据类型，参1：被转化的字段，参2：转化为什么类型
            i_query = i_query.filter(db.cast(Invest_record.pDate,db.DATE) <= db.cast(start,db.DATE)).filter(
                            db.cast(Invest_record.pDate, db.DATE) >= db.cast(end, db.DATE)
            )
        data = i_query.paginate(curPage,pageSize,error_out=False)

        data = InvestRecordPaginateSerializer(data).to_dict()
        return {'msg':'success','data':data}






