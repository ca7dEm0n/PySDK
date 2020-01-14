# coding: utf-8
'''
@Author: cA7dEm0n
@Blog: http://www.a-cat.cn
@Since: 2019-12-31 15:56:25
@Motto: 欲目千里，更上一层
@message: 工具集
'''
import string
import random
from redis import ConnectionPool, StrictRedis
from types import FunctionType

__all__ = ('sRedis', 'genPassword', 'dict2Obj', 'filterDict')


def genPassword(length: int = 8,
                chars=string.digits + string.ascii_letters) -> str:
    '''
    @description: 生成随机密码
    @param {int}  length  密码长度，默认为8
    @return: string
    '''
    return ''.join(random.sample(chars * 10, length))

def filterDict(dictObj:dict, callback:FunctionType) -> dict:
    '''
    @description: 字典过滤
    '''    
    newDict = dict()
    for (key, value) in dictObj.items():
        if callback((key, value)):
            newDict[key] = value
    return newDict


def sRedis(db: int = 0,
           host: str = "127.0.0.1",
           port: int = 6379) -> StrictRedis:
    '''
    @description: 连接Redis
    @param {int}        db     库，默认为0 
    @param {string}     host   主机，默认为127.0.0.1
    @param {int}        port   端口，默认为6379
    @return: StrictRedis
    '''
    pool = ConnectionPool(host=host, port=port, db=db, max_connections=10)
    return StrictRedis(connection_pool=pool)


def dict2Obj(data: dict, class_name: str = "new") -> object:
    '''
    @description: 字典转对象
    '''
    _new = type(class_name, (object, ), data)
    seqs = tuple, list, set, frozenset
    for _k, _v in data.items():
        if isinstance(_v, dict):
            setattr(_new, _k, dict2Obj(_v))
        elif isinstance(_v, seqs):
            setattr(
                _new, _k,
                type(_v)(dict2Obj(ik) if isinstance(ik, dict) else ik
                         for ik in _v))
        else:
            setattr(_new, _k, _v)
    return _new
