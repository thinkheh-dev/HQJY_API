#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2018-12-03 15:31
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : filter.py
# @software: PyCharm
import django_filters
from .models import DefaultServices, FinancingServices, ServiceClassification, FinancingServicesClassification


class DefaultServicesFilter(django_filters.rest_framework.FilterSet):
	"""
	普适服务过滤类
	"""
	price_min = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最低价格', lookup_expr='gte')
	price_max = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最高价格', lookup_expr='lte')
	service_class1 = django_filters.CharFilter(field_name="service_classification1", lookup_expr='exact')
	service_class2 = django_filters.CharFilter(field_name="service_classification2", lookup_expr='exact')
	service_class3 = django_filters.CharFilter(field_name="service_classification3", lookup_expr='exact')
	service_class4 = django_filters.CharFilter(field_name="service_classification4", lookup_expr='exact')
	service_class5 = django_filters.CharFilter(field_name="service_classification5", lookup_expr='exact')
	is_hot = django_filters.BooleanFilter(field_name='is_hot', lookup_expr='exact')
	
	class Meta:
		model = DefaultServices
		fields = ['price_min', 'price_max', 'service_class1', 'service_class2', 'service_class3', 'service_class4',
		          'service_class5', 'is_hot']


class FinancingServicesFilter(django_filters.rest_framework.FilterSet):
	"""
	金融服务过滤类
	"""
	price_min = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最低价格', lookup_expr='gte')
	price_max = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最高价格', lookup_expr='lte')
	financing_service_classification1 = django_filters.CharFilter(field_name="financing_service_classification1",
	                                                              lookup_expr='exact')
	financing_service_classification2 = django_filters.CharFilter(field_name="financing_service_classification2",
	                                                              lookup_expr='exact')
	financing_service_classification3 = django_filters.CharFilter(field_name="financing_service_classification3",
	                                                              lookup_expr='exact')
	financing_service_classification4 = django_filters.CharFilter(field_name="financing_service_classification4",
	                                                              lookup_expr='exact')
	financing_service_classification5 = django_filters.CharFilter(field_name="financing_service_classification5",
	                                                              lookup_expr='exact')
	is_hot = django_filters.BooleanFilter(field_name='is_hot', lookup_expr='exact')
	
	class Meta:
		model = FinancingServices
		fields = ['price_min', 'price_max', 'financing_service_classification1', 'financing_service_classification2',
		          'financing_service_classification3', 'financing_service_classification5', 'is_hot']


class DefaultCategoryFilter(django_filters.rest_framework.FilterSet):
	"""
	普适服务分类过滤类
	"""
	category_type = django_filters.NumberFilter(field_name='category_type', help_text="普适服务分类级别", lookup_expr='exact')
	
	class Meta:
		model = ServiceClassification
		fields = ['category_type', ]


class FinancingCategoryFilter(django_filters.rest_framework.FilterSet):
	"""
	金融服务分类过滤类
	"""
	category_type = django_filters.NumberFilter(field_name='category_type', help_text="金融服务分类级别", lookup_expr='exact')
	
	class Meta:
		model = FinancingServicesClassification
		fields = ['category_type', ]
		

