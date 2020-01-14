# coding: utf-8
'''
@Author: cA7dEm0n
@Blog: http://www.a-cat.cn
@Since: 2020-01-07 18:02:28
@Motto: 欲目千里，更上一层
@message: Web Async Http Request
'''
from functools import partial
import traceback
import asyncio

from requests import Session
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

methods = ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']

__all__ = ['map', 'session'] + methods + [ "_{}" for _ in methods ]

defaultRetry = Retry(total=5,
                     backoff_factor=0.2,
                     status_forcelist=[500, 502, 503, 504])

def defaultSession():
    __session = Session()
    adapter = HTTPAdapter(max_retries=defaultRetry)
    __session.mount('https://', adapter)
    __session.mount('https://', adapter)
    return __session

def defaultRequest(method: str, url: str, **kwargs):
    '''
    @description: 普通请求
    '''
    new_kwargs = {}
    default_headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
    }
    headers = kwargs.pop('headers', None)
    if headers:
        default_headers.update(headers)
    new_kwargs['headers'] = default_headers
    kwargs.update(new_kwargs)
    try:
        response = defaultSession().request(method, url, **kwargs)
    except Exception as e:
        return False, e
    return True, response


class AsyncRequest(object):
    def __init__(self, method, url, **kwargs):
        self.method = method
        self.url = url
        self.session = kwargs.pop('session', None)
        if self.session is None:
            self.session = defaultSession()
        callback = kwargs.pop('callback', None)
        if callback:
            kwargs['hooks'] = {'response': callback}
        self.kwargs = kwargs
        self.response = None

    async def send(self, **kwargs):
        '''
        @description: 发起请求
        '''
        # 合并参数
        merged_kwargs = {}
        merged_kwargs.update(self.kwargs)
        merged_kwargs.update(kwargs)
        try:
            self.response = self.session.request(self.method, self.url,
                                                 **merged_kwargs)
        except Exception as e:
            self.exception = e
            self.traceback = traceback.format_exc()
        return self


# Shortcuts for creating AsyncRequest with appropriate HTTP method
get = partial(AsyncRequest, 'GET')
_get = partial(defaultRequest, 'GET')

options = partial(AsyncRequest, 'OPTIONS')
_options = partial(defaultRequest, 'OPTIONS')

head = partial(AsyncRequest, 'HEAD')
_head = partial(defaultRequest, 'HEAD')

post = partial(AsyncRequest, 'POST')
_post = partial(defaultRequest, 'POST')

put = partial(AsyncRequest, 'PUT')
_put = partial(defaultRequest, 'PUT')

patch = partial(AsyncRequest, 'PATCH')
_patch = partial(defaultRequest, 'PATCH')

delete = partial(AsyncRequest, 'DELETE')
_delete = partial(defaultRequest, 'DELETE')

session = defaultSession()

async def gather(loop_list): return await asyncio.gather(*loop_list)


def map(requests, exception_handler=None):
    '''
    @description: Async请求
    @param {list}  requests  请求列表
    @param {exception}  exception_handler  异常处理
    @return: list
    '''
    ret = []
    gather_list = asyncio.run(gather(requests))
    for request in gather_list:
        if request.response is not None:
            ret.append(request.response)
        elif exception_handler and hasattr(request, 'exception'):
            ret.append(exception_handler(request, request.exception))
        else:
            ret.append(None)
    return ret