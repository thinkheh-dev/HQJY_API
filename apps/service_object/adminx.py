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
	FinancingServicesClassification,FinancingServices, ServiceBrand, DefaultCouponType, DefaultServicesPackage, \
	DefaultServiceCoupon, HotSearchWords,EnterpriseDemand, CorporateFinanceDemand, DefaultServicesImage, \
	FinancingServicesImage, DefaultServicesBanner, FinancingServicesBanner


class ServiceClassificationAdmin(object):
	list_display = ['name', 'code', 'ico_str', 'ico_file', 'desc', 'category_type', 'is_tab', 'add_time']


# 已舍弃
# class ServiceClassificationSecondAdmin(object):
# 	list_display = ['classis_name', 'service_classification']


class DefaultServicesAdmin(object):
	list_display = ['service_sn','service_belong_to_company','service_name','service_classification1',
	                'service_classification2','service_classification3','service_classification4',
	                'service_classification5', 'service_inventory', 'service_market_price', 'service_platform_price']
	search_fields = ['service_name', ]
	list_editable = ['is_hot', ]
	list_filter = ['service_name', 'service_sn', 'service_clicks', 'service_sales', 'service_fav_nums',
	               'service_market_price', 'service_platform_price']
	style_fields = {"service_detailed_description": "ueditor"}
	
	class DefaultServicesImageInline(object):
		model = DefaultServicesImage
		exclude = ['add_time']
		extra = 1
		
	inlines = [DefaultServicesImageInline]


class FinancingServicesClassificationAdmin(object):
	list_display = ['name', 'code', 'ico_str', 'ico_file', 'desc', 'category_type', 'is_tab', 'add_time']


# 已舍弃
# class FinancingServicesClassificationSecondAdmin(object):
# 	list_display = ['name', 'fscs']


class FinancingServicesAdmin(object):
	list_display = ['service_sn','service_belong_to_company','service_name', 'financing_service_classification1',
	                'financing_service_classification2', 'financing_service_classification3',
	                'financing_service_classification4', 'financing_service_classification5', 'time_limit',
	                'annual_interest_rate', 'approval_lines']
	search_fields = ['service_name', ]
	list_editable = ['is_hot', ]
	list_filter = ['service_name', 'service_sn', 'service_clicks', 'service_sales', 'service_fav_nums',
	               'service_market_price', 'service_platform_price']
	style_fields = {"service_detailed_description": "ueditor"}
	
	class FinancingServicesImageInline(object):
		model = FinancingServicesImage
		exclude = ['add_time']
		extra = 1
	
	inlines = [FinancingServicesImageInline]


class DefaultServicesPackageAdmin(object):
	list_display = ['package_name', 'package_img', 'package_desc', 'default_service']
	style_fields = {"package_desc": "ueditor"}
	
	
class ServiceBrandAdmin(object):
	list_display = ['brand_name', 'brand_desc', 'brand_img', 'add_time']
	
	
class DefaultCouponTypeAdmin(object):
	list_display = ['name', ]

	
class DefaultServiceCouponAdmin(object):
	list_display = ['coupon_name', 'coupon_amount', 'coupon_img', 'coupon_desc', 'coupon_start_time',
	                'coupon_end_time', 'belong_coupon', 'default_coupon_type', 'add_time', 'default_num', 'remain_num']

	
class HotSearchWordsAdmin(object):
	list_display = ['keywords', 'key_index', 'add_time']
	

class DefaultServicesImageAdmin(object):
	list_display = ['default_services', 'image', 'add_time']
	
	
class FinancingServicesImageAdmin(object):
	list_display = ['financing_services', 'image', 'add_time']

	
class DefaultServicesBannerAdmin(object):
	list_display = ['default_services', 'image', 'index', 'add_time']
	
	
class FinancingServicesBannerAdmin(object):
	list_display = ['financing_services', 'image', 'index', 'add_time']


class EnterpriseDemandAdmin(object):
	list_display = ['sv_class', ]
	style_fields = {"demand_desc": "ueditor"}


class CorporateFinanceDemandAdmin(object):
	list_display = ['fsc', 'financing_amount', 'financing_to', 'financing_maturity']
	style_fields = {"demand_desc": "ueditor"}


xadmin.site.register(ServiceClassification, ServiceClassificationAdmin)
# xadmin.site.register(ServiceClassificationSecond, ServiceClassificationSecondAdmin) 已舍弃
xadmin.site.register(DefaultServices, DefaultServicesAdmin)
xadmin.site.register(FinancingServicesClassification, FinancingServicesClassificationAdmin)
# xadmin.site.register(FinancingServicesClassificationSecond, FinancingServicesClassificationSecondAdmin) 已舍弃
xadmin.site.register(FinancingServices, FinancingServicesAdmin)
xadmin.site.register(DefaultServicesPackage, DefaultServicesPackageAdmin)
xadmin.site.register(ServiceBrand, ServiceBrandAdmin)
xadmin.site.register(DefaultCouponType, DefaultCouponTypeAdmin)
xadmin.site.register(DefaultServiceCoupon, DefaultServiceCouponAdmin)
xadmin.site.register(HotSearchWords, HotSearchWordsAdmin)
xadmin.site.register(DefaultServicesImage, DefaultServicesImageAdmin)
xadmin.site.register(FinancingServicesImage, FinancingServicesImageAdmin)
xadmin.site.register(DefaultServicesBanner, DefaultServicesBannerAdmin)
xadmin.site.register(FinancingServicesBanner, FinancingServicesBannerAdmin)
xadmin.site.register(EnterpriseDemand, EnterpriseDemandAdmin)
xadmin.site.register(CorporateFinanceDemand, CorporateFinanceDemandAdmin)
