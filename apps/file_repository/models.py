from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid
import os


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
	
	sub_folder = 'file_repository'
	sub_folder_sub = 'file_repository_other'
	
	if ext.lower() in ["jpg", "png", "gif", "svg", "jpeg"]:
		sub_folder_sub = "file_repository_avatar"
	if ext.lower() in ["pdf", "docx", "doc", "xlsx", "xls"]:
		sub_folder_sub = "file_repository_document"
		
		
	return os.path.join(sub_folder, sub_folder_sub, filename)

#此方法已弃用
def user_authfile_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
	# return the whole path to the file
	return os.path.join("user_auth_file", instance.username, filename)



class AttachLibraryManager(models.Model):
	"""
	附件库管理
	"""
	library_name = models.CharField(max_length=200, verbose_name="附件库名称", help_text="附件库名称")
	# attach_resource = models.ForeignKey(AttachResources, on_delete=models.CASCADE, related_name="attach_lib",
	#                                     verbose_name="附件资源", help_text="附件资源")
	attach_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="附件上传者", help_text="附件上传者",
	                                  related_name="attach_to_author")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "附件库管理"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.library_name


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
		(7, "普通文件")
	)
	
	attach_name = models.CharField(max_length=200, verbose_name="附件名称", help_text="附件名称")
	attach_type = models.IntegerField(choices=ATTACH_TYPE, default=7, verbose_name="附件类型", help_text="附件类型")
	attach_desc = models.TextField(blank=True, null=True, verbose_name="附件用途描述", help_text="附件用途描述")
	attach_file = models.FileField(upload_to=user_upload_path, verbose_name="用户附件", help_text="用户附件")
	attach_library_manager = models.ForeignKey(AttachLibraryManager, on_delete=models.CASCADE,
	                                           related_name="attach_lib_man", verbose_name="附件资源", help_text="附件资源")
	
	class Meta:
		verbose_name = "附件资源"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.attach_name
