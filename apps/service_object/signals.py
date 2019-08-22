#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019/8/20 下午3:14
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : signals.py
# @software: PyCharm

from .models import DefaultServices
from service_signal import signal_service_re


def browse_nums_signal(sender, signal_re, **kwargs):
	print("接受到了 {} 信号,开始计数!".format(signal_re))
	print("需要增加浏览次数的产品编号是: {}".format(sender.service_sn))
	service_clicks_num = DefaultServices.objects.get(service_sn=sender.service_sn).service_clicks
	print("计数前的浏览次数是: {}".format(service_clicks_num))
	service_clicks_num += 1
	print("计数后的浏览次数是: {}".format(service_clicks_num))
	DefaultServices.objects.filter(service_sn=sender.service_sn).update(service_clicks=service_clicks_num)


# 为自定义信号创建链接
signal_service_re.connect(browse_nums_signal)
