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
from user_operation.models import ShoppingCart, OrderInfo, OrderServiceDetail, WorkbenchNavConfiguration, \
	WorkbenchParameterConfiguration


class ShoppingCartAdmin(object):
	list_display = ['user_info', 'default_services', 'default_services_package', 'buy_nums']
	

class OrderInfoAdmin(object):
	list_display = ['user_info', 'order_sn', 'order_status', 'order_message', 'order_message', 'order_amount',
	                'default_service_coupon', 'pay_time', 'enterprise_info_service', 'order_contact_name',
	                'order_contact_phone', 'order_remark', 'industry_commissioner']


class OrderServiceDetailAdmin(object):
	list_display = ['order_info', 'default_services', 'default_services_package', 'service_num', 'add_time']


class WorkbenchNavConfigurationAdmin(object):
	list_display = ['name', 'index', 'nav_img', 'nav_url', 'display_flag']
	

class WorkbenchParameterConfigurationAdmin(object):
	list_display = ['name', 'workbench_img', 'workbench_css']


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderServiceDetail, OrderServiceDetailAdmin)
xadmin.site.register(WorkbenchNavConfiguration, WorkbenchNavConfigurationAdmin)
xadmin.site.register(WorkbenchParameterConfiguration, WorkbenchParameterConfigurationAdmin)
