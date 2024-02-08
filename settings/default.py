# 开发时间：2023/9/6  22:51
# The road is nothing，the end is all    --Demon

# 负责整个项目的配置信息

class Config:
    # 配置数据库和SQLAlchemy
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'msb_finance'
    USERNAME = 'root'
    PASSWORD = 'root'

    DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?/charset=utf8mb4'
    # 数据库的连接URL


    SQLALCHEMY_DATABASE_URL = DB_URL  # 将数据库的连接URL赋值给环境变量
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不需要跟踪数据的修改，此功能一般建议关闭（开启可能会影响性能）
    # 均为环境变量


    # 日志的配置
    LOGGING_LEVEL = 'DEBUG'  # 日志级别
    LOGGING_FILE_DIR = 'logs/'  # 日志文件目录
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024  # 单个日志文件最大存储字节数
    LOGGING_FILE_BACKUP = 100  # 日志文件备份数量


    # 限流器的redis数据库配置
    RATELIMIT_STORAGE_URL = 'redis://192.168.23.3:6379/0'
    # 限流策略：移动窗口：时间窗口会自动变化
    RATELIMIT_STRATEGY = 'moving-window'

    REDIS_URL = 'redis://192.168.23.3:6379/1'


# 开发环境下的配置信息
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 打印SQL


# 生产环境中的配置信息
class ProductConfig(Config):
    pass

