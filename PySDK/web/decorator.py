# coding: utf-8
'''
@Author: cA7dEm0n
@Blog: http://www.a-cat.cn
@Since: 2020-01-09 15:51:35
@Motto: 欲目千里，更上一层
@message: Web装饰器
'''

__all__ = ('debugCors')

def debugCors(func):
    def wrapper(*args, **kw):
        resp = func(*args, **kw)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
    return wrapper