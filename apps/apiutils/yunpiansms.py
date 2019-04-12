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

class YunPianSms(object):
	"""
	云片网短信接口
	"""
	
	def __init__(self, api_key):
		self.api_key = api_key
		self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"
	
	def send_sms(self, code, user_phone):
		parmas = {
			"apikey": self.api_key,
			"mobile": user_phone,
			#"text": "【红企家园】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
			"text": "【姚运旭】测试验证码是{code}".format(code=code)
		}
		
		response = requests.post(self.single_send_url, data=parmas)
		re_dict = json.loads(response.text)
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
		self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"
	
	def send_sms(self, username, company_name, success, user_phone):
		parmas = {
			"apikey": self.api_key,
			"mobile": user_phone,
			# "text": "【姚运旭】尊敬的{username}您提交的{company_name}企业认证审核{success},请登录红企家园继续操作！".format(username=username,
			#                                                                                   company_name=company_name, success=success)
			"text": "【姚运旭】{username}{company_name}{success}".format(username=username,company_name=company_name,success=success)
		}
		
		response = requests.post(self.single_send_url, data=parmas)
		re_dict = json.loads(response.text)
		return re_dict
