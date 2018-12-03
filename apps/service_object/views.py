from django.shortcuts import render
from .models import DefaultServices, FinancingServices
from .serializers import DefaultServicesSerializers, FinancingServicesSerializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend
from .filters import DefaultServicesFilter, FinancingServicesFilter

# Create your views here.


class DefaultServicesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


class DefaultServicesListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    普适服务列表接口
    """

    queryset = DefaultServices.objects.all()
    serializer_class = DefaultServicesSerializers
    pagination_class = DefaultServicesPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = DefaultServicesFilter
    search_fields = ('service_name', 'service_sn', 'service_describe', 'service_detailed_description')
    ordering_fields = ('service_sales', 'service_platform_price')


class FinancingServicesListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    金融服务列表接口
    """

    queryset = FinancingServices.objects.all()
    serializer_class = FinancingServicesSerializers
    pagination_class = DefaultServicesPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = FinancingServicesFilter
    search_fields = ('service_name', 'service_sn', 'service_describe', 'service_detailed_description')
    ordering_fields = ('service_sales', 'service_platform_price')
