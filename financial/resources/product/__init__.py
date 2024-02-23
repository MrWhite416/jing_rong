# 开发时间：2024/2/23  15:26
# The road is nothing，the end is all    --Demon

from flask import Blueprint
from flask_restful import Api
from comment.utils.output import output_json



# 创建蓝图
bp_product = Blueprint('product',__name__,'/product')
product_api = Api(bp_product)

# 使用我们自定义的json格式，替代装饰器的写法
product_api.representation('application/json')(output_json)

from financial.resources.product.product_resource import *





