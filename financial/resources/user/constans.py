# 开发时间：2024/2/13  20:13
# The road is nothing，the end is all    --Demon

# 短信验证码存放到redis中的时效
SMS_CODE_EXPIRES = 6 * 60

# 根据ip限制验证码频次
LIMIT_SMS_CODE_BY_IP = '10/hour'

# 根据手机号限制验证码频次
LIMIT_SMS_CODE_BY_MOBILE = '1/minute'

# 每次邀请用户成功后则奖励50元的代金券
INVITE_MONEY = 50


