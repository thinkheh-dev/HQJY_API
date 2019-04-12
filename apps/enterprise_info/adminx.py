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
from enterprise_info.models import EnterpriseTypeLevel, EnterpriseType, BasicEnterpriseInfo, EnterpriseLabel, \
	EnterpriseReviewFile, EnterpriseAuthManuallyReview


class EnterpriseLabelAdmin(object):
	list_display = ['name', 'label_ico', 'level']


class EnterpriseTypeLevelAdmin(object):
	list_display = ['name', 'level']
	
	
class EnterpriseTypeAdmin(object):
	list_display = ['name', 'code', 'desc', 'category_type', 'add_time']
	
	
class EnterpriseReviewFileAdmin(object):
	list_display = ['eps_review_template_file', 'add_time']
	

class EnterpriseAuthManuallyReviewAdmin(object):
	list_display = ['user_id', 'enterprise_name', 'enterprise_oper_name', 'enterprise_oper_idcard',
	                'enterprise_license', 'enterprise_review', 'apply_audit_status', 'add_time', 'update_time']
	
	
	
class BasicEnterpriseInfoAdmin(object):
	list_display = ['name', 'credit_no', 'oper_name', 'econ_kind', 'regist_capi', 'scope', 'status', 'address',
	                'start_date', 'term_start', 'term_end', 'belong_org', 'company_area', 'enterprise_type',
	                'enterprise_label', 'oper_phone', 'scan_of_company_license',
	                'scan_of_id_card']


xadmin.site.register(EnterpriseLabel, EnterpriseLabelAdmin)
xadmin.site.register(EnterpriseTypeLevel, EnterpriseTypeLevelAdmin)
xadmin.site.register(EnterpriseType, EnterpriseTypeAdmin)
xadmin.site.register(EnterpriseReviewFile, EnterpriseReviewFileAdmin)
xadmin.site.register(EnterpriseAuthManuallyReview, EnterpriseAuthManuallyReviewAdmin)
xadmin.site.register(BasicEnterpriseInfo, BasicEnterpriseInfoAdmin)
