#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-01-30 10:26
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from rest_framework import serializers
from django.db.models import Q

from .models import EnterpriseTypeLevel, EnterpriseType, BasicEnterpriseInfo, EnterpriseLabel


class EnterpriseLabelSerializers(serializers.ModelSerializer):
	"""
	企业标签序列化
	"""
	class Meta:
		model = EnterpriseLabel
		fields = "__all__"

class EnterpriseTypeLevelSerializers(serializers.ModelSerializer):
	"""
	企业级别序列化
	"""
	class Meta:
		model = EnterpriseTypeLevel
		fields = "__all__"
		

#企业类型序列化 -- 开始
class EnterpriseTypeSerializers3(serializers.ModelSerializer):
	
	class Meta:
		model = EnterpriseType
		fields = "__all__"


class EnterpriseTypeSerializers2(serializers.ModelSerializer):
	
	sub_classification = EnterpriseTypeSerializers3(many=True)
	
	class Meta:
		model = EnterpriseType
		fields = "__all__"
		
class EnterpriseTypeSerializers(serializers.ModelSerializer):
	
	sub_classification = EnterpriseTypeSerializers2(many=True)
	
	class Meta:
		model = EnterpriseType
		fields = "__all__"
#企业类型序列化 -- 结束


class BasicEnterpriseInfoSerializers(serializers.ModelSerializer):
	"""
	企业基本信息序列化
	"""
	enterprise_type = EnterpriseTypeSerializers()
	enterprise_label = EnterpriseLabelSerializers()
	
	class Meta:
		model = BasicEnterpriseInfo
		fields = "__all__"

		

