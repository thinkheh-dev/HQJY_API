#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2018-11-26 15:09
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from rest_framework import serializers
from django.db.models import Q

from .models import ServiceClassification, DefaultServices, FinancingServicesClassification, \
	FinancingServices, ServiceBrand, DefaultServicesPackage, DefaultCouponType, DefaultServiceCoupon, HotSearchWords, \
	EnterpriseDemand, CorporateFinanceDemand


class ServiceClassificationSerializers5(serializers.ModelSerializer):
	class Meta:
		model = ServiceClassification
		fields = "__all__"


class ServiceClassificationSerializers4(serializers.ModelSerializer):
	sub_classification = ServiceClassificationSerializers5(many=True)
	class Meta:
		model = ServiceClassification
		fields = "__all__"


class ServiceClassificationSerializers3(serializers.ModelSerializer):
	sub_classification = ServiceClassificationSerializers4(many=True)
	class Meta:
		model = ServiceClassification
		fields = "__all__"


class ServiceClassificationSerializers2(serializers.ModelSerializer):
	sub_classification = ServiceClassificationSerializers3(many=True)
	class Meta:
		model = ServiceClassification
		fields = "__all__"


class ServiceClassificationSerializers(serializers.ModelSerializer):
	"""
	普适产品分类
	"""
	sub_classification = ServiceClassificationSerializers2(many=True)
	class Meta:
		model = ServiceClassification
		fields = "__all__"
		

class DefaultServicesSerializers(serializers.ModelSerializer):
	"""
	普适产品序列化
	"""
	service_classification = ServiceClassificationSerializers()
	class Meta:
		model = DefaultServices
		fields = "__all__"


class FinancingServicesClassificationSerializers5(serializers.ModelSerializer):
	class Meta:
		model = FinancingServicesClassification
		fields = "__all__"


class FinancingServicesClassificationSerializers4(serializers.ModelSerializer):
	sub_classification = FinancingServicesClassificationSerializers5(many=True)
	
	class Meta:
		model = FinancingServicesClassification
		fields = "__all__"


class FinancingServicesClassificationSerializers3(serializers.ModelSerializer):
	sub_classification = FinancingServicesClassificationSerializers4(many=True)
	
	class Meta:
		model = FinancingServicesClassification
		fields = "__all__"


class FinancingServicesClassificationSerializers2(serializers.ModelSerializer):
	sub_classification = FinancingServicesClassificationSerializers3(many=True)
	
	class Meta:
		model = FinancingServicesClassification
		fields = "__all__"


class FinancingServicesClassificationSerializers(serializers.ModelSerializer):
	"""
	金融产品分类
	"""
	sub_classification = FinancingServicesClassificationSerializers2(many=True)
	
	class Meta:
		model = FinancingServicesClassification
		fields = "__all__"


class FinancingServicesSerializers(serializers.ModelSerializer):
	"""
	金融产品序列化
	"""
	fsc = FinancingServicesClassificationSerializers()
	class Meta:
		model = FinancingServices
		fields = "__all__"