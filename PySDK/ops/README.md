
# 方法使用说明
---

## 模块说明

- encrypt	    加解密
- gRequests     请求

### utils
---

- utils.sRedis

> Reids操作

- utils.genPassword

> 生成随机密码


### encrypt
---

- encrypt.jwtDecode

> JWT解密

示例
```python
from pysdk.ops.encrypt import jwtDecode
print (jwtDecode(token, secret_key))

# (True, {'user_id': 14, 'username': 'admin', 'exp': 1577725478, 'email': 'a-ca7@139.com', 'uid': '10623', 'orig_iat': 1577696678})
```

### gRequests
---

**单次请求**

- gRequests.`_<methods>`

> 普通请求
> 传参与`requests`模块一致

示例
```python
import pysdk.ops.gRequests
testB = gRequests._get("http://www.baidu.com")
status, response = testB
print (status, response)
# True <Response [200]>
```


- gRequests.`<methods>`

> 协程请求
> 传参与`requests`模块一致

示例
```python
import pysdk.ops.gRequests
testA    = gRequests.get("http://www.baidu.com", callback=back)
response = testA.send()
print (response.response)

# <Response [200]>
```

**批量请求**

- gRequests.map

> 批量请求
> 传入请求列表

示例
```python
def exception_handler(request, exception):
    print "Request failed"

reqs = [
    gRequests.get('http://httpbin.org/delay/1', timeout=0.001),
    gRequests.get('http://fakedomain/'),
    gRequests.get('http://httpbin.org/status/500')]
gRequests.map(reqs, exception_handler=exception_handler)
# Request failed
# Request failed
# [None, None, <Response [500]>]
```

- gRequests.imap

> 批量请求 - 以迭代生成器模式


示例
```python
getList = [
    gRequests.get("http://baidu.com"),
    gRequests.get("http://a-cat.com")
]
responses = gRequests.imap(getList)
for _ in responses:
    print (_)

# <Response [200]>
# <Response [200]>
```



