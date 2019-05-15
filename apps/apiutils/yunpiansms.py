#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2018-11-14 10:29
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : YunPianSms.py
# @software: PyCharm

import json
import requests
import urllib

class YunPianSms(object):
	"""
	原定使用云片网短信，后修改为聚合网短信，函数名称不做修改
	聚合网短信接口
	"""
	
	def __init__(self, api_key):
		self.api_key = api_key
		self.single_send_url = "http://v.juhe.cn/sms/send"
	
	def send_sms(self, code, user_phone):
		tpl_id = 157783
		tpl_value = "#code#={code}".format(code=code)
		params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
				 (self.api_key, user_phone, tpl_id, urllib.request.quote(tpl_value))  # 组合参数

		wp = urllib.request.urlopen(self.single_send_url + "?" + params)
		content = wp.read()  # 获取接口返回内容
		re_dict = json.loads(content)
		return re_dict
	
	# if __name__ == "__main__":
	# 	yun_pian = YunPianSms("")
	# 	yun_pian.send_sms("2018", "")

class YunPianSmsSend(object):
	"""
	完成企业认证人工审核-云片网短信发送接口
	"""

	def __init__(self, api_key):
		self.api_key = api_key
		self.success_value = 158221
		self.fail_value = 158222
		self.single_send_url = "http://v.juhe.cn/sms/send"

	def send_success_sms(self, user_phone):
		tpl_id = self.success_value
		tpl_value = ""
		params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
				 (self.api_key, user_phone, tpl_id, tpl_value)  # 组合参数

		wp = urllib.request.urlopen(self.single_send_url + "?" + params)
		content = wp.read()  # 获取接口返回内容
		re_dict = json.loads(content)
		return re_dict

	def send_fail_sms(self, user_phone):
		tpl_id = self.fail_value
		tpl_value = ""
		params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
				 (self.api_key, user_phone, tpl_id, tpl_value)  # 组合参数

		wp = urllib.request.urlopen(self.single_send_url + "?" + params)
		content = wp.read()  # 获取接口返回内容
		re_dict = json.loads(content)
		return re_dict
