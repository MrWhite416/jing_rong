# 开发时间：2024/2/13  16:54
# The road is nothing，the end is all    --Demon

import urllib.parse
import urllib.request

def send_code(phone,code):
    #接口地址
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'

    #定义请求的数据
    values = {
        'account':'C46661594',
        'password':'12f42681b4996eeace8d758f0d7f9346',
        'mobile':phone,
        'content':f'您的验证码是：{code}。请不要把验证码泄露给其他人。',
        'format':'json',
    }

    #将数据进行编码
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')

    #发起请求
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    res = response.read()

    return res.decode('utf8')

    #打印结果
    # print(res.decode("utf8"))
