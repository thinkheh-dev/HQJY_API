#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019/12/11 上午10:42
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : search_indexes.py
# @software: PyCharm

from haystack import indexes
from .models import DefaultServices, FinancingServices


class DefaultServicesIndex(indexes.SearchIndex, indexes.Indexable):
	"""
	建立普适服务产品索引
	"""
	
	text = indexes.CharField(document=True, use_template=True)
	service_sn = indexes.CharField(model_attr="service_sn")
	service_belong_to_company = indexes.CharField(model_attr="service_belong_to_company")
	service_name = indexes.CharField(model_attr="service_name")
	service_describe = indexes.CharField(model_attr="service_describe")
	service_detailed_description = indexes.CharField(model_attr="service_detailed_description")
	
	def get_model(self):
		return DefaultServices
	
	def index_queryset(self, using=None):
		return self.get_model().objects.filter(is_shelf=True)


class FinancingServicesIndex(indexes.SearchIndex, indexes.Indexable):
	"""
	建立金融服务产品索引
	"""
	
	text = indexes.CharField(document=True, use_template=True)
	service_sn = indexes.CharField(model_attr="service_sn")
	service_belong_to_company = indexes.CharField(model_attr="service_belong_to_company")
	service_name = indexes.CharField(model_attr="service_name")
	service_describe = indexes.CharField(model_attr="service_describe")
	service_detailed_description = indexes.CharField(model_attr="service_detailed_description")
	
	def get_model(self):
		return FinancingServices
	
	def index_queryset(self, using=None):
		return self.get_model().objects.filter(is_shelf=True)
