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
			"text": "【红企家园】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
		}
		
		response = requests.post(self.single_send_url, data=parmas)
		re_dict = json.loads(response.text)
		return re_dict
	
	if __name__ == "__main__":
		yun_pian = YunPianSms("")
		yun_pian.send_sms("2018", "")
		
		