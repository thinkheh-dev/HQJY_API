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
from platform_operation.models import InfoCategories, WeMediaArticles, PlatformActivity, \
	ActivityRegList, ActivityRegistration


class InfoCategoriesAdmin(object):
	list_display = ['name', 'code', 'desc', 'category_type', 'parent_category', 'is_tab', 'add_time']
	

# class InfoCategoriesSecondAdmin(object):
# 	list_display = ['section_name', 'info_categories']


class WeMediaArticlesAdmin(object):
	list_display = ['title', 'subtitle', 'info_categories', 'abstract', 'content',
	                'attachment', 'publish_time', 'author', 'read_nums', 'fav_nums']
	style_fields = {"content": "ueditor"}
	

class WeMediaArticleFavAdmin(object):
	list_display = ['user_info', 'wemedia_article', 'add_time']


class PlatformActivityAdmin(object):
	list_display = ['activity_title', 'activity_posters', 'activity_organizer', 'activity_start_time',
	                'activity_end_time', 'activity_address', 'activity_desc', 'activity_tickets', 'meals_flag',
	                'accommodation_flag', 'add_time']
	style_fields = {"activity_desc": "ueditor"}


class ActivityRegListAdmin(object):
	list_display = ['name', 'sex', 'national', 'phone']


class ActivityRegistrationAdmin(object):
	list_display = ['reg_account', 'reg_company', 'reg_number', 'meals_number', 'accommodation_number', 'reg_list']
	
	
xadmin.site.register(InfoCategories, InfoCategoriesAdmin)
#xadmin.site.register(InfoCategoriesSecond, InfoCategoriesSecondAdmin)
xadmin.site.register(WeMediaArticles, WeMediaArticlesAdmin)
xadmin.site.register(PlatformActivity, PlatformActivityAdmin)
xadmin.site.register(ActivityRegList, ActivityRegListAdmin)
xadmin.site.register(ActivityRegistration, ActivityRegistrationAdmin)
