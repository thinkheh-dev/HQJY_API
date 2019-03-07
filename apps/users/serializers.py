#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2018-11-14 09:51
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from datetime import datetime, timedelta
import re

from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.http import request

from .models import VerifyCode, UserPermissionsName
from HQJY_API.settings import REGEX_MOBILE


User = get_user_model()


class SmsSerializer(serializers.Serializer):
	"""
	短信序列化类
	"""
	user_phone = serializers.CharField(max_length=11)
	
	def validate_user_phone(self, user_phone):
		"""
		验证手机号
		:param user_phone:
		:return: user_phone
		"""
		# 验证手机是否存在
		if User.objects.filter(user_phone=user_phone).count():
			raise serializers.ValidationError("用户已经存在")
		
		# 验证手机号是否合法
		if not re.match(REGEX_MOBILE, user_phone):
			raise serializers.ValidationError("手机号不合法")
		
		# 验证码发送频率
		one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
		if VerifyCode.objects.filter(add_time__gt=one_minute_ago, user_phone=user_phone).count():
			raise serializers.ValidationError("验证码发送时间间隔不足60S")
		
		return user_phone


class FindPasswordSmsSerializer(serializers.Serializer):
	"""
	找回密码短信序列化类
	"""
	user_phone = serializers.CharField(max_length=11)
	
	def validate_user_phone(self, user_phone):
		"""
		验证手机号
		:param user_phone:
		:return: user_phone
		"""
		# 验证手机号是否合法
		if not re.match(REGEX_MOBILE, user_phone):
			# return Response({
			# 	"error_messages": "手机号不合法"
			# }, status=status.HTTP_400_BAD_REQUEST)
			raise serializers.ValidationError("手机号不合法", code=status.HTTP_400_BAD_REQUEST)
		
		# 验证手机是否存在
		if not User.objects.filter(user_phone=user_phone).count():
			# return Response({
			# 	"error_messages": "用户不存在，请先注册！"
			# }, status=status.HTTP_400_BAD_REQUEST)
			raise serializers.ValidationError("用户不存在,请先注册", code=status.HTTP_400_BAD_REQUEST)
		
		# 验证码发送频率
		one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
		if VerifyCode.objects.filter(add_time__gt=one_minute_ago, user_phone=user_phone).count():
			# return Response({
			# 	"error_messages": "验证码发送时间间隔不足60S"
			# }, status=status.HTTP_400_BAD_REQUEST)
			raise serializers.ValidationError("验证码发送时间间隔不足60S", code=status.HTTP_400_BAD_REQUEST)
		
		return user_phone


class UserInfoDetailSerializers(serializers.ModelSerializer):
	"""
	用户详情序列化
	"""
	
	class Meta:
		model = User
		fields = ('id', 'user_name', 'user_logo', 'user_sex', 'user_phone', 'user_ip', 'user_browser', 'user_id_card',
		          'user_birthday', 'QQ_num', 'wechat_num', 'contact_address', 'user_email',
		          'user_real_name_authentication', 'user_to_company', 'enterprise_type', 'user_permission_name',
		          'user_labels')


class UserPhoneSerializers(serializers.Serializer):
	"""
	用户手机号异步验证序列化
	"""
	
	user_phone = serializers.CharField(max_length=11)
	
	def validate_user_phone(self, user_phone):
		"""
		验证手机号
		:param user_phone:
		:return: user_phone
		"""
		# 验证手机是否存在
		if User.objects.filter(user_phone=user_phone).count():
			raise serializers.ValidationError("用户已经存在")
		
		# 验证手机号是否合法
		if not re.match(REGEX_MOBILE, user_phone):
			raise serializers.ValidationError("手机号不合法")
		
		return user_phone
	

class UserRegSerializer(serializers.ModelSerializer):
	"""
	用户注册序列化
	"""
	code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, label="验证码",
	                             error_messages={
		                             "blank": "请输入验证码",
		                             "required": "请输入验证码",
		                             "max_length": "验证码格式错误",
		                             "min_length": "验证码格式错误"})
	
	username = serializers.CharField(label="用户名", required=True, allow_blank=False,
	                                 validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
	
	password = serializers.CharField(
		style={'input_type': 'password'}, label="密码", write_only=True,
	)
	
	# def create(self, validated_data):
	# 	user = super(UserRegSerializer, self).create(validated_data=validated_data)
	# 	user.set_password(validated_data["password"])
	# 	user.save()
	# 	return user
	
	def validate_code(self, code):
		
		verify_records = VerifyCode.objects.filter(user_phone=self.initial_data["username"]).order_by("-add_time")
		if verify_records:
			last_record = verify_records[0]
			
			five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
			if five_mintes_ago > last_record.add_time:
				raise serializers.ValidationError("验证码过期")
			
			if last_record.code != code:
				raise serializers.ValidationError("验证码错误")
		
		else:
			raise serializers.ValidationError("验证码错误")
	
	def validate(self, attrs):
		attrs["user_phone"] = attrs["username"]
		del attrs["code"]
		return attrs
	
	class Meta:
		model = User
		fields = ("username", "code", "user_phone", "password", "user_protocol")


class UserFindPasswordSerizlizers(serializers.Serializer):
	"""
	用户通过手机验证码找回密码-获取验证码序列化
	"""
	
	user_phone = serializers.CharField(label="手机号", required=True, allow_blank=False, max_length=11,
	                                   min_length=11, error_messages={
														"blank": "请输入您的手机号",
														"required": "请输入您的手机号",
														"max_length": "手机格式不正确",
														"min_length": "手机格式不正确"})
	
	code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, label="验证码",
	                             error_messages={
		                             "blank": "请输入验证码",
		                             "required": "请输入验证码",
		                             "max_length": "验证码格式错误",
		                             "min_length": "验证码格式错误"})
	
	password = serializers.CharField(style={'input_type': 'password'}, label="密码")
	

	def validate_code(self, code):
		
		verify_records = VerifyCode.objects.filter(user_phone=self.initial_data["user_phone"]).order_by("-add_time")
		if verify_records:
			last_record = verify_records[0]
			
			five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
			if five_mintes_ago > last_record.add_time:
				raise serializers.ValidationError("验证码过期", code=status.HTTP_400_BAD_REQUEST)
			
			if last_record.code != code:
				raise serializers.ValidationError("验证码错误", code=status.HTTP_400_BAD_REQUEST)
		
		else:
			raise serializers.ValidationError("验证码错误", code=status.HTTP_400_BAD_REQUEST)
	
	def validate(self, attrs):
		del attrs["code"]
		return attrs
	
	class Meta:
		model = User
		fields = ("code", "user_phone", "password")

