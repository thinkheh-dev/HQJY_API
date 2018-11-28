from django.shortcuts import render
from .models import DefaultServices, FinancingServices
from .serializers import DefaultServicesSerializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets

# Create your views here.


class DefaultServicesPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


class DefaultServicesListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    普适服务产品列表接口
    """

    queryset = DefaultServices.objects.all()
    serializer_class = DefaultServicesSerializers
    pagination_class = DefaultServicesPagination
