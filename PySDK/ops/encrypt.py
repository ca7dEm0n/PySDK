# coding: utf-8
'''
@Author: cA7dEm0n
@Blog: http://www.a-cat.cn
@Since: 2019-12-31 13:48:59
@Motto: 欲目千里，更上一层
@message: 加解密
'''
import jwt
from datetime import timedelta
from itsdangerous import URLSafeSerializer, TimestampSigner

__all__ = ('jwtDecode', 'itsEncode', 'itsDecode')

# 默认加密key
DEFAULT_SAFE_KEY = "default"


def itsEncode(data: str,
              url_safe_key: str = DEFAULT_SAFE_KEY,
              time_safe_key: str = DEFAULT_SAFE_KEY) -> TimestampSigner.sign:
    '''
    @description: its加密
    @param {data} data 加密数据 
    @param {str}  url_safe_key URL加密密钥
    @param {str}  time_safe_key Time加密密钥
    @return: Data
    '''
    uSafe = URLSafeSerializer(url_safe_key)
    dumpUsafe = uSafe.dumps(data)
    tSafe = TimestampSigner(time_safe_key)
    signTsafe = tSafe.sign(dumpUsafe)
    return signTsafe


def itsDecode(data:str,
              time:int=15,
              url_safe_key:str=DEFAULT_SAFE_KEY,
              time_safe_key:str=DEFAULT_SAFE_KEY) -> (bool, str):
    '''
    @description: its解密
    @param {data} data 加密数据 
    @param {int}  time 过期时间
    @param {str}  url_safe_key URL加密密钥
    @param {str}  time_safe_key Time加密密钥
    @return: True/False, Data
    '''
    result = None
    time = int(time)
    try:
        tSafe = TimestampSigner(time_safe_key)
        tUnsign = tSafe.unsign(data, time)
    except:
        return False, "授权过期"
    try:
        uSafe = URLSafeSerializer(url_safe_key)
        result = uSafe.loads(url_safe_key)
        return True, result
    except:
        return False, "解析失败"


def jwtDecode(auth_token:str,
              secret_key:str,
              algorithms:list=['HS256'],
              leeway:timedelta=timedelta(hours=8)) -> (bool, str):
    '''
    @description: JWT解密
    @param {string}     auth_token     加密的TOKEN
    @param {string}     secret_key     解密的KEY
    @param {list}       algorithms     解密的算法，默认为:HS256
    @param {timedelta}  leeway         超时时间，默认8小时
    @return: True/False, Data/ErrorMessage
    '''
    try:
        payload = jwt.decode(auth_token,
                             secret_key,
                             algorithms=algorithms,
                             leeway=leeway)
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, 'Token过期'
    except jwt.InvalidTokenError:
        return False, '无效Token'