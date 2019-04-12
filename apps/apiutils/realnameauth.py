#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-04-02 20:53
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : realnameauth.py
# @software: PyCharm

import json
import requests

class RealNameAuthInterface(object):
	"""
	实名认证第三方接口
	"""
	
	def __init__(self, api_key):
		self.api_key = api_key
		self.send_url = ""
	
	def send_auth(self, user_phone, realname, idcard):
		parmas = {
			
			"key": self.api_key,
			"mobile": user_phone,
			"realname": realname,
			"idcard": idcard
			
		}
		
		return_result = {
            "reason": "查询成功",
            "result": {
	            "realname": realname,
	            "mobile": user_phone,
	            "idcard": idcard,
	            "res": 1, #/*匹配结果：1匹配 2不匹配*/
	            "resmsg": "三要素身份验证一致,", #/*说明,res为1时返回三要素身份验证一致,res为2时返回三要素身份验证不一致*/
	            "type": "移动", #/*手机运营商,输入参数type为1时返回*/
	            "orderid":"J201712251904163782Ay", #/*聚合订单号,输入参数showid为1时返回*/
	            "province":"云南省红河州", #/*归属地省*/
	            "city" : "蒙自市", #/**归属地城市*/
                "rescode":"11", #/*输入detail为1时返回匹配详情码,11:匹配,21:姓名不匹配,22:身份证不匹配,
                #23:姓名身份证均不匹配,33:身份证和姓名不一致,24:不匹配,具体要素不匹配未知*/
		    },
		    "error_code": 0
}
		
		# response = requests.post(self.single_send_url, data=parmas)
		#re_dict = json.loads(return_result)
		return return_result
