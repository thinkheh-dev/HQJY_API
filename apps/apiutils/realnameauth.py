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
import urllib

class RealNameAuthInterface(object):
	"""
	实名认证第三方接口
	"""
	
	def __init__(self, api_key):
		self.api_key = api_key
		self.send_url = "http://v.juhe.cn/telecom/query"
	
	def send_auth(self, user_phone, realname, idcard):

		#定义实名认证所需的参数字典
		params = {}

		#根据参数说明，按需添加所需的参数
		params['key'] = self.api_key		#必填
		params['realname'] = realname	  	#必填
		params['idcard'] = idcard			#必填
		params['mobile'] = user_phone		#必填
		params['detail'] = 1				#非必填
		params['type'] = 1					#非必填 运营商
		params['province'] = 1				#非必填 归属地省
		params['city'] = 1					#非必填 归属地城市

		#拼接实名认证请求url
		url = self.send_url + "?" + urllib.parse.urlencode(params)

		#通过urllib发送请求
		request = urllib.request.Request(url)
		result = urllib.request.urlopen(request)

		#接口返回数据
		jsonarr = json.loads(result.read().decode('utf-8'))

		return jsonarr
