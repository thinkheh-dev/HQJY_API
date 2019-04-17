from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from apiutils.permissions import IsOwnerOrReadOnly, IsServiceProvider

from .models import InfoCategories, WeMediaArticles, WeMediaArticleFav
from .serializers import InfoCategoriesSerializers, WeMediaArticlesSerializers, WeMediaArticleFavDetailSerializers, \
    WeMediaArticleFavSerializers


#分页
class WeMediaArticlesPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


class WeMediaArticlesDetailViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    平台自媒体文章视图
    list:
        平台自媒体文章列表
    retrieve:
        平台自媒体文章详情
    """
    
    serializer_class = WeMediaArticlesSerializers
    pagination_class = WeMediaArticlesPagination
    
    
    def get_queryset(self):
        return WeMediaArticles.objects.all().order_by('id')


class WeMediaArticlesCreateViewSet(mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    """
    平台自媒体文章视图
    list:
        平台自媒体文章列表
    retrieve:
        平台自媒体文章详情
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, IsServiceProvider)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = WeMediaArticlesSerializers
    
    def get_queryset(self):
        return WeMediaArticles.objects.all()


class WeMediaArticlesFavViewSet(viewsets.ModelViewSet):
    """
	用户收藏视图
	list:
		获取用户收藏详情
	create:
		创建用户收藏
	delete:
		删除用户收藏
	"""
    
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = WeMediaArticleFavSerializers
    
    def get_serializer_class(self):
        if self.action == "list":
            return WeMediaArticleFavDetailSerializers
        else:
            return WeMediaArticleFavSerializers
    
    def get_queryset(self):
        return WeMediaArticleFav.objects.filter(user_info=self.request.user)

