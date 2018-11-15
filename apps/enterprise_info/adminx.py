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
from enterprise_info.models import EnterpriseTypeLevel, EnterpriseType, BasicEnterpriseInfo

class EnterpriseTypeLevelAdmin(object):
	list_display = ['name', 'level']
	
class EnterpriseTypeAdmin(object):
	list_display = ['name', 'code', 'desc', 'category_type', 'add_time']
	
class BasicEnterpriseInfoAdmin(object):
	list_display = ['name', 'credit_no', 'oper_name', 'econ_kind', 'regist_capi', 'scope', 'status', 'address',
	                'start_date', 'term_start', 'term_end', 'belong_org', 'company_area', 'company_area',
	                'enterprise_type', 'oper_phone', 'scan_of_company_license',
	                'scan_of_id_card']

xadmin.site.register(EnterpriseTypeLevel, EnterpriseTypeLevelAdmin)
xadmin.site.register(EnterpriseType, EnterpriseTypeAdmin)
xadmin.site.register(BasicEnterpriseInfo, BasicEnterpriseInfoAdmin)
