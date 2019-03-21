#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-03-15 09:44
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : adminx.py
# @software: PyCharm

import xadmin
from xadmin import views
from .models import AttachResources, AttachLibraryManager

class AttachLibraryManagerAdmin(object):
	list_display = ['library_name', 'attach_author', 'add_time']
	search_fields = ['library_name', 'attach_author']
	list_filter = ['library_name', 'attach_author', 'add_time']
	
	class AttachResourcesInline(object):
		model = AttachResources
		exclude = ['add_time']
		extra = 1
		
	inlines = [AttachResourcesInline]


xadmin.site.register(AttachLibraryManager, AttachLibraryManagerAdmin)
