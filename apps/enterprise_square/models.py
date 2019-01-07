from django.db import models

from datetime import datetime
from django.utils import timezone
import random

from DjangoUeditor.models import UEditorField
from django.db import models

from enterprise_info.models import BasicEnterpriseInfo


class EnterpriseSquareClassification(models.Model):
	"""
	企业广场分类
	"""
	CLASSIFICATION = (
		(1, "一级类别"),
		(2, "二级类别"),
		(3, "三级类别"),
		(4, "四级类别"),
		(5, "五级类别"),
	)
	
	name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
	code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
	desc = models.TextField(default="", help_text="类别描述", verbose_name="类别描述")
	category_type = models.IntegerField(choices=CLASSIFICATION, verbose_name="类目级别", help_text="类目级别")
	parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
	                                    related_name="sub_classification", on_delete=models.CASCADE)
	is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "企业广场分类管理"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name


class EnterpriseSquareManager(models.Model):
	"""
	企业广场管理
	"""
	enterprise_name = models.ForeignKey(BasicEnterpriseInfo, null=True, blank=True, help_text="企业名称",
	                                    related_name="en_name", on_delete=models.CASCADE)
	enterprise_image = models.ImageField(upload_to="enp_img/", verbose_name="封面图片上传", null=True, blank=True)
	enterprise_video = models.FileField(upload_to="enp_video/", verbose_name="视频文件上传", null=True, blank=True)
	ens_content_title = models.CharField(max_length=200, null=True, blank=True, verbose_name="企业展示内容标题")
	ens_content = UEditorField(verbose_name="企业展示详细内容", imagePath="enterprise_square/images/", width=1000,
	                                            height=300, filePath="enterprise_square/files/", default='')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	
	class Meta:
		verbose_name = "企业广场管理"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.enterprise_name
	



