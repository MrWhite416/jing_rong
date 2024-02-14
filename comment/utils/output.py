# 开发时间：2024/2/12  21:14
# The road is nothing，the end is all    --Demon
from flask import make_response, current_app
from flask_restful.utils import PY3
from json import dumps


def output_json(data, code, headers=None):


    """Makes a Flask response with a JSON encoded body"""
    # 此处为自己添加***************
    # 目的：对返回给前端的数据做一个统一的封装，
    # 便于前端可以使用统一的规则来得到数据
    if 'message' not in data:
        data = {
            # 'message': 'OK',
            'data': data,
            'code':20000  # 自动把状态20000封装到json中
        }
    # **************************
    settings = current_app.config.get('RESTFUL_JSON', {})
    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here. Note that this won't override any existing value
    # that was set. We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
    settings.setdefault('sort_keys', not PY3)
    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"  # 把字典转为json
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp