# 开发时间：2023/9/6  22:06
# The road is nothing，the end is all    --Demon

from flask import Flask
from settings import dict_config
from flask_migrate import Migrate

'''
创建APP的函数，参数代表运行的类型：1. 开发环境  2. 生产环境
'''

def creat_app(run_type):

    app = Flask(__name__)
    # 加载整个项目的配置,__name__表示当前模块的名称
    app.config.from_object(dict_config.get(run_type))

    # 初始化SQLAlchemy
    from comment.models import db
    db.init_app(app)

    # 初始化Redis的数据库连接
    from comment.utils.Flnancial_Redis import fr
    fr.init_app(app)
 
    # 初始化日志处理工具
    from comment.utils.Financial_Logging import create_logger
    create_logger(app)

    # 初始化Migrate，之后就可以直接执行命令了init、migrate、upgrade
    # 执行以上的三个命令，需要默认的Flask项目入口文件（一般名为app.py或wsgi.py的文件即可是）
    # 当前项目没有默认的项目入口文件，需要设置（不设置就会采用默认的）。
    Migrate(app,db)


    return app