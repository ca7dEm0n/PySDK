from functools import partial
import traceback
try:
    import gevent
    from gevent import monkey as curious_george
    from gevent.pool import Pool
except ImportError:
    raise RuntimeError('Gevent is required for grequests.')

# 初始化修改标准库
curious_george.patch_all(thread=False, select=False)

from requests import Session
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

methods = ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']

__all__ = ['map', 'imap', 'request', 'session'] + methods + ["_{}" for _ in methods]

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

    def send(self, **kwargs):
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


def send(r, pool=None, stream=False):
    """Sends the request object using the specified pool. If a pool isn't
    specified this method blocks. Pools are useful because you can specify size
    and can hence limit concurrency."""
    if pool is not None:
        return pool.spawn(r.send, stream=stream)

    return gevent.spawn(r.send, stream=stream)


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

# synonym
def request(method, url, **kwargs):
    return AsyncRequest(method, url, **kwargs)


# 协程
def map(requests,
        stream=False,
        size=None,
        exception_handler=None,
        gtimeout=None):
    """Concurrently converts a list of Requests to Responses.
    :param requests: a collection of Request objects.
    :param stream: If True, the content will not be downloaded immediately.
    :param size: Specifies the number of requests to make at a time. If None, no throttling occurs.
    :param exception_handler: Callback function, called when exception occured. Params: Request, Exception
    :param gtimeout: Gevent joinall timeout in seconds. (Note: unrelated to requests timeout)
    """

    requests = list(requests)

    pool = Pool(size) if size else None
    jobs = [send(r, pool, stream=stream) for r in requests]
    gevent.joinall(jobs, timeout=gtimeout)

    ret = []

    for request in requests:
        if request.response is not None:
            ret.append(request.response)
        elif exception_handler and hasattr(request, 'exception'):
            ret.append(exception_handler(request, request.exception))
        else:
            ret.append(None)

    return ret


# 线程池迭代模式
def imap(requests, stream=False, size=2, exception_handler=None):
    """Concurrently converts a generator object of Requests to
    a generator of Responses.
    :param requests: a generator of Request objects.
    :param stream: If True, the content will not be downloaded immediately.
    :param size: Specifies the number of requests to make at a time. default is 2
    :param exception_handler: Callback function, called when exception occurred. Params: Request, Exception
    """
    pool = Pool(size)

    def send(r):
        return r.send(stream=stream)

    # 线程迭代
    # imap_unordered 更高效的一种
    for request in pool.imap_unordered(send, requests):
        if request.response is not None:
            yield request.response
        elif exception_handler:
            ex_result = exception_handler(request, request.exception)
            if ex_result is not None:
                yield ex_result

    pool.join()