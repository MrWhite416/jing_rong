# 开发时间：2023/9/6  22:11
# The road is nothing，the end is all    --Demon

# 马士兵金融项目入口
from financial import creat_app


app = creat_app('development')

if __name__ == '__main__':
    app.run()