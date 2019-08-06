from django.db import models
from datetime import datetime

# 页面配置模型

# class HomeNav(models.Model):
# 	"""
# 	主页导航
# 	"""
# 	nav_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="导航名称", help_text="导航名称")
# 	nav_image = models.ImageField(upload_to="home_nav/", blank=True, null=True, verbose_name="导航图片", help_text="导航图片")
# 	nav_link = models.URLField(verbose_name="导航链接", blank=True, null=True, help_text="导航链接")
#
# 	class Meta:
# 		verbose_name = "主页导航"
# 		verbose_name_plural = verbose_name
#
# 	def __str__(self):
# 		return self.nav_name
	
# class HomeBackground(models.Model):
# 	"""
# 	主页页头背景图
# 	"""
# 	img_default = models.ImageField(upload_to="home_back/", blank=True, null=True, verbose_name="默认图片", help_text="默认图片")
# 	img_upload = models.ImageField(upload_to="home_back_upload/", blank=True, null=True, verbose_name="自定义图片上传", help_text="自定义图片上传")
# 	img_url = models.URLField(verbose_name="图片地址", blank=True, null=True, help_text="图片地址")
#
# 	class Meta:
# 		verbose_name = "主页页头背景图"
# 		verbose_name_plural = verbose_name


class WebLogo(models.Model):
	"""
	网站标志
	"""
	img_logo = models.ImageField(upload_to="web_logo/", blank=True, null=True, verbose_name="网站logo图片", help_text="网站logo图片")
	img_url = models.URLField(verbose_name="图片地址", blank=True, null=True, help_text="图片地址")
	img_enable = models.BooleanField(default=False, verbose_name="是否启用该LOGO", help_text="是否启用该LOGO")
	
	class Meta:
		verbose_name = "网站LOGO"
		verbose_name_plural = verbose_name


class WebName(models.Model):
	"""
	网站名称
	"""
	web_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="网站名称", help_text="网站名称")
	name_display = models.BooleanField(default=False, verbose_name="是否显示名称", help_text="是否显示名称")
	
	class Meta:
		verbose_name = "网站名称"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.web_name


class ADConfig(models.Model):
	"""
	广告配置
	"""
	ad_img = models.ImageField(upload_to="ad_img/", blank=True, null=True, verbose_name="广告图片", help_text="广告图片")
	img_description = models.CharField(max_length=200, blank=True, null=True, verbose_name="图片描述", help_text="图片描述")
	img_index = models.IntegerField(default=0, editable=True, verbose_name="排序", help_text="排序")
	ad_index = models.IntegerField(default=1, editable=True, verbose_name="广告级别", help_text="广告级别")
	
	class Meta:
		verbose_name = "广告配置"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.img_description


class WebFooterLink(models.Model):
	"""
	网站页脚友情链接
	"""
	link_logo = models.ImageField(upload_to="link_img/", blank=True, null=True, verbose_name="友情链接图片",
	                              help_text="友情链接图片 ")
	link_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="链接名称", help_text="链接名称")
	link_url = models.URLField(verbose_name="链接地址", blank=True, null=True, help_text="链接地址")
	
	class Meta:
		verbose_name = "友情链接管理"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.link_name


class WebFooterInfo(models.Model):
	"""
	网站页脚信息
	"""
	web_contact = models.CharField(max_length=20, blank=True, null=True, verbose_name="联系方式", help_text="联系方式")
	web_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="地址", help_text="地址")
	web_icp = models.CharField(max_length=50, blank=True, null=True, verbose_name="ICP备案信息", help_text="ICP备案信息")
	web_security_info = models.CharField(max_length=50, blank=True, null=True, verbose_name="公安备案信息", help_text="公安备案信息")
	wechat_qrcode = models.ImageField(upload_to="wechat_qrcode/", blank=True, null=True, verbose_name="公众号二维码", help_text="公众号二维码")
	wechat_qrcode2 = models.ImageField(upload_to="wechat_qrcode/", blank=True, null=True, verbose_name="小程序二维码", help_text="小程序二维码")
	# web_footer_link = models.ForeignKey(WebFooterLink, on_delete=models.CASCADE, related_name="web_footer_link",
	#                                     verbose_name="页脚友情链接", help_text="页脚友情链接")
	
	class Meta:
		verbose_name = "网站页脚信息"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.web_contact


class SystemAdminURL(models.Model):
	"""
	后台管理系统地址
	"""
	web_admin_url = models.CharField(default="HQJY-Admin", max_length=20, verbose_name="系统后台管理地址", help_text="系统后台管理地址")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")
	
	class Meta:
		verbose_name = "系统后台管理地址"
		verbose_name_plural = verbose_name
		ordering = ("-add_time", )
	
	def __str__(self):
		return self.web_admin_url
