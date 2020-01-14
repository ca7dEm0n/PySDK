# coding: utf-8
'''
@Author: cA7dEm0n
@Blog: http://www.a-cat.cn
@Since: 2020-01-03 10:15:40
@Motto: 欲目千里，更上一层
@message: 认证鉴权
'''
from django.conf import settings
SECRET_KEY = settings.SECRET_KEY

from pysdk.ops.encrypt import jwtDecode
from pysdk.ops.utils import dict2Obj

from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)

__all__ = ('JwtAuthentication', )


def jwt_decode_handler(token):
    return jwtDecode(token, SECRET_KEY)


class JwtAuthentication(BaseAuthentication):
    '''
    @description: JWT认证
    '''
    JWT_AUTH_HEADER_PREFIX = "JWT"
    JWT_AUTH_COOKIE = "auth"

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        payload = jwt_decode_handler(jwt_value)
        _ok, payload = jwt_decode_handler(jwt_value)
        if not _ok:
            raise exceptions.AuthenticationFailed(payload)
        user = dict2Obj(payload, "User")
        return (user, jwt_value)

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = self.JWT_AUTH_HEADER_PREFIX.lower()
        if not auth:
            return request.COOKIES.get(self.JWT_AUTH_COOKIE)
        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        return auth[1]