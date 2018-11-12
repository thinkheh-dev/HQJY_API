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
from enterprise_info.models import EnterpriseTypeFirst, EnterpriseTypeSecond, BasicEnterpriseInfo

class EnterpriseTypeFirstAdmin(object):
	list_display = ['first_type_name', ]
	
class EnterpriseTypeSecondAdmin(object):
	list_display = ['second_type_name', 'enterprise_type_first']
	
class BasicEnterpriseInfoAdmin(object):
	list_display = ['name', 'credit_no', 'oper_name', 'econ_kind', 'regist_capi', 'scope', 'status', 'address',
	                'start_date', 'term_start', 'term_end', 'belong_org', 'company_area', 'company_area',
	                'enterprise_type_first', 'enterprise_type_second', 'oper_phone', 'scan_of_company_license',
	                'scan_of_id_card']


xadmin.site.register(EnterpriseTypeFirst, EnterpriseTypeFirstAdmin)
xadmin.site.register(EnterpriseTypeSecond, EnterpriseTypeSecondAdmin)
xadmin.site.register(BasicEnterpriseInfo, BasicEnterpriseInfoAdmin)
