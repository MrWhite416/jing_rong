# 开发时间：2023/9/9  20:24
# The road is nothing，the end is all    --Demon

import logging
import logging.handlers
from flask import request
import os

'''
定义了日志的格式
'''

class RequestShoppingFormatter(logging.Formatter):  # logging主要用于输出运行日志，formatter决定日志记录格式
    """
    自定义的日志输出格式
    """

    def format(self, record):
        record.url = request.url  # 需要在日志中记录请求地址
        record.remote_addr = request.remote_addr  # 需要在日志中记录客户端的地址
        return super().format(record)

# 创建一个个性化的logger对象
def create_logger(app):
    """
    设置日志配置
    :param app: Flask中的app对象
    :return:
    """
    logging_file_dir = app.config['LOGING_FILE_DIR']  # 日志文件所在的目录
    logging_file_max_bytes = app.config['LOGING_FILE_MAX_BYTES']  # 日志文件最大的大小
    logging_file_backup = app.config['LOGING_FILE_BACKUP']  # 保留备份的日志文件个数
    logging_level = app.config['LOGING_LEVEL']  # 默认的日志级别

    # 设置日志的输出格式（针对文件）
    request_formatter = RequestShoppingFormatter(
        '[%(asctime)s] %(remote_addr)s  请求 %(url)s \t %(levelname)s 在 %(module)s %(lineno)d : %(message)s'
    )

    # 检查如果目录不存在，则创建目录
    if os.path.isdir(logging_file_dir):
        pass
    else:
        os.mkdir(logging_file_dir)  # 如果目录不存在，则创建

    # 自定义一个目录和日志文件，RotatingFileHandler：按照指定文件的大小来规定日志文件的生成规则
    # flask_file_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(logging_file_dir, 'shopping.log'),
    #                                      maxBytes=logging_file_max_bytes,
    #                                      backupCount=logging_file_backup)

    # 为了让一个进程操作一个文件，所以文件命名时加上当前进程ID
    # TimedRotatingFileHandler：根据时间来规定日志文件的生成规则
    flask_file_handler = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(logging_file_dir, 'financial'+str(os.getpid())+'.log'),
                                                              when='D', interval=1,  # when--时间单位（D是天），interval--具体的时间数（此处为1天）
                                                              backupCount=logging_file_backup)

    # 给当前的handler设置格式
    flask_file_handler.setFormatter(request_formatter)
    # 得到一个logger对象，根据包的名字，如果存在则获取到该logger对象，如果不存在则根据名称创建一个logger对象
    # 所有核心的业务逻辑（资源接口）都在financial中，所以日志的生成也是因为它，所以使用该包名
    flask_logger = logging.getLogger('financial')
    flask_logger.addHandler(flask_file_handler)
    flask_logger.setLevel(logging_level)

    # 整个项目需要两个handler：文件，控制台
    # StreamHandler是将日志输出到控制台上
    flask_console_handler = logging.StreamHandler()
    flask_console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(module)s %(lineno)d : %('
                                                         'message)s'))


