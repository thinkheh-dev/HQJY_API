#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-03-26 09:35
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from rest_framework import serializers, status
from rest_framework.response import Response

from .models import UserFav, OrderInfo, OrderServiceDetail
from service_object.models import DefaultServices, FinancingServices, DefaultServicesPackage
from service_object.serializers import DefaultServicesSerializers, FinancingServicesSerializers, \
	DefaultServicesPackageSerializers, DefaultCouponTypeSerializers, DefaultServiceCouponSerializers


class UserFavDetailSerializers(serializers.ModelSerializer):
	"""
	用户收藏商品详情序列化
	"""
	default_services = DefaultServicesSerializers(many=False)
	financing_services = FinancingServicesSerializers(many=False)
	default_services_package = DefaultServicesPackageSerializers(many=False)
	
	class Meta:
		model = UserFav
		fields = "__all__"
	

class UserFavSerializers(serializers.Serializer):
	"""
	用户收藏序列化
	"""
	
	user_info = serializers.HiddenField(default=serializers.CurrentUserDefault())
	default_services = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, allow_empty=True,
	                                                      queryset=DefaultServices.objects.all())
	financing_services = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, allow_empty=True,
	                                                        queryset=FinancingServices.objects.all())
	default_services_package = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, allow_empty=True,
	                                                              queryset=DefaultServicesPackage.objects.all())
	
	def create(self, validated_data):
		"""
		用户收藏create方法
		:param validated_data:
		:return:
		"""
		user = self.context['request'].user
		# print(user)
		

		default_services = validated_data['default_services']
		

		financing_services = validated_data['financing_services']


		default_services_package = validated_data['default_services_package']

		
		existed = UserFav.objects.filter(user_info=user, default_services=default_services,
		                                      financing_services=financing_services, default_services_package=default_services_package)
		
		if existed:
			existed = existed[0]
			raise serializers.ValidationError(detail={"error_message": "已收藏过该商品", "error_code":
														  status.HTTP_400_BAD_REQUEST, "existed": existed})
		else:
			existed = UserFav.objects.create(**validated_data)
			# return Response({"exisited":existed}, status=status.HTTP_201_CREATED)
		
		return existed
	

	
class OrderInfoSerializers(serializers.ModelSerializer):
	"""
	订单序列化
	"""
	
	user_info = serializers.HiddenField(default=serializers.CurrentUserDefault())
	default_services = serializers.CharField(label="普适服务产品id", required=False, allow_null=True, allow_blank=True,
	                                         write_only=True)
	financing_services = serializers.CharField(label="金融产品id", required=False, allow_null=True, allow_blank=True,
	                                           write_only=True)
	default_services_package = serializers.CharField(label="普适服务产品包id", required=False, allow_null=True,
	                                                 allow_blank=True, write_only=True)
	
	#不显示给用户的字段
	order_sn = serializers.UUIDField(read_only=True)
	order_status = serializers.CharField(read_only=True)
	order_remark = serializers.CharField(read_only=True)
	industry_commissioner = serializers.CharField(read_only=True)
	
	
	class Meta:
		model = OrderInfo
		fields = "__all__"


class OrderServiceDetailSerialziers(serializers.ModelSerializer):
	"""
	订单商品详情序列化
	"""
	order_info = OrderInfoSerializers()
	default_services = DefaultServicesSerializers()
	financing_services = FinancingServicesSerializers()
	default_services_package = DefaultServicesPackageSerializers()
	
	class Meta:
		model = OrderServiceDetail
		fields = ['order_info', 'default_services', 'financing_services', 'default_services_package']
