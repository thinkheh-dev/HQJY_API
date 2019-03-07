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
	print(user.user_permission_name)
	return {
		'token': token,
		'user_id': user.id,
		'username': user.username,
		'user_permission_name': user.user_permission_name.id
	}
	
class UserLoginThrottle(SimpleRateThrottle):
	"""
	限制用户登录60s尝试次数
	"""
	scope = 'user_login_scope'  # 显示频率的Key,在配置文件里需要有个跟这个同名
	
	def get_cache_key(self, request, view):
		return self.get_ident(request)  # 获取请求IP



class CustomBackend(ModelBackend):
	"""
    自定义用户验证
    """
	
	throttle_classes = [UserLoginThrottle, ]
	
	def throttled(self, request, wait):
		"""
		访问次数被限制时，定制错误信息
		"""
		
		class Throttled(exceptions.Throttled):
			default_detail = '请求被限制.'
			extra_detail_singular = '请 {wait} 秒之后再重试.'
			extra_detail_plural = '请 {wait} 秒之后再重试.'
		
		raise Throttled(wait)

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
