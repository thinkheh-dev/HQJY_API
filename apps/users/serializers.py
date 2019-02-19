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

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
from django.http import request

from .models import VerifyCode
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


class UserInfoDetailSerializers(serializers.ModelSerializer):
	"""
	用户详情序列化
	"""
	
	class Meta:
		model = User
		fields = ('user_name', 'user_logo', 'user_sex', 'user_phone', 'user_ip', 'user_browser', 'user_id_card',
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
		                             "min_length": "验证码格式错误"
	                             },
	                             help_text="验证码")
	username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
	                                 validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
	password = serializers.CharField(
		style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
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
