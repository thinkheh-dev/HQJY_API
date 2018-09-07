from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户模型


class UserPermissions(models.Model):
	"""
	用户权限
	"""
	permission_name = models.CharField(max_length=30, verbose_name="权限名称")
	permission_sn = models.CharField(max_length=20, verbose_name="权限代码")
	permission_desc = models.CharField(max_length=200, verbose_name="权限描述")
	
	class Meta:
		verbose_name = "用户权限"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.permission_name
	

class UserLabels(models.Model):
	"""
	用户模式
	"""
	label_name = models.CharField(max_length=20, verbose_name="模式名称")
	
	class Meta:
		verbose_name = "用户模式"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.label_name
	

class UserProfile(AbstractUser):
	"""
	用户信息
	"""
	user_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="用户姓名")
	user_id_card = models.CharField(max_length=18, blank=True, null=True, verbose_name="身份证号")
	user_birthday = models.DateField(verbose_name="用户生日")
	user_sex = models.CharField(choices=(("male", "男"), ("female", "女")), default="female", verbose_name="性别")
	user_phone = models.CharField(max_length=11, unique=True, verbose_name="用户手机号")
	user_email = models.EmailField(blank=True, null=True, verbose_name="电子邮件地址")
	QQ_num = models.CharField(max_length=20, blank=True, null=True, verbose_name="QQ号码")
	wechat_num = models.CharField(max_length=20, blank=True, null=True, verbose_name="微信号")
	contact_address = models.CharField(max_length=200, blank=True, null=True, verbose_name="联系地址")
	user_real_name_authentication = models.BooleanField(default=False, verbose_name="实名认证标志")
	user_ip = models.IPAddressField(blank=True, null=True, verbose_name="最后一次登录IP地址")
	user_browser = models.CharField(max_length=200, blank=True, null=True, verbose_name="最一次登录用的浏览器")
	user_to_company = models.ForeignKey(BasicEnterpriseInfo, on_delete=models.CASCADE, related_name="user_to_company", verbose_name="关联的企业")
	enterprise_type_first = models.ForeignKey(EnterpriseTypeFirst, on_delete=models.CASCADE, related_name="enterprise_type_first", verbose_name="行业一级分类")
	enterprise_type_second = models.ForeignKey(EnterpriseTypeSecond, on_delete=models.CASCADE, related_name="enterprise_type_second", verbose_name="行业二级分类")
	user_permissions = models.ForeignKey(UserPermissions, on_delete=models.CASCADE, related_name="user_permissions", verbose_name="关联用户权限")
	user_labels = models.ForeignKey(UserLabels, on_delete=models.CASCADE, related_name="user_labels", verbose_name="关联用户模式标签")
	disable_flag = models.CharField(choices=(("ENABLE", "启用"), ("DISABLE", "禁用")), default="ENABLE", verbose_name="用户禁用标志")
	
	class Meta:
		verbose_name = "用户信息"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.user_name


class VerifyCode(models.Model):
	"""
	短信验证码
	"""
	code = models.CharField(max_length=10, verbose_name="短信验证码")
	user_phone = models.CharField(max_length=11, verbose_name="用户手机号")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="验证时间")
	
	class Meta:
		verbose_name = "短信验证码"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.code