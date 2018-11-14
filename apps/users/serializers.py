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
		:return:
		"""
		#验证手机是否存在
		if User.objects.filter(user_phone = user_phone).count():
			raise serializers.ValidationError("用户已经存在")
		
		#验证手机号是否合法
		if not re.match(REGEX_MOBILE, user_phone):
			raise serializers.ValidationError("手机号不合法")
		
		#验证码发送频率
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
		fields = ('user_name', 'user_sex', 'user_phone', 'user_ip', 'user_browser', 'user_id_card', 'user_birthday',
		          'QQ_num', 'wechat_num', 'contact_address', 'user_email', 'user_real_name_authentication',
		          'user_to_company', 'enterprise_type_first', 'enterprise_type_second','user_permissions_name',
		          'user_labels', 'disable_flag')
	
