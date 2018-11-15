#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2018-11-07 16:35
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : adminx.py
# @software: PyCharm

import xadmin
from service_object.models import ServiceAbstractClass, ServiceClassification, DefaultServices, \
	FinancingServiesClassification,FinancingServices, ServiceBrand, DefaultCouponType, DefaultServicesPackage, \
	DefaultServiceCoupon, HotSearchWords,EnterpriseDemand, CorporateFinanceDemand


class ServiceClassificationAdmin(object):
	list_display = ['name', 'code', 'desc', 'category_type', 'is_tab', 'add_time']


# class ServiceClassificationSecondAdmin(object):
# 	list_display = ['classis_name', 'service_classification']
	

class DefaultServicesAdmin(object):
	list_display = ['service_classification', 'service_inventory',
	                'service_market_price', 'service_platform_price']
	style_fields = {"service_detailed_description": "ueditor"}


class FinancingServiesClassificationAdmin(object):
	list_display = ['name', 'code', 'desc', 'category_type', 'is_tab', 'add_time']


# class FinancingServicesClassificationSecondAdmin(object):
# 	list_display = ['name', 'fscs']


class FinancingServicesAdmin(object):
	list_display = ['fsc', 'time_limit', 'annual_interest_rate', 'approval_lines']
	
	
class ServiceBrandAdmin(object):
	list_display = ['brand_name', 'brand_desc', 'brand_img', 'add_time']
	
	
class DefaultCouponTypeAdmin(object):
	list_display = ['name', ]
	

class DefaultServicesPackageAdmin(object):
	list_display = ['package_name', 'package_img', 'package_desc', 'default_service']

	
class DefaultServiceCouponAdmin(object):
	list_display = ['coupon_name', 'coupon_amount', 'coupon_img', 'coupon_desc', 'coupon_start_time',
	                'coupon_end_time', 'belong_coupon', 'default_coupon_type', 'add_time', 'default_num', 'remain_num']

	
class HotSearchWordsAdmin(object):
	list_display = ['keywords', 'key_index', 'add_time']
	

class EnterpriseDemandAdmin(object):
	list_display = ['sv_class', ]


class CorporateFinanceDemandAdmin(object):
	list_display = ['fsc', 'financing_amount', 'financing_to', 'financing_maturity']


xadmin.site.register(ServiceClassification, ServiceClassificationAdmin)
# xadmin.site.register(ServiceClassificationSecond, ServiceClassificationSecondAdmin)
xadmin.site.register(DefaultServices, DefaultServicesAdmin)
xadmin.site.register(FinancingServiesClassification, FinancingServiesClassificationAdmin)
# xadmin.site.register(FinancingServicesClassificationSecond, FinancingServicesClassificationSecondAdmin)
xadmin.site.register(FinancingServices, FinancingServicesAdmin)
xadmin.site.register(ServiceBrand, ServiceBrandAdmin)
xadmin.site.register(DefaultCouponType, DefaultCouponTypeAdmin)
xadmin.site.register(DefaultServicesPackage, DefaultServicesPackageAdmin)
xadmin.site.register(DefaultServiceCoupon, DefaultServiceCouponAdmin)
xadmin.site.register(HotSearchWords, HotSearchWordsAdmin)
xadmin.site.register(EnterpriseDemand, EnterpriseDemandAdmin)
xadmin.site.register(CorporateFinanceDemand, CorporateFinanceDemandAdmin)
