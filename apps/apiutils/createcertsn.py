#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019/6/13 下午3:13
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : createcertsn.py
# @software: PyCharm

import uuid
import datetime


class EnterpriseAuthCertification(object):
	
	def __init__(self, enterprise_code):
		self.enterprise_code = enterprise_code
	
	# 创建企业认证证书编号
	def create_cert_sn(self):
		header = "REHSOC"
		cert_start = datetime.date.today().strftime('%Y%m%d')
		cert_end = (datetime.date.today() + datetime.timedelta(days=366)).strftime('%Y%m%d')
		uuid_num = uuid.uuid4().hex[:8]
		en_code = self.enterprise_code[15:18].lower()
	
		sn_str = header + cert_start + cert_end + uuid_num + en_code
		return sn_str

