# 开发时间：2024/3/23  23:39
# The road is nothing，the end is all    --Demon
from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from comment.models.user import User
from comment.models.expected_return import Expected_return
from financial.resources.transaction.serializer import ExpectedReturnPaginateSerializer


class ExpectedReturnResource(Resource):
    """
    查询当前登录用户所有的预期收益列表
    """

    def get(self):
        rp = RequestParser()
        rp.add_argument('cur_page')  # 当前页
        rp.add_argument('per_page')  # 每页数量

        args = rp.parse_args()
        cur_page = int(args.get('cur_page'))
        per_page = int(args.get('per_page'))
        uid = g.user_id
        user = User.query.filter(User.id == uid).first()

        return_list = Expected_return.query.filter(Expected_return.userId == uid)
        return_list = return_list.paginate(cur_page, per_page, error_out=False)

        data = ExpectedReturnPaginateSerializer(return_list).to_dict()

        return {'msg': 'success', 'data': data}
