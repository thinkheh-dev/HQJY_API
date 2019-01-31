from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import EnterpriseType, EnterpriseTypeLevel, BasicEnterpriseInfo
from .serializers import EnterpriseTypeSerializers, BasicEnterpriseInfoSerializers


#分页
class EnterpriseInfoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100
    

class EnterpriseTypeListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	企业分类列表接口
	
	list:
		企业分类列表
	retrieve:
		企业分类详情
	"""
	
	queryset = EnterpriseType.objects.all()
	serializer_class = EnterpriseTypeSerializers


class EnterpriseListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	企业列表接口
	
	list:
		企业列表
	retrieve:
		企业详情
	"""
	
	queryset = BasicEnterpriseInfo.objects.all()
	serializer_class = BasicEnterpriseInfoSerializers
	pagination_class = EnterpriseInfoPagination
	search_fields = ('name', 'credit_no', 'oper_name', 'oper_phone', 'company_area')
	ordering_fields = ('name', 'company_area')
