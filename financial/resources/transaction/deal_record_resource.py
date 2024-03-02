# 开发时间：2024/2/26  20:04
# The road is nothing，the end is all    --Demon

from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from comment.models.user import User
from comment.models.deal_record import DealRecord
from comment.models import db
from financial.resources.transaction.serializer import DealRecordPaginateSerializer


class DealResource(Resource):
    '''
    交易记录的资源类
    '''

    def get(self):
        '''
        交易记录的列表
        :return:
        '''

        rp = RequestParser()
        rp.add_argument('start')  # 起始时间
        rp.add_argument('end')  # 结束时间
        rp.add_argument('dealType')  # 投资类型，初始值为0，表示‘购买中的计划’
        rp.add_argument('curPage',required=True)  # 当前页码
        rp.add_argument('pageSize',required=True)  # 每页显示数据条数

        args = rp.parse_args()
        start = args.get('start')
        end = args.get('end')
        dealType = 0 if args.get('dealType')==None else int(args.get('investType'))
        curPage = args.get('curPage')
        pageSize = args.get('pageSize')

        u_id = g.user_id
        user = User.query.filter(User.id == u_id).first()

        # 当过滤逻辑较复杂时，建议分开写
        # 得到一个查询对象
        i_query = DealRecord.query
        # 开始过滤:1. 根据用户ID过滤
        if user.role == 0:  # 0为普通用户，1为管理员
            i_query = i_query.filter(DealRecord.aUserId == u_id)
        # 2. 根据交易类型过滤
        if dealType>0:  # dealType为0时是全部，在交易记录中交易类型名称不可能为‘全部’
            i_query = i_query.filter(DealRecord.aType == dealType)
        # 3. 根据起始时间和结束时间过滤
        if start and end:
            # cast，转化数据类型，参1：被转化的字段，参2：转化为什么类型
            i_query = i_query.filter(db.cast(DealRecord.aDate,db.DATE) >= db.cast(start,db.DATE)).filter(
                            db.cast(DealRecord.aDate, db.DATE) <= db.cast(end, db.DATE)
            )
        data = i_query.paginate(curPage,pageSize,error_out=False)

        data = DealRecordPaginateSerializer(data).to_dict()
        return {'msg':'success','data':data}



