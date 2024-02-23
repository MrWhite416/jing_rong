# 开发时间：2024/2/22  19:39
# The road is nothing，the end is all    --Demon
from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from comment.models.band_card import BankCard
from comment.models.user import User
from comment.utils.decorators import login_required
from comment.models import db


class Card_Resource(Resource):
    '''
    银行卡管理的资源类
    '''

    method_decorators = [login_required]


    def post(self):
        '''添加银行卡'''

        u_id = g.user_id
        login_user = User.query.filter(User.id == u_id).first()

        rp = RequestParser()
        rp.add_argument('holder', required=True)  # 持卡人
        rp.add_argument('openingBank', required=True)  # 开户银行
        rp.add_argument('bankBranch', required=True)  # 支行
        rp.add_argument('cityId', required=True)  # 城市ID
        rp.add_argument('cardNum', required=True)  # 卡号

        args = rp.parse_args()

        holder = args.holder
        opening_bank = args.openingBank
        bank_branch = args.bankBranch
        city_id = args.cityId
        bank_card_num = args.cardNum

        # 验证银行卡是否唯一
        card_info = BankCard.query.filter(BankCard.bankCardNum == bank_card_num).first()
        if card_info:
            return {'message': '银行卡已存在，请勿重复添加', 'code': 201}

        # 把银行卡数据保存到数据库
        card = BankCard(bankCardNum=bank_card_num, openingBank=opening_bank,
                        bankBranch=bank_branch, cityId=city_id, userId=u_id,
                        reservePhone=login_user.phone)

        db.session.add(card)
        db.session.commit()
        return {'message':'success'}

    def get(self):
        '''
        查询当前登录用户所拥有的银行卡列表
        :return:
        '''

        u_id = g.user_id

        # 查询数据库中，当前用户下所有的银行卡
        card_list = BankCard.query.filter(BankCard.userId == u_id).all()

        from financial.resources.card.serializer import BankCardListSerializer

        if card_list:
            return BankCardListSerializer(card_list).to_dict()
        else:
            return {'message':'None'}
