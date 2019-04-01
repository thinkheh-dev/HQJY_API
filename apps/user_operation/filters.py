#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-03-29 10:30
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : filters.py
# @software: PyCharm

import django_filters
from user_operation.models import OrderInfo


class OrderInfoFilter(django_filters.rest_framework.FilterSet):
	"""
	订单信息过滤类
	"""
	order_status = django_filters.CharFilter(field_name='order_status', help_text='订单状态',
	                                          lookup_expr='exact')
	order_sn  = django_filters.CharFilter(field_name='order_sn', help_text='订单编号', lookup_expr='exact')
	order_amount_min = django_filters.NumberFilter(field_name='order_amount', lookup_expr='gte')
	order_amount_max = django_filters.NumberFilter(field_name='order_amount', lookup_expr='lte')
	
	order_add_time = django_filters.DateFromToRangeFilter(field_name='order_add_time', lookup_expr='gte',
	                                                      label='订单下单时间')
	
	class Meta:
		model = OrderInfo
		fields = ['order_status', 'order_sn', 'order_amount_min', 'order_amount_max', 'order_add_time']
