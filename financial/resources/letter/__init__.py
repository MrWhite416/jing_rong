# 开发时间：2024/2/20  19:56
# The road is nothing，the end is all    --Demon

from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json


# 创建蓝图
letter_bp = Blueprint('letter',__name__,url_prefix='/notify')
letter_api = Api(letter_bp)

letter_api.representation('application/json')(output_json)

from financial.resources.letter.letter_resource import *

letter_api.add_resource(Letter_Res,'/message',endpoint='message')