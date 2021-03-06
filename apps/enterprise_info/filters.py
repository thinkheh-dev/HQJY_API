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
from .models import BasicEnterpriseInfo, EnterpriseAuthManuallyReview
from users.models import UserInfo
from service_object.models import DefaultServices, FinancingServices
from user_operation.models import OrderInfo


class BasicEnterpriseInfoFilter(django_filters.rest_framework.FilterSet):
    """
    企业信息筛选器
    """
    enterprise_name = django_filters.CharFilter(field_name='name', help_text='企业名称', lookup_expr='icontains')
    credit_no = django_filters.CharFilter(field_name='credit_no', help_text='统一信用代码', lookup_expr='exact')
    oper_name = django_filters.CharFilter(field_name='oper_name', help_text='法人姓名', lookup_expr='exact')
    # company_area = django_filters.ChoiceFilter(choices=BasicEnterpriseInfo.COUNTY_CHOICES, help_text='公司归属地',
    # lookup_expr='exact')

    class Meta:
        model = BasicEnterpriseInfo
        fields = ['enterprise_name', 'credit_no', 'oper_name']


class EnterpriseInfoOperatorDetailFilter(django_filters.rest_framework.FilterSet):
    """
    企业及负责人信息筛选器
    """
    user_to_company = django_filters.CharFilter(field_name='user_to_company', help_text='企业外键', lookup_expr='exact')

    class Meta:
        model = UserInfo
        fields = ['user_to_company', ]


class EnterpriseSelfDefaultServicesFilter(django_filters.rest_framework.FilterSet):
    """
    企业归属普适服务产品筛选器
    """
    ds_belong_to_company = django_filters.CharFilter(field_name='service_belong_to_company', help_text='企业外键',
                                                     lookup_expr='exact')

    class Meta:
        model = DefaultServices
        fields = ['ds_belong_to_company', ]


class EnterpriseSelfFinancingServicesFilter(django_filters.rest_framework.FilterSet):
    """
    企业归属金融服务产品筛选器
    """
    fs_belong_to_company = django_filters.CharFilter(field_name='service_belong_to_company', help_text='企业外键',
                                                     lookup_expr='exact')

    class Meta:
        model = FinancingServices
        fields = ['fs_belong_to_company', ]


class EnterpriseSelfOrderFilter(django_filters.rest_framework.FilterSet):
    """
    企业归属订单筛选器
    """
    # order_user = django_filters.CharFilter(field_name='user_info', help_text='企业用户外键', lookup_expr='exact')
    price_min = django_filters.NumberFilter(label="最低价格", field_name='order_amount', help_text='平台最低价格',
                                            lookup_expr='gte')
    price_max = django_filters.NumberFilter(label="最高价格", field_name='order_amount', help_text='平台最高价格',
                                            lookup_expr='lte')

    class Meta:
        model = OrderInfo
        fields = ['order_sn', 'order_status', 'price_min', 'price_max']


class EnterpriseAuthListFilter(django_filters.rest_framework.FilterSet):
    """
    企业认证列表筛选器
    """

    auth_status = django_filters.ChoiceFilter(label="审核状态", field_name='apply_audit_status',
                                              choices=EnterpriseAuthManuallyReview.STATUS, help_text='审核状态选择',
                                              lookup_expr='exact')
    soc_mark_flag = django_filters.BooleanFilter(label="是否服务机构申请", field_name='soc_mark_flag')
    audit_valid_flag = django_filters.BooleanFilter(label="验证信息是否有效", field_name='audit_valid_flag')

    class Meta:
        model = EnterpriseAuthManuallyReview
        fields = ['auth_status', 'soc_mark_flag', 'audit_valid_flag']
