from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import DefaultServices, FinancingServices, ServiceClassification, FinancingServicesClassification, \
    HotSearchWords, ServiceBrand, DefaultServicesBanner, FinancingServicesBanner, EnterpriseDemand, CorporateFinanceDemand

from .serializers import DefaultServicesSerializers, FinancingServicesSerializers, \
    FinancingServicesClassificationSerializers, FinancingServicesImageSerializers, ServiceBrandSerializers, \
    DefaultServicesPackageSerializers, DefaultCouponTypeSerializers, DefaultServiceCouponSerializers, \
    HotSearchWordsSerializers, DefaultServicesBannerSerializers, FinancingServicesBannerSerializers, \
    EnterpriseDemandSerializers, CorporateFinanceDemandSerializers, ServiceClassificationSerializers, \
    ServiceClassificationNavSerializers, FinancingServicesClassificationNavSerializers

from .filters import DefaultServicesFilter, FinancingServicesFilter, DefaultCategoryFilter, FinancingCategoryFilter


#分页
class DefaultServicesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


class DefaultServicesListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    普适服务列表接口
    
    list:
        普适服务列表
    retrieve:
        普适服务详情
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
    
    list:
        金融服务列表
    retrieve:
        金融服务详情
    """

    queryset = FinancingServices.objects.all()
    serializer_class = FinancingServicesSerializers
    pagination_class = DefaultServicesPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = FinancingServicesFilter
    search_fields = ('service_name', 'service_sn', 'service_describe', 'service_detailed_description')
    ordering_fields = ('service_sales', 'service_platform_price')


class DefaultCategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        普适服务分类列表数据
    retrieve:
        获取普适服务分类详情
    """
    queryset = ServiceClassification.objects.filter(category_type=1)
    serializer_class = ServiceClassificationSerializers

    
class DefaultCategoryNavViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        普适服务分类导航数据 -- 只显示后台确认是导航条目的数据
    """
    queryset = ServiceClassification.objects.filter(is_tab=True)
    serializer_class = ServiceClassificationNavSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = DefaultCategoryFilter
    
    
    
class FinancingCategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        金融服务分类列表数据
    retrieve:
        获取金融服务分类详情
    """
    queryset = FinancingServicesClassification.objects.filter(category_type=1)
    serializer_class = FinancingServicesClassificationSerializers
    

class FinancingCategoryNavViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        金融服务分类导航数据 -- 只显示后台确认是导航条目的数据
    """
    queryset = FinancingServicesClassification.objects.filter(is_tab=True)
    serializer_class = FinancingServicesClassificationNavSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = FinancingCategoryFilter
    

class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-key_index")
    serializer_class = HotSearchWordsSerializers
    
    
class DefaultServicesBannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取普适服务轮播图列表
    """
    queryset = DefaultServicesBanner.objects.all().order_by("index")
    serializer_class = DefaultServicesBannerSerializers
    

class FinancingServicesBannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取金融服务轮播图列表
    """
    queryset = FinancingServicesBanner.objects.all().order_by("index")
    serializer_class = FinancingServicesBannerSerializers
    

class ServicesBrandViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    获取品牌列表、详情
    list:
        品牌列表
    retrieve:
        品牌详情
    """
    queryset = ServiceBrand.objects.all()
    serializer_class = ServiceBrandSerializers
    
class EnterpriseDemandViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """
    企业普适服务需求列表、详情
    list:
        需求列表
    retrieve:
        需求详情
    create:
        创建需求
    """
    queryset = EnterpriseDemand.objects.all()
    serializer_class = EnterpriseDemandSerializers

class CorporateFinanceDemandViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                                    viewsets.GenericViewSet):
    """
    企业金融服务需求列表、详情
    list:
        需求列表
    retrieve:
        需求详情
    create:
        创建需求
    """
    queryset = CorporateFinanceDemand.objects.all()
    serializer_class = CorporateFinanceDemandSerializers
