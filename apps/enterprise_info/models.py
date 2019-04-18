from django.db import models
from datetime import datetime
from rest_framework.response import Response

import uuid
import os


class EnterpriseLabel(models.Model):
	"""
	企业标签
	"""
	LEVEL_CHOICE = (
		(1,'普通'),
		(2,'高级'),
		(3,'超级'),
	)
	name = models.CharField(max_length=50, blank=True, null=True, verbose_name="企业标签名称",
	                        help_text="企业标签名称")
	label_ico = models.FileField(verbose_name="标签图片", upload_to="en_label_ico/", blank=True, null=True,
	                             help_text="企业标签图片")
	level = models.IntegerField(default=1, choices=LEVEL_CHOICE, blank=True, null=True, verbose_name="企业标签级别", \
	                                                                                               help_text="标签级别")
	class Meta:
		verbose_name = "企业标签管理"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name
	


class EnterpriseTypeLevel(models.Model):
	"""
	企业分类级别
	"""
	name = models.CharField(max_length=50, verbose_name="级别名称", help_text="级别名称")
	level = models.IntegerField(editable=True, verbose_name="分类级别", help_text="只可填写1-5之间的数字")
	
	class Meta:
		verbose_name = "企业分类级别管理"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class EnterpriseType(models.Model):
	"""
	企业分类
	"""
	name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
	code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
	desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
	category_type = models.ForeignKey(EnterpriseTypeLevel, on_delete=models.CASCADE, verbose_name="类目级别",
	                                  help_text="类目级别")
	parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父类别",
	                                    related_name="sub_type", on_delete=models.CASCADE)
	#is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "企业分类管理"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name


def auth_review_path(instance, filename):
	"""
	文件上传路径拼装类
	:param instance: 文 件实例
	:param filename: 文件名
	:return: 拼装后的文件路径
	"""
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
	
	sub_folder = 'enterprise_auth_file'
	u_name = instance.enterprise_name
	
	if ext.lower() in ["jpg", "jpeg", "png"]:
		return os.path.join(sub_folder, u_name, filename)
	else:
		return Response({"error_message": "请上传jpg/jpeg/png格式的图片！"})
	

class EnterpriseReviewFile(models.Model):
	"""
	企业认证申请文件模板
	"""
	eps_review_template_file = models.FileField(upload_to="eps_review_template/", verbose_name="企业认证申请文件模板",
	                                       help_text="企业认证申请文件模板")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="文件上传时间")
	
	class Meta:
		verbose_name = "企业认证申请文件模板上传"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return "模板-{}".format(self.eps_review_template_file.name)
	

class EnterpriseAuthManuallyReview(models.Model):
	"""
	企业认证人工审核
	"""
	
	STATUS = (
		(1, "审核成功"),
		(2, "审核未通过"),
		(3, "待审核")
	)
	
	user_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="被审核用户id", help_text="被审核用户id")
	enterprise_name = models.CharField(max_length=50, verbose_name="企业名称", help_text="企业名称")
	enterprise_oper_name = models.CharField(max_length=20, verbose_name="企业法人姓名", help_text="企业法人姓名")
	enterprise_oper_idcard = models.ImageField(upload_to=auth_review_path, blank=True, verbose_name="企业法人身份证正面照片",
	                                           help_text="企业法人身份证正面照片")
	enterprise_license = models.ImageField(upload_to=auth_review_path, verbose_name="企业营业执照正面照片", blank=True,
	                                       help_text="企业营业执照正面照片")
	enterprise_review = models.ImageField(upload_to=auth_review_path, verbose_name="企业认证申请扫描件",
	                                      blank=True, help_text="企业认证申请扫描件")
	apply_audit_status = models.IntegerField(choices=STATUS, default=3, verbose_name="申请审核状态", help_text="申请审核状态")
	auth_failure_reason = models.TextField(max_length=200, blank=True, null=True, verbose_name="审核不通过的原因",
	                                       help_text="如果审核不通过，请填写原因")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="申请提交时间", help_text="申请提交时间")
	update_time = models.DateTimeField(auto_now=True, verbose_name="审核更新时间", help_text="审核更新时间")
	
	class Meta:
		verbose_name = "企业认证人工审核"
		verbose_name_plural = verbose_name
		ordering = ['-add_time', ]
		unique_together = (('user_id', 'enterprise_name'))
	
	def __str__(self):
		return "{} -- 企业认证信息".format(self.enterprise_name)


