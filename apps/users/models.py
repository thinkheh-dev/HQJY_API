from datetime import datetime
import uuid
import os

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from enterprise_info.models import BasicEnterpriseInfo, EnterpriseAuthManuallyReview, EnterpriseCertification

from DjangoUeditor.models import UEditorField


class UserPermissionsName(models.Model):
	"""
	用户权限
	"""
	permission_name = models.CharField(max_length=30, verbose_name="权限名称", help_text="权限名称")
	permission_sn = models.CharField(max_length=20, null=True, blank=True, verbose_name="权限代码",
	                                 help_text="权限代码")
	permission_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="权限描述",
	                                   help_text="权限描述")
	
	class Meta:
		verbose_name = "用户权限"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.permission_name


class UserLabels(models.Model):
	"""
	用户模式
	"""
	label_name = models.CharField(max_length=20, verbose_name="模式名称", help_text="模式名称")
	label_code = models.CharField(max_length=10, default="YHMS001", verbose_name="模式代码", help_text="模式代码")
	label_img = models.ImageField(upload_to="label_img/", blank=True, null=True, verbose_name="用户模式标签图片",
	                              help_text="用户模式标签图片")
	
	class Meta:
		verbose_name = "用户模式"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.label_name


def user_upload_path(instance, filename):
	"""
	文件上传路径拼装类
	:param instance: 文件实例
	:param filename: 文件名
	:return: 拼装后的文件路径
	"""
	User = get_user_model()
	
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
	
	sub_folder = 'user_logo'
	u_name = User.objects.filter(id=instance.id).values()[0]['username']
	sub_folder_sub = ''
	
	if ext.lower() in ["jpg", "png", "gif", "svg", "jpeg"]:
		sub_folder_sub = "avatar"
	if ext.lower() in ["pdf", "docx", "doc", "xlsx", "xls"]:
		raise ValueError("请上传扩展名为：jpg, png, gif, svg, jpeg的图片，不支持其他格式的图片")
	
	return os.path.join(sub_folder, u_name, sub_folder_sub, filename)


class UserInfo(AbstractUser):
	"""
	用户主信息
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
		("红河州", "红河州"),
		("昆明市", "昆明市"),
		("其他地州", "其他地州"),
		("其他省市", "其他省市"),
	)
	
	user_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="用户真实姓名",
	                             help_text="用户真实姓名")
	user_logo = models.ImageField(upload_to=user_upload_path, blank=True, null=True, verbose_name="用户头像",
	                              help_text="用户头像", default="user_logo/default.svg")
	user_sex = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), blank=True, null=True,
	                            verbose_name="性别", help_text="性别")
	user_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="用户手机号",
	                              help_text="用户手机号")
	user_id_card = models.CharField(max_length=18, blank=True, null=True, verbose_name="身份证号",
	                                help_text="身份证号")
	user_birthday = models.DateField(blank=True, null=True, editable=False, verbose_name="用户生日",
	                                 help_text="用户生日")
	QQ_num = models.CharField(max_length=20, blank=True, null=True, verbose_name="QQ号码", help_text="QQ号码")
	wechat_num = models.CharField(max_length=20, blank=True, null=True, verbose_name="微信号", help_text="微信号")
	contact_address = models.CharField(max_length=200, blank=True, null=True, verbose_name="联系地址",
	                                   help_text="联系地址")
	user_email = models.EmailField(blank=True, null=True, verbose_name="电子邮件地址", help_text="电子邮件地址")
	user_to_company = models.OneToOneField(BasicEnterpriseInfo, blank=True, null=True, on_delete=models.SET_NULL,
	                                       related_name="user_to_company", verbose_name="关联的企业",
	                                       help_text="关联的企业")
	eps_auth_manually_review = models.OneToOneField(EnterpriseAuthManuallyReview, blank=True, null=True,
	                                                on_delete=models.SET_NULL, related_name="eps_amr",
	                                                verbose_name="企业认证人工审核关联", help_text="企业认证人工审核关联")
	eps_auth_soc = models.OneToOneField(EnterpriseCertification, blank=True, null=True, on_delete=models.SET_NULL,
	                                    related_name="eps_soc", verbose_name="企业认证证书关联", help_text="企业认证证书关联,请勿修改")
	user_permission_name = models.ForeignKey(UserPermissionsName, null=True, blank=True, on_delete=models.SET_NULL,
	                                         related_name="user_permission_userinfo", verbose_name="关联用户权限",
	                                         help_text="关联用户权限")
	user_home = models.CharField(max_length=10, choices=COUNTY_CHOICES, blank=True, null=True,
	                             verbose_name="用户归属地",
	                             help_text="用户归属地")
	user_labels = models.ManyToManyField(UserLabels, related_name="user_labels_userinfo", blank=True,
	                                     verbose_name="关联用户模式标签", help_text="关联用户模式标签")
	service_provider = models.BooleanField(default=False, verbose_name="是否服务提供商", help_text="是否服务提供商")
	
	# 新增用户字段
	user_introduce = models.TextField(max_length=200, blank=True, null=True, verbose_name="用户自我介绍",
	                                  help_text="用户自我介绍（200字以内）")
	user_important_qualification1 = models.ImageField(upload_to=user_upload_path, blank=True, null=True,
	                                                  verbose_name="用户重要资质一", help_text="您的重要资质")
	user_important_qualification2 = models.ImageField(upload_to=user_upload_path, blank=True, null=True,
	                                                  verbose_name="用户重要资质二", help_text="您的重要资质")
	user_important_qualification3 = models.ImageField(upload_to=user_upload_path, blank=True, null=True,
	                                                  verbose_name="用户重要资质三", help_text="您的重要资质")
	userinfo_flag = models.BooleanField(default=False, verbose_name="是否显示用户信息", help_text="是否显示用户信息")
	
	# 来源于聚合三方手机认证API
	user_phone_type = models.CharField(max_length=20, blank=True, null=True, verbose_name="用户手机运营商",
	                                   help_text="来源于聚合三方手机认证API")
	user_phone_province = models.CharField(max_length=20, blank=True, null=True, verbose_name="用户手机归属省市",
	                                       help_text="来源于聚合三方手机认证API")
	user_phone_city = models.CharField(max_length=30, blank=True, null=True, verbose_name="用户手机归属城市",
	                                   help_text="来源于聚合三方手机认证API")
	
	user_protocol = models.BooleanField(default=False, verbose_name="是否同意用户协议", help_text="是否同意用户协议")
	
	class Meta:
		verbose_name = "用户信息"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.username


class VerifyCode(models.Model):
	"""
	短信验证码
	"""
	
	code = models.CharField(max_length=6, verbose_name="短信验证码", help_text="短信验证码")
	user_phone = models.CharField(max_length=11, verbose_name="用户手机号", help_text="用户手机号")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="验证时间", help_text="验证时间")
	
	class Meta:
		verbose_name = "短信验证码"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.code


class UserProtocol(models.Model):
	"""
	用户协议
	"""
	
	protocol_title = models.CharField(max_length=200, verbose_name="协议标题", help_text="协议标题")
	protocol_subtitle = models.CharField(max_length=200, verbose_name="协议副标题", help_text="协议副标题")
	protocol_content = UEditorField(verbose_name="协议内容", imagePath="user_protocol/images/", width=1000,
	                                height=300, filePath="user_protocol/files/", default='', help_text="协议内容")
	
	class Meta:
		verbose_name = "用户协议"
		verbose_name_plural = verbose_name
