# 开发时间：2024/3/20  19:16
# The road is nothing，the end is all    --Demon

from flask import g
from flask_restful import Resource
from comment.models.funding_not_matched import Funding_not_matched
from flask_restful.reqparse import RequestParser

from financial.resources.transaction.serializer import AllMatchedPaginateSerializer



class AllMatchedResource(Resource):
    """
    所有待匹配资金列表 和 所有已经匹配资金列表
    """

    def get(self):
        rp = RequestParser()
        rp.add_argument('cur_page')  # 当前页
        rp.add_argument('per_page')  # 每页数据
        rp.add_argument('type')  # 匹配状态，未匹配和部分匹配不用传

        args = rp.parse_args()

        cur_page = int(args.get('cur_page'))
        per_page = int(args.get('per_page'))
        status = args.get('type')

        if not status:
            # 查询所有未匹配和部分匹配的
            matched_lst = Funding_not_matched.query.filter(Funding_not_matched.matchedStatus != 2)
        else:
            matched_lst = Funding_not_matched.query.filter(Funding_not_matched.matchedStatus == 2)

        matched_lst = matched_lst.paginate(cur_page,per_page,error_out=False)
        data = AllMatchedPaginateSerializer(matched_lst).to_dict()

        return {'msg':'success','data':data}







