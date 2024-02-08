# 开发时间：2023/9/6  22:06
# The road is nothing，the end is all    --Demon

from flask import Flask
from settings import dict_config

'''
创建APP的函数，参数代表运行的类型：1. 开发环境  2. 生产环境
'''

def creat_app(run_type):

    app = Flask(__name__)
    # 加载整个项目的配置,__name__表示当前模块的名称
    app.config.from_object(dict_config.get(run_type))

    # 初始化SQLAlchemy
    from comment.modules import db
    db.init_app(app)

    # 初始化Redis的数据库连接
    from comment.utils.Flnancial_Redis import fr
    fr.init_app(app)

    return app;