#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019/8/20 下午4:33
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : service_signal.py
# @software: PyCharm

from django.dispatch import Signal

# 自定义信号
signal_service_re = Signal(providing_args=["signal_re"])
# 'signal_service_re'是信号的名称，后面的providing_args是传参给接收者的，也就是这个信号的接
# 收者可以调用到"signal_re"参数，就算是'None'也可以
