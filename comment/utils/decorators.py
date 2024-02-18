# 开发时间：2024/2/17  21:28
# The road is nothing，the end is all    --Demon
from flask import g
'''
自定义一个装饰器，判断用户是否登录。如果登录了就继续访问，否则直接返回（不再访问）
'''

def login_required(func):
    def wrapper(*args,**kwargs):
        if g.user_id is not None:
            return func(*args,**kwargs)
        else:
            return {'message':'用户未登录，拒绝访问'},401
    return wrapper


