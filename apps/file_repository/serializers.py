#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-03-15 09:44
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import AttachLibraryManager, AttachResources, TinyMCEAttach
from user_operation.models import OrderServiceDetail
from user_operation.serializers import OrderServiceDetailSerializers, OrderInfoSerializers

User = get_user_model()

class AttachLibraryManagerSerializers(serializers.ModelSerializer):
	"""
	资料库管理序列化
	"""
	class Meta:
		model = AttachLibraryManager
		fields = ['library_name', ]


class AttachResourcesSerializers(serializers.ModelSerializer):
	"""
	附件资源序列化
	"""
	order_info = OrderServiceDetailSerializers(many=True)
	attach_author = serializers.HiddenField(default=serializers.CurrentUserDefault())
	attach_library_manager = AttachLibraryManagerSerializers()
	
	class Meta:
		model = AttachResources
		fields = "__all__"


class AttachResourceListSerializers(serializers.Serializer):
	
	image_files = serializers.ListField(
		child=serializers.ImageField(max_length=100000,
		                            allow_empty_file=False,
		                            use_url=True), write_only=True
	)
	
	attach_images = serializers.ListField(
		child=serializers.CharField(max_length=1000), read_only=True
	)
	
	order_info = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, allow_empty=True,
	                                                queryset=OrderServiceDetail.objects.all())
	
	def create(self, validated_data):
		
		image_files = validated_data.get('image_files')
		order_info_id = validated_data.get('order_info')
		
		images = []
		
		for index, url in enumerate(image_files):
			image = AttachResources.objects.create(attach_file=url, attach_author=User.objects.get(id=self.context[
				'request'].user.id), attach_type=8, attach_library_manager=8, order_info=order_info_id)
			attach_image = AttachResourcesSerializers(image, context=self.context)
			images.append(attach_image.data['url'])
			
		OrderServiceDetail.objects.filter(order_info=order_info_id).update(allow_upload_file=False)
		return {'attach_images': images}


class TinyMCEAttachSerializers(serializers.ModelSerializer):
	"""
	TinyMCE富文本编辑器图片序列化
	"""
	user_info = serializers.HiddenField(default=serializers.CurrentUserDefault())


	class Meta:
		model = TinyMCEAttach
		fields = ('user_info', 'url')


class TinyMCEAttachListSerializers(serializers.Serializer):
	"""
	TinyMCE富文本编辑器图片列表序列化
	"""
	imgs = serializers.ListField(child=serializers.ImageField(max_length=100000,
								 allow_empty_file=True,
								 allow_null=True, use_url=True),
								 write_only=True,
								 allow_empty=True,
								 allow_null=True)

	def create(self, validated_data):
		image_files = validated_data.get('imgs')

		images = []

		for index, url in enumerate(image_files):
			image = AttachResources.objects.create(url=url, user_info=User.objects.get(id=self.context['request'].user.id))
			tiny_attach = TinyMCEAttachSerializers(image, context=self.context)
			images.append(tiny_attach.data['url'])

		return {'tiny_imgs': images}




		
