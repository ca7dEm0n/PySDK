from rest_framework.permissions import BasePermission

__all__ = ('AnyUser', )


class AnyUser(BasePermission):
    '''
    @description: 匿名用户权限
    '''
    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        return True