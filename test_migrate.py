# 开发时间：2024/2/11  21:04
# The road is nothing，the end is all    --Demon

from financial import creat_app
from flask_script import Manager
from comment.models import db
from flask_migrate import Migrate
# 如果导入不了MigrateCommand，是因为flask与flask-migrate的版本冲突问题
# 解决：1. 全面降低版本flask==1.1.2  flask-migrate==2.7.0
#       2. 按照最新版本的的方法执行命令

# 以下是老版本的代码
'''# 初始化app
app = creat_app('develop')

from comment.models.user import User
from comment.models.account import Account
manager = Manager(app)


Migrate(app.db)
manager.add_command('db',Migrate)
'''

# 新版本只需要初始化Migrate即可

