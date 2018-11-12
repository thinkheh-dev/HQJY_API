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
from xadmin import views
from .models import VerifyCode, UserPermissionsName, UserLabels, UserProfile, UserInfo


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "红企家园后台管理系统"
    site_footer = "ThinkHeH 红企家园"
    menu_style = "accordion"


class UserPermissionsNameAdmin(object):
	list_display = ['permission_name', 'permission_sn', 'permission_desc']


class UserLabelsAdmin(object):
	list_display = ['label_name', ]
	

class UserInfoAdmin(object):
	list_display = ['user_name', 'user_sex', 'user_phone', 'user_ip', 'user_browser', 'user_permissions_name', 'user_labels', 'disable_flag']


class UserProfileAdmin(object):
 	list_display = ['user_id_card', 'user_birthday', 'QQ_num', 'wechat_num', 'contact_address', 'user_email', 'user_real_name_authentication', 'user_info', 'user_to_company', 'enterprise_type_first', 'enterprise_type_second']


class VerifyCodeAdmin(object):
	list_display = ['code', 'user_phone', "add_time"]


xadmin.site.register(UserPermissionsName, UserPermissionsNameAdmin)
xadmin.site.register(UserLabels, UserLabelsAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)