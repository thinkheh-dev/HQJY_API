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
from page_control.models import WebLogo, WebFooterLink, WebFooterInfo, WebName, ADConfig, SystemAdminURL


# class HomeNavAdmin(object):
# 	list_display = ['nav_name', 'nav_image', 'nav_link']
	

# class HomeBackgroundAdmin(object):
# 	list_display = ['img_default', 'img_upload', 'img_url']
	

class WebLogoAdmin(object):
	list_display = ['img_logo', 'img_url', 'img_enable']


class WebFooterLinkAdmin(object):
	list_display = ['link_logo', 'link_name', 'link_url']


class WebFooterInfoAdmin(object):
	list_display = ['web_contact', 'web_address', 'web_icp', 'web_security_info', 'wechat_qrcode', 'wechat_qrcode2']


class WebNameAdmin(object):
	list_display = ['web_name', 'name_display']


class ADConfigAdmin(object):
	list_display = ['ad_img', 'img_description', 'img_index', 'ad_index']
	

class SystemAdminURLAdmin(object):
	list_display = ['web_admin_url', ]
	
	
xadmin.site.register(WebLogo, WebLogoAdmin)
xadmin.site.register(WebFooterLink, WebFooterLinkAdmin)
xadmin.site.register(WebFooterInfo, WebFooterInfoAdmin)
xadmin.site.register(WebName, WebNameAdmin)
xadmin.site.register(ADConfig, ADConfigAdmin)
xadmin.site.register(SystemAdminURL, SystemAdminURLAdmin)
