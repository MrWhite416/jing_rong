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


class ProductRate(Resource):
    '''
    产品利率的资源类
    '''


    def get(self):
        '''
        返回一个产品的利率列表
        :return:
        '''
        rp = RequestParser()
        rp.add_argument('proID',required=True)

        args = rp.parse_args()
        p_ID = args.get('proID')
        rate_list = Product_rate.query.filter(Product_rate.productId == p_ID).all()

        data = ProductRateListSerializer(rate_list).to_dict()
        return {'msg':'success','data':data}