def eps_info_path(instance, filename):
	"""
	文件上传路径拼装类
	:param instance: 文 件实例
	:param filename: 文件名
	:return: 拼装后的文件路径
	"""
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
	
	sub_folder = 'eps_info_file'
	u_name = instance.name
	
	if ext.lower() in ["jpg", "jpeg", "png"]:
		return os.path.join(sub_folder, u_name, filename)
	else:
		return Response({"error_message": "请上传jpg/jpeg/png格式的图片！"})


class BasicEnterpriseInfo(models.Model):
	"""
	企业基础信息
	"""
	COUNTY_CHOICES = (
		("个旧市", "个旧市"),
		("开远市", "开远市"),
		("蒙自市", "蒙自市"),
		("建水县", "建水县"),
		("石屏县", "石屏县"),
		("弥勒市", "弥勒市"),
		("泸西县", "泸西县"),
		("红河县", "红河县"),
		("元阳县", "元阳县"),
		("绿春县", "绿春县"),
		("屏边县", "屏边县"),
		("金平县", "金平县"),
		("河口县", "河口县"),
		("昆明市", "昆明市"),
		("其他地州", "其他地州"),
		("其他省市", "其他省市"),
	)
	
	name = models.CharField(max_length=50, blank=True, null=True, verbose_name="企业名称", help_text="企业名称")
	credit_no = models.CharField(max_length=18, blank=True, null=True, verbose_name="统一社会信用代码", help_text="统一社会信用代码")
	oper_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="企业法人", help_text="企业法人")
	econ_kind = models.CharField(max_length=20, blank=True, null=True, verbose_name="公司类型", help_text="公司类型")
	regist_capi = models.IntegerField(blank=True, null=True, verbose_name="注册资金（万元）", help_text="注册资金（万元）")
	scope = models.CharField(max_length=255, blank=True, null=True, verbose_name="经营范围", help_text="经营范围")
	status = models.CharField(max_length=20, choices=(("开业", "开业"), ("注销", "注销")), default="开业",
	                          verbose_name="公司状态(开业/注销)", help_text="公司状态(开业/注销)")
	address = models.CharField(max_length=200, blank=True, null=True, verbose_name="企业地址", help_text="企业地址")
	start_date = models.DateField(blank=True, null=True, verbose_name="成立日期", help_text="成立日期")
	term_start = models.DateField(blank=True, null=True, verbose_name="营业开始日期", help_text="营业开始日期")
	term_end = models.DateField(blank=True, null=True, verbose_name="营业结束日期", help_text="营业结束日期")
	belong_org = models.CharField(max_length=50, blank=True, null=True, verbose_name="登记机关", help_text="登记机关")
	company_area = models.CharField(max_length=20, choices=COUNTY_CHOICES, default="蒙自市", verbose_name="企业归属地",
	                                help_text="企业归属地")
	enterprise_type = models.ForeignKey(EnterpriseType, on_delete=models.CASCADE, related_name="entype_first",
	                                    blank=True, null=True, verbose_name="企业分类", help_text="企业分类")
	enterprise_label = models.ForeignKey(EnterpriseLabel, on_delete=models.CASCADE, related_name="enlabel",
	                                     blank=True, null=True, verbose_name="企业标签", help_text="企业标签")
	oper_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="企业联系人", help_text="企业联系人")
	scan_of_company_license = models.ImageField(upload_to=eps_info_path, blank=True, null=True,
	                                            verbose_name="营业执照正面清晰扫描件", help_text="营业执照正面清晰扫描件")
	scan_of_id_card = models.ImageField(upload_to=eps_info_path, blank=True, null=True, verbose_name="法人身份清晰彩色扫描件",
	                                    help_text="法人身份清晰彩色扫描件")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="企业信息创建时间", help_text="企业信息创建时间")
	
	class Meta:
		verbose_name = "企业基础信息"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name


