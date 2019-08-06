#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019/8/6 上午9:23
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm


from rest_framework import serializers, status

from .models import WebLogo, WebName, WebFooterInfo, WebFooterLink


class WebLogoSerializers(serializers.ModelSerializer):
	"""
	网站logo序列化
	"""
	class Meta:
		model = WebLogo
		fields = "__all__"
		
		
class WebNameSerializers(serializers.ModelSerializer):
	"""
	网站名称序列化
	"""
	class Meta:
		model = WebName
		fields = "__all__"

		
class WebFooterInfoSerializers(serializers.ModelSerializer):
	"""
	网站页脚信息序列化
	"""
	class Meta:
		model = WebFooterInfo
		fields = "__all__"
		

class WebFooterLinkSerializers(serializers.ModelSerializer):
	"""
	网站友情链接序列化
	"""
	class Meta:
		model = WebFooterLink
		fields = "__all__"

