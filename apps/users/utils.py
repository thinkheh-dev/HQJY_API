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

def jwt_response_payload_handler(token, user=None, request=None):
	"""为返回的结果添加用户相关信息"""
	
	return {
		'token': token,
		'user_id': user.id,
		'username': user.username
	}

User = get_user_model()

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
			
			# # 获取用户的浏览器及IP地址
			# agent = get_agent()
			# print(agent)
			#
			# user_ip_now = get_ip()
			# print(user_ip_now)
			
			if user.check_password(password) and self.user_can_authenticate(user):
				
				# # 保存用户ip地址及浏览器
				# user.user_ip = user_ip_now
				# user.user_browser = agent
				# user.save()
				
				return user
			else:
				return None
		except Exception as e:
			return None

