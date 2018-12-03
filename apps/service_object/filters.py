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
from .models import DefaultServices, FinancingServices


class DefaultServicesFilter(django_filters.rest_framework.FilterSet):
	"""
	普适服务过滤类
	"""
	price_min = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最低价格', lookup_expr='gte')
	price_max = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最高价格', lookup_expr='lte')
	# service_name = django_filters.CharFilter(field_name='service_name', help_text='普适服务名称', lookup_expr='icontains')
	# service_sn = django_filters.CharFilter(field_name='service_sn', help_text='服务编号', lookup_expr='icontains')

	
	class Meta:
		model = DefaultServices
		fields = ['price_min', 'price_max']


class FinancingServicesFilter(django_filters.rest_framework.FilterSet):
	"""
	金融服务过滤类
	"""
	price_min = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最低价格', lookup_expr='gte')
	price_max = django_filters.NumberFilter(field_name='service_platform_price', help_text='平台最高价格', lookup_expr='lte')
	
	class Meta:
		model = FinancingServices
		fields = ['price_min', 'price_max']