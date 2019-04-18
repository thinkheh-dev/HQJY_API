#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-04-11 16:09
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : filters.py
# @software: PyCharm
import django_filters
from .models import BasicEnterpriseInfo

class BasicEnterpriseInfoFilter(django_filters.rest_framework.FilterSet):
	"""
	企业信息筛选器
	"""
	enterprise_name = django_filters.CharFilter(field_name='name', help_text='企业名称', lookup_expr='icontains')
	credit_no = django_filters.CharFilter(field_name='credit_no', help_text='统一信用代码', lookup_expr='exact')
	oper_name = django_filters.CharFilter(field_name='oper_name', help_text='法人姓名', lookup_expr='exact')
	company_area = django_filters.ChoiceFilter(choices=BasicEnterpriseInfo.COUNTY_CHOICES, help_text='公司归属地', lookup_expr='exact')
	
	class Meta:
		model = BasicEnterpriseInfo
		fields = ['enterprise_name', 'credit_no', 'oper_name', 'company_area']