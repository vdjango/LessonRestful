'''
来源： https://github.com/vdjango/lhwl_restful/blob/master/api/permissions.py
工具类：
    封装权限类，具体控制个体用户具体权限
'''

from rest_framework import permissions


class IsPublicReadUserSet(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。允许具有管理权限用户修改操作
    """
    SAFE_METHODS = ('GET', 'HEAD', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS')

    permission_all = False  # 用户关联的Models，将展示修改权限
    permission_pubilc_write = True  # 公共读

    def get_methods_permission(self, request, view, obj=None):
        '''
        用于验证 [has_permission, has_object_permission] 方法是否通过
        :param request:
        :param view:
        :param obj:
        :return:
        '''

        if request.user.is_staff:
            return True

        if view.kwargs:

            '''
            用户关联的Models，将展示修改权限
            '''
            # if view.user_key and self.cache_object.serializable_value(view.user_key) == request.user.id:
            #     self.permission_all = True
            #     pass
            if self.permission_all:
                if request.method not in self.SAFE_METHODS:
                    return False
            else:
                # 其他用户，只读权限
                if request.method not in permissions.SAFE_METHODS:
                    return False
                pass
            pass
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            return view.permission_pubilc_write

        return True

    def has_object_permission(self, request, view, obj):
        '''
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        对任何请求都允许读取权限
        所以我们总是允许获得，头部或选项请求
        :param request:
        :param view:
        :param obj:
        :return:
        '''

        if not request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False

        return self.get_methods_permission(request, view, obj)

    def has_permission(self, request, view):
        '''
        Api view access
        Unregistered users do not have permission to modify the API interface.
        GET HEAD PATCH PUT POST DELETE OPTIONS
        API视图访问
        未注册用户没有修改API接口的权限。
        GET HEAD PATCH PUT POST DELETE OPTIONS
        :param request:
        :param view:
        :return:
        '''
        # print('has_permission', request.user)

        if not request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False

        return self.get_methods_permission(request, view)


class IsAdminOrPublicReadOnlyAndUserInterface(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    SAFE_METHODS = ('GET', 'HEAD', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS')
    permission_safe = True  # True根据SAFE_METHODS方法实现 False不可写

    def get_methods_permission(self, request, view, obj=None):
        '''
        接口权限开关
        验证当前接口是否关联于用户
        '''

        try:
            self.permission_safe = view.permission_safe
        except AttributeError:
            pass
        try:
            self.SAFE_METHODS = view.SAFE_METHODS
        except AttributeError:
            pass

        if request.user.is_staff:
            return True

        if self.permission_safe:
            if not (request.method in self.SAFE_METHODS):
                return False

        return self.permission_safe

    def has_object_permission(self, request, view, obj):
        '''
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        对任何请求都允许读取权限
        所以我们总是允许获得，头部或选项请求
        :param request:
        :param view:
        :param obj:
        :return:
        '''

        # if not request.user.is_authenticated:
        #
        #     if request.method in permissions.SAFE_METHODS:
        #         return True
        #     return False

        return self.get_methods_permission(request, view, obj)

    def has_permission(self, request, view):
        '''
        Api view access
        Unregistered users do not have permission to modify the API interface.
        GET HEAD PATCH PUT POST DELETE OPTIONS
        API视图访问
        未注册用户没有修改API接口的权限。
        GET HEAD PATCH PUT POST DELETE OPTIONS
        :param request:
        :param view:
        :return:
        '''
        # print('has_permission', request.user)

        # if not request.user.is_authenticated:
        #     if request.method in permissions.SAFE_METHODS:
        #         return True
        #     return False

        return self.get_methods_permission(request, view)


class IsPrivateWriteUserInterface(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    SAFE_METHODS = ('GET', 'HEAD', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS')

    permission_all = False
    permission_pubilc_write = True  # 公共读

    cache_object = None

    def get_methods_permission(self, request, view, obj=None):
        '''
        用于验证 [has_permission, has_object_permission] 方法是否通过
        :param request:
        :param view:
        :param obj:
        :return:
        '''

        if request.user.is_staff:
            return True

        print('开始', view.kwargs)

        if view.kwargs:

            '''detail'''
            if not self.cache_object:
                if obj:
                    self.cache_object = obj
                else:
                    self.cache_object = view.get_object()
                pass

            if view.user_key and self.cache_object.serializable_value(view.user_key) == request.user.id:
                self.permission_all = True
                print('用户操作自己的数据')
                pass

            if self.permission_all:
                print('用户操作自己的数据')
                # 用户关联的Models，将展示修改权限
                if request.method not in self.SAFE_METHODS:
                    return False
            else:
                print('其他用户的数据')
                # 其他用户，只读权限
                if request.method not in permissions.SAFE_METHODS:
                    return False
                pass
            pass
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            return view.permission_pubilc_write

        # print('开始')
        return True

    def has_object_permission(self, request, view, obj):
        '''
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        对任何请求都允许读取权限
        所以我们总是允许获得，头部或选项请求
        :param request:
        :param view:
        :param obj:
        :return:
        '''

        if not request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            print('开始 未登录 objtects')
            return False

        return self.get_methods_permission(request, view, obj)

    def has_permission(self, request, view):
        '''
        Api view access
        Unregistered users do not have permission to modify the API interface.
        GET HEAD PATCH PUT POST DELETE OPTIONS
        API视图访问
        未注册用户没有修改API接口的权限。
        GET HEAD PATCH PUT POST DELETE OPTIONS
        :param request:
        :param view:
        :return:
        '''
        # print('has_permission', request.user)

        if not request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            print('开始 未登录 permission')
            return True

        return self.get_methods_permission(request, view)

    pass


class IsPublicUserInterface(permissions.BasePermission):
    """
    公共访问权限，允许所以请求
    """
    SAFE_METHODS = ('GET', 'HEAD', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS')

    permission_all = False
    permission_pubilc_write = True  # 公共读

    cache_object = None

    def get_methods_permission(self, request, view, obj=None):
        '''
        接口权限开关
        验证当前接口是否关联于用户
        '''

        try:
            self.permission_pubilc_write = view.permission_pubilc_write
        except AttributeError:
            pass

        if self.permission_pubilc_write:
            if request.method in permissions.SAFE_METHODS:
                return True

        return self.permission_pubilc_write

    def has_object_permission(self, request, view, obj):
        '''
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        对任何请求都允许读取权限
        所以我们总是允许获得，头部或选项请求
        :param request:
        :param view:
        :param obj:
        :return:
        '''

        return self.get_methods_permission(request, view, obj)

    def has_permission(self, request, view):
        '''
        Api view access
        Unregistered users do not have permission to modify the API interface.
        GET HEAD PATCH PUT POST DELETE OPTIONS
        API视图访问
        未注册用户没有修改API接口的权限。
        GET HEAD PATCH PUT POST DELETE OPTIONS
        '''

        return self.get_methods_permission(request, view)


class IsPublicNoModifyUserInterface(permissions.BasePermission):
    """
    接口访问权限，不允许修改删除
    """
    SAFE_METHODS = ('GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE')
    permission_safe = True  # True根据SAFE_METHODS方法实现 False不可写

    def get_methods_permission(self, request, view, obj=None):
        '''
        接口权限开关
        验证当前接口是否关联于用户
        '''

        try:
            self.permission_safe = view.permission_safe
        except AttributeError:
            pass
        try:
            self.SAFE_METHODS = view.SAFE_METHODS
        except AttributeError:
            pass

        if request.user and request.user.is_authenticated:
            return True

        if self.permission_safe:
            if not (request.method in self.SAFE_METHODS):
                return False

        return self.permission_safe

    def has_object_permission(self, request, view, obj):
        '''
        Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        对任何请求都允许读取权限
        所以我们总是允许获得，头部或选项请求
        :param request:
        :param view:
        :param obj:
        :return:
        '''

        return self.get_methods_permission(request, view, obj)

    def has_permission(self, request, view):
        '''
        Api view access
        Unregistered users do not have permission to modify the API interface.
        GET HEAD PATCH PUT POST DELETE OPTIONS
        API视图访问
        未注册用户没有修改API接口的权限。
        GET HEAD PATCH PUT POST DELETE OPTIONS
        '''

        return self.get_methods_permission(request, view)


class IsAuthenticationOrPublicReadOnlyInterface(permissions.BasePermission):
    """
    匿名用户只能获取查看请求，认证用户只能获取SAFE_METHODS指定的权限，管理员获取所有权限
    """
    SAFE_METHODS = ('GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE')
    permission_safe = True  # True根据SAFE_METHODS方法实现 False不可写

    def get_methods_permission(self, request, view, obj=None):

        try:
            self.permission_safe = view.permission_safe
        except AttributeError:
            pass
        try:
            self.SAFE_METHODS = view.SAFE_METHODS
        except AttributeError:
            pass

        if request.user.is_staff:
            return True

        if request.user and request.user.is_authenticated:
            if request.method in self.SAFE_METHODS:
                return True
            else:
                return False

        if self.permission_safe:
            if not (request.method in ['GET', 'HEAD', 'OPTIONS']):
                return False

        return self.permission_safe

    def has_object_permission(self, request, view, obj):

        return self.get_methods_permission(request, view, obj)

    def has_permission(self, request, view):

        return self.get_methods_permission(request, view)
