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
	EnterpriseReviewFile, EnterpriseAuthManuallyReview, BasicEnterpriseInfoTemp


class EnterpriseLabelAdmin(object):
	list_display = ['name', 'label_ico', 'level']


class EnterpriseTypeLevelAdmin(object):
	list_display = ['name', 'level']


class EnterpriseTypeAdmin(object):
	list_display = ['name', 'code', 'desc', 'category_type', 'add_time']


class EnterpriseReviewFileAdmin(object):
	list_display = ['eps_review_template_file', 'add_time']


class EnterpriseAuthManuallyReviewAdmin(object):
	list_display = ['user_id', 'enterprise_code', 'enterprise_oper_name', 'enterprise_oper_idcard',
	                'enterprise_license', 'enterprise_review', 'apply_audit_status', 'add_time', 'update_time']


class BasicEnterpriseInfoTempAdmin(object):
	list_display = ['name', 'credit_no', 'oper_name', 'reg_no', 'econ_kind', 'regist_capi', 'reg_capcur', 'status',
	                'cancel_date', 'revoke_date', 'start_date', 'term_start', 'term_end', 'belong_org',
	                'abu_item', 'cbu_item', 'operate_scope', 'operate_scope_and_form', 'org_code', 'appr_date',
	                'province', 'city', 'county', 'area_code', 'industry_phycode', 'industry_phyname', 'industry_code',
	                'industry_name', 'contact_name', 'contact_phone', 'scan_of_company_license',
	                'scan_of_id_card', 'add_time']


class BasicEnterpriseInfoAdmin(object):
	list_display = ['name', 'credit_no', 'oper_name', 'reg_no', 'econ_kind', 'regist_capi', 'reg_capcur', 'status',
	                'cancel_date', 'revoke_date', 'start_date', 'term_start', 'term_end', 'belong_org',
	                'abu_item', 'cbu_item', 'operate_scope', 'operate_scope_and_form', 'org_code', 'appr_date',
	                'province', 'city', 'county', 'area_code', 'industry_phycode', 'industry_phyname', 'industry_code',
	                'industry_name', 'enterprise_label', 'contact_name', 'contact_phone', 'scan_of_company_license',
	                'scan_of_id_card', 'add_time']


xadmin.site.register(EnterpriseLabel, EnterpriseLabelAdmin)
xadmin.site.register(EnterpriseTypeLevel, EnterpriseTypeLevelAdmin)
xadmin.site.register(EnterpriseType, EnterpriseTypeAdmin)
xadmin.site.register(EnterpriseReviewFile, EnterpriseReviewFileAdmin)
xadmin.site.register(EnterpriseAuthManuallyReview, EnterpriseAuthManuallyReviewAdmin)
xadmin.site.register(BasicEnterpriseInfo, BasicEnterpriseInfoAdmin)
xadmin.site.register(BasicEnterpriseInfoTemp, BasicEnterpriseInfoTempAdmin)
