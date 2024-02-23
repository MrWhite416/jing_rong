# 开发时间：2024/2/22  19:39
# The road is nothing，the end is all    --Demon

from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json

# 创建蓝图
bp_card = Blueprint('card',__name__,url_prefix='/card')

card_api = Api(bp_card)

card_api.representation('application/json')(output_json)


from financial.resources.card.card_resource import *

card_api.add_resource(Card_Resource, '/card_resource', endpoint='card_resource')



