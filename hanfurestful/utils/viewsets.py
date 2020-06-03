"""
来源： https://github.com/vdjango/lhwl_restful/blob/master/api/util/ModelViewUtil.py
工具类：
    封装视图方法，集合权限，分页
"""

from collections import OrderedDict

from django.http import HttpResponse
from django_pdfkit import PDFView
from rest_framework import viewsets, pagination, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import timezone
from .JsonRender import Utf8JSONRenderer
from .LimitOffsetPagination import Pagination
from .permissions import IsAdminOrPublicReadOnlyAndUserInterface, IsPrivateWriteUserInterface


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    """
    自定义分页方法
    """
    page_size_query_param = "page_size"
    page_query_param = 'page'
    page_size = 60
    default_limit = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    pass


class ModelViewSet(viewsets.ModelViewSet):  # RetrieveCacheResponseMixin
    '''
    :param user_key: 模型用户外键 数据模型所关联的用户，所属用户
    :param permission_pubilc_write: 接口公共写入状态[True/False]
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。
        IsAuthenticated: 需要身份令牌验证
    :param pagination_class: 接口分页
    :param code: 接口内部返回值[未实现]
    '''
    # permission_pubilc_write = True
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAdminOrPublicReadOnlyAndUserInterface,)  # IsAuthenticated
    pagination_class = Pagination
    renderer_classes = (Utf8JSONRenderer, BrowsableAPIRenderer)
    user_key = 'key'
    code = 200

    serializer_list_class = None

    def get_serializer_class_list(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_list_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_list_class

    def get_serializer_list(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class_list()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # @cache_response(key_func='list_cache_key_func')
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        no_page = self.request.query_params.get('no_page', None)

        if no_page:
            """
            该字段用来判断是否经过分页处理
            """
            serializers = self.get_serializer_list(queryset, many=True)
            return Response(serializers.data)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializers = self.get_serializer_list(page, many=True)
                return self.get_paginated_response(serializers.data)

            serializers = self.get_serializer_list(queryset, many=True)
            return Response(serializers.data)

    '''
    @ensure_csrf_cookie 
    Django官方解释 对于完全的前后分离，是拿不到csrf的。 通过这种方式将csrf设置cookie里面
    '''

    def dispatch(self, request, *args, **kwargs):
        if not self.serializer_list_class:
            self.serializer_list_class = self.serializer_class

        # if self.permission_pubilc_write:
        #     self.permission_classes = (IsAdminOrPublicReadOnlyAndUserInterface,)
        # else:
        #     self.permission_classes = (IsAuthenticated,)
        #     pass

        # get_token(request)

        return super(ModelViewSet, self).dispatch(request, *args, **kwargs)


class MethodPubilcViewSet(viewsets.ModelViewSet):
    '''
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。
        IsAuthenticated: 需要身份令牌验证
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAdminOrPublicReadOnlyAndUserInterface, IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        return super(MethodPubilcViewSet, self).dispatch(request, *args, **kwargs)


class MethodPrivateViewSet(viewsets.ModelViewSet):
    '''
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。
        IsAuthenticated: 需要身份令牌验证
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        return super(MethodPrivateViewSet, self).dispatch(request, *args, **kwargs)


class ModelPrivateWriteViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsPrivateWriteUserInterface,)

    pass


class ObjectViewSet(ViewSet):
    '''
    不具备query
    '''
    serializer_class = None

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    pass


class PDFViewSet(PDFView):
    pdfkit_options = {
        'page-size': 'Letter',
        'margin-top': '0.2in',
        'margin-right': '0.0in',
        'margin-bottom': '0.2in',
        'margin-left': '0.0in',
        'encoding': "UTF-8",
        'print-media-type': False,
    }
    filename = '{name}.pdf'
    title = None

    def get_options_filename(self, **kwargs):
        if self.title:
            self.pdfkit_options.update({
                'title': self.title
            })

    def get_context_data(self, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        context = {
            **serializer.data,
            **kwargs
        }
        return context

    def get(self, request, *args, **kwargs):
        """
        下载。/?download
        HTML预 /?html
        PDF预 /

        Return a HTTPResponse either of a PDF file or HTML.

        :rtype: HttpResponse
        """
        self.get_options_filename()
        if 'html' in request.GET:
            # Output HTML
            content = self.render_html(*args, **kwargs)
            return HttpResponse(content)

        else:
            # Output PDF
            content = self.render_pdf(*args, **kwargs)

            response = HttpResponse(content, content_type='application/pdf')

            if (not self.inline or 'download' in request.GET) and 'inline' not in request.GET:
                response['Content-Disposition'] = 'attachment; filename="%s"' % self.get_filename().format(
                    name='{}'.format(str(timezone.now()).split('.')[0])
                )

            response['Content-Length'] = len(content)

            return response

    pass
