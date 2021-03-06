from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework.response import Response
import uuid
import os

from user_operation.models import OrderServiceDetail

User = get_user_model()


def user_upload_path(instance, filename):
	"""
	文件上传路径拼装类
	:param instance: 文件实例
	:param filename: 文件名
	:return: 拼装后的文件路径
	"""
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
	
	sub_folder = 'file_repository %s '
	sub_folder_sub = ''
	
	if ext.lower() in ["jpg", "png", "gif", "svg", "jpeg"]:
		sub_folder_sub = "file_repository_avatar"
	else:
		return Response({"您上传的文件{}不是图片类型，请重新上传！", filename})
	
	return os.path.join(sub_folder, instance.username, filename)


# 此方法已弃用
def user_authfile_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
	# return the whole path to the file
	return os.path.join("user_auth_file", instance.username, filename)


class AttachLibraryManager(models.Model):
	"""
	附件库管理
	"""
	LIB_NAME = (
		(1, "公司认证库"),
		(2, "政策文件库"),
		(3, "平台保密文件库"),
		(4, "平台普通文件库"),
		(5, "个人证件库"),
		(6, "公司证件库"),
		(7, "普通文件库"),
		(8, "合同文件库"),
		(9, "其他文件库")
	)
	library_name = models.IntegerField(choices=LIB_NAME, default=7, verbose_name="附件库名称", help_text="附件库名称")
	
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "附件库管理"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return str(self.library_name)


class AttachResources(models.Model):
	"""
	附件资源类
	"""
	ATTACH_TYPE = (
		(1, "认证-申请"),
		(2, "政策文件"),
		(3, "平台保密文件"),
		(4, "平台普通文件"),
		(5, "个人证件"),
		(6, "公司证件"),
		(7, "普通文件"),
		(8, "合同文件"),
		(9, "其他文件")
	)
	
	attach_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="附件上传者", help_text="附件上传者",
									  related_name="attach_to_author")
	attach_type = models.IntegerField(choices=ATTACH_TYPE, default=7, verbose_name="附件类型", help_text="附件类型")
	attach_file = models.ImageField(upload_to=user_upload_path, verbose_name="用户附件", help_text="用户附件")
	attach_library_manager = models.ForeignKey(AttachLibraryManager, on_delete=models.CASCADE,
											   related_name="attach_lib_man", verbose_name="附件资源", help_text="附件资源")
	order_info = models.ForeignKey(OrderServiceDetail, on_delete=models.CASCADE, blank=True, null=True,
	                               verbose_name="关联的订单外键", help_text="关联的订单外键id")
	class Meta:
		verbose_name = "附件资源"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return str(self.attach_library_manager.library_name)


class TinyMCEAttach(models.Model):
	"""
	富文本编辑器TinyMCE图片上传模型-支持多文件
	"""
	user_info = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="图片上传者", help_text="图片上传者", related_name="tinymce_author")
	url = models.ImageField(upload_to=user_upload_path, null=True, blank=True, verbose_name="图片url", help_text="图片url")

	class Meta:
		verbose_name = "TinyMCE图片上传"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.url
