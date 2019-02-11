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
	EnterpriseDemand, CorporateFinanceDemand, DefaultServicesImage, FinancingServicesImage, DefaultServicesBanner, \
	FinancingServicesBanner

#普适服务分类序列化函数--开始
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
#普适服务分类序列化函数--结束


class ServiceClassificationNavSerializers(serializers.ModelSerializer):
	"""
	普通服务分类导航
	"""
	class Meta:
		model = ServiceClassification
		fields = ('name', 'ico_str', 'ico_file', 'category_type')


class DefaultServicesImageSerializers(serializers.ModelSerializer):
	"""
	普适服务轮播图
	"""
	class Meta:
		model = DefaultServicesImage
		fields = ('image', )


class DefaultServicesSerializers(serializers.ModelSerializer):
	"""
	普适产品序列化
	"""
	service_classification = ServiceClassificationSerializers()
	default_images = DefaultServicesImageSerializers(many=True)
	class Meta:
		model = DefaultServices
		fields = "__all__"

#金融服务分类序列化函数--开始
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
#金融服务分类序列化函数--结束

class FinancingServicesClassificationNavSerializers(serializers.ModelSerializer):
	"""
	金融服务分类导航
	"""
	class Meta:
		model = FinancingServicesClassification
		fields = ('name', 'ico_str', 'ico_file', 'category_type')


class FinancingServicesImageSerializers(serializers.ModelSerializer):
	"""
	金融服务轮播图序列化
	"""
	class Meta:
		model = FinancingServicesImage
		fields = ("image", )


class FinancingServicesSerializers(serializers.ModelSerializer):
	"""
	金融产品序列化
	"""
	fsc = FinancingServicesClassificationSerializers()
	financing_images = FinancingServicesImageSerializers(many=True)
	class Meta:
		model = FinancingServices
		fields = "__all__"
		

class ServiceBrandSerializers(serializers.ModelSerializer):
	"""
	服务品牌序列化
	"""
	class Meta:
		model = ServiceBrand
		fields = "__all__"
		
class DefaultServicesPackageSerializers(serializers.ModelSerializer):
	"""
	普适项目服务包序列化
	"""
	class Meta:
		model = DefaultServicesPackage
		fields = "__all__"


class DefaultCouponTypeSerializers(serializers.ModelSerializer):
	"""
	普适服务优惠券类型序列化
	"""
	class Meta:
		model = DefaultCouponType
		fields = "__all__"
		

class DefaultServiceCouponSerializers(serializers.ModelSerializer):
	"""
	普适服务优惠券序列化
	"""
	default_coupon_type = DefaultCouponTypeSerializers()
	
	class Meta:
		model = DefaultServiceCoupon
		fields = "__all__"


class HotSearchWordsSerializers(serializers.ModelSerializer):
	"""
	热搜词序列化
	"""
	class Meta:
		model = HotSearchWords
		fields = "__all__"
		
		
class DefaultServicesBannerSerializers(serializers.ModelSerializer):
	"""
	普适服务轮播图
	"""
	class Meta:
		model = DefaultServicesBanner
		fields = "__all__"
		
		
class FinancingServicesBannerSerializers(serializers.ModelSerializer):
	"""
	金融服务轮播图
	"""
	class Meta:
		model = FinancingServicesBanner
		fields = "__all__"
		

class EnterpriseDemandSerializers(serializers.ModelSerializer):
	"""
	企业普适服务需求序列化
	"""
	sv_class = ServiceClassificationSerializers()
	
	class Meta:
		model = EnterpriseDemand
		fields = "__all__"
		

class CorporateFinanceDemandSerializers(serializers.ModelSerializer):
	"""
	企业金融服务需求序列化
	"""
	fsc_class =  FinancingServicesClassificationSerializers()
	
	class Meta:
		model = CorporateFinanceDemand
		fields = "__all__"
