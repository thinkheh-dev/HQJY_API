#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2018-11-14 09:51
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from datetime import datetime, timedelta
import re

from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.http import request

from .models import InfoCategories, WeMediaArticles, PlatformActivity, ActivityRegistration, ActivityRegList, \
	WeMediaArticleFav


#信息分类序列化 -- 开始
class InfoCategoriesSerializers5(serializers.ModelSerializer):
	
	class Meta:
		model = InfoCategories
		fields = "__all__"
		
		
class InfoCategoriesSerializers4(serializers.ModelSerializer):
	
	sub_classification = InfoCategoriesSerializers5(many=True)
	
	class Meta:
		model = InfoCategories
		fields = "__all__"


class InfoCategoriesSerializers3(serializers.ModelSerializer):
	
	sub_classification = InfoCategoriesSerializers4(many=True)
	
	class Meta:
		model = InfoCategories
		fields = "__all__"
		
		
class InfoCategoriesSerializers2(serializers.ModelSerializer):
	
	sub_classification = InfoCategoriesSerializers3(many=True)
	
	class Meta:
		model = InfoCategories
		fields = "__all__"
		
	
class InfoCategoriesSerializers(serializers.ModelSerializer):
	
	sub_classification = InfoCategoriesSerializers2(many=True)
	
	class Meta:
		model = InfoCategories
		fields = "__all__"
		
#信息分类序列化 -- 结束


class WeMediaArticlesSerializers(serializers.ModelSerializer):
	"""
	平台自媒体文章序列化
	"""
	info_categories = InfoCategoriesSerializers(many=True)
	
	class Meta:
		model = WeMediaArticles
		fields = "__all__"
		

class WeMediaArticlesCreateSerializers(serializers.ModelSerializer):
	"""
	平台自媒体文章编辑序列化
	"""
	
	title = serializers.CharField(required=True, label="文章标题", max_length=100, min_length=5,
	                              error_messages=({
													"blank": "文章标题不能为空",
													"required": "文章标题必须填写",
													"min_length": "文章标题太短",
		                                            "max_length": "文章标题太长"}))
	subtitle = serializers.CharField(required=False, label="文章副标题", allow_blank=True, allow_null=True, max_length=20,
	                                 min_length=2, error_messages=({"blank": "文章副标题不能为空",
	                                                                "required": "文章副标题必须填写",
	                                                                "min_length": "文章副标题太短",
	                                                                "max_length": "文章副标题太长"}))
	#不显示给用户的字段
	publish_time = serializers.DateTimeField(read_only=True)
	read_nums = serializers.IntegerField(read_only=True)
	fav_nums = serializers.IntegerField(read_only=True)
	
	class Meta:
		model = WeMediaArticles
		fields = "__all__"

class WeMediaArticleFavDetailSerializers(serializers.ModelSerializer):
	"""
	自媒体收藏详情序列化
	"""
	wemedia_article = WeMediaArticlesSerializers(many=False)
	
	class Meta:
		model = WeMediaArticleFav
		fields = "__all__"
		

class WeMediaArticleFavSerializers(serializers.Serializer):
	"""
	平台自媒体收藏序列化
	"""
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	wemedia_article = serializers.PrimaryKeyRelatedField(required=True, queryset=WeMediaArticles.objects.all())
	
	def create(self, validated_data):
		"""
		平台自媒体收藏create方法
		:param validated_data:
		:return:
		"""
		user = self.context['request'].user
		# print(user)
		
		wemedia_article = validated_data['wemedia_article']
		
		existed = WeMediaArticleFav.objects.filter(user_info=user, wemedia_article=wemedia_article)
		
		if existed:
			existed = existed[0]
			raise serializers.ValidationError(detail={"error_message": "该文章您已经收藏过！", "error_code":
				status.HTTP_400_BAD_REQUEST, "existed": existed})
		else:
			existed = WeMediaArticleFav.objects.create(**validated_data)
		
		return existed
