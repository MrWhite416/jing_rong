# 开发时间：2023/9/6  22:13
# The road is nothing，the end is all    --Demon

from .default import DevelopmentConfig
from .default import ProductConfig

# 把两个不同环境的配置信息和字符串映射起来
dict_config = {
    'development': DevelopmentConfig,
    'product': ProductConfig
}