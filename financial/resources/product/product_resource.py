# 开发时间：2024/2/23  15:44
# The road is nothing，the end is all    --Demon

from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from comment.utils.decorators import login_required
from comment.models.product import Product
from comment.models.product_rate import Product_rate
from comment.models import db
from financial.resources.product.serializer import ProductListSerializer,ProductRateListSerializer



class InvestProduct(Resource):
    '''
    理财产品的资源类
    '''

    def get(self):
        '''
        返回所有的理财产品列表
        :return:
        '''
        product_list = Product.query.all()
        data = ProductListSerializer(product_list).to_dict()

        return {'msg':'success','data':data}







