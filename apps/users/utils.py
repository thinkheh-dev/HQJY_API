#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-02-26 17:25
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : utils.py
# @software: PyCharm

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.throttling import SimpleRateThrottle


User = get_user_model()


def jwt_response_payload_handler(token, user=None, request=None):
	"""为返回的结果添加用户相关信息"""
	
	# 解决登录用户获取公司信息报错
	company_id = User.objects.filter(pk=user.id).values_list('user_to_company', flat=True)[0]

	return {
		'token': token,
		'user_id': user.id,
		'username': user.username,
		'user_permission_name': user.user_permission_name.permission_sn,
		'user_logo': user.user_logo.url,
		'user_home': user.user_home,
		'is_staff': user.is_staff,
		'is_superuser': user.is_superuser,
		'user_to_company': company_id
	}


class CustomBackend(ModelBackend):
	"""
    自定义用户验证
    """

	def authenticate(self, request, username=None, password=None, **kwargs):

		# def get_ip():
		#
		# 	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
		#
		# 	if x_forwarded_for:
		# 		ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
		# 		print("realip:", ip)
		# 	else:
		# 		ip = request.META.get('REMOTE_ADDR', None)  # 这里获得代理ip
		# 		print("proxyip:", ip)
		#
		# 		return ip
		#
		# def get_agent():
		# 	print(request.META.get('HTTP_USER_AGENT', None))
		# 	return request.META.get('HTTP_USER_AGENT', None)
		
		try:
			user = User.objects.get(Q(username=username) | Q(user_phone=username))
			print(user)
			
			if user.check_password(password) and self.user_can_authenticate(user):
				
				return user
			else:
				return None
		except Exception as e:
			return None

