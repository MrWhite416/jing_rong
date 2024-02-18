# 开发时间：2024/2/15  14:48
# The road is nothing，the end is all    --Demon
import os

SECRET_KEY = os.urandom(16)  # 生成随机一个字符串作为秘钥

JWT_EXPIRY_SECOND = 60*60  # token有效时间，单位是秒