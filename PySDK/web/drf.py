# coding: utf-8
'''
@Author: cA7dEm0n
@Blog: http://www.a-cat.cn
@Since: 2020-01-02 14:37:10
@Motto: 欲目千里，更上一层
@message: Django rest framework
'''
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

__all__ = ('MyPagination', )


class MyPagination(PageNumberPagination):
    '''
    @description: 自定义分页器
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([('count', self.page.paginator.count),
                         ('results', data)]))
