#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-03-15 09:44
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from rest_framework import serializers

from .models import AttachLibraryManager, AttachResources

class AttachLibraryManagerSerializers(serializers.ModelSerializer):
	"""
	资料库管理序列化
	"""
	class Meta:
		model = AttachLibraryManager
		fields = ['library_name', 'attach_author', ]


class AttachResourcesSerializers(serializers.ModelSerializer):
	"""
	附件资源序列化
	"""
	attach_library_manager = AttachLibraryManagerSerializers()
	class Meta:
		model = AttachResources
		fields = ['attach_name', 'attach_type', 'attach_desc', 'attach_file', 'attach_library_manager']



		
