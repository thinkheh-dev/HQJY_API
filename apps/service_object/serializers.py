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

from service_object.models import ServiceClassification, DefaultServices, FinancingServiesClassification, \
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
	sub_classification = ServiceClassificationSerializers2(many=True)
	class Meta:
		model = ServiceClassification
		fields = "__all__"
		

class DefaultServicesSerializers(serializers.ModelSerializer):
	service_classification = ServiceClassificationSerializers()
	class Meta:
		model = DefaultServices
		fields = "__all__"
