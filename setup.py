# coding: utf-8
'''
@Author: cA7dEm0n
@Blog: http://www.a-cat.cn
@Since: 2019-12-30 18:24:31
@Motto: 欲目千里，更上一层
'''

from setuptools import find_packages, setup

setup(name='PySDK',
      version='0.0.10',
      packages=find_packages(exclude=['*.test', '*.test.*']),
      url='http://www.a-cat.cn/',
      license='BSD',
      install_requires=['requests', 'pyjwt', 'redis', 'gevent', 'itsdangerous'],
      author='cA7dEm0n',
      author_email='a-ca7@139.com',
      description='SDK of the operation and maintenance script')
