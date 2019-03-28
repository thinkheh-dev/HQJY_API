from datetime import datetime
import uuid
from DjangoUeditor.models import UEditorField
from django.db import models

from django.contrib.auth import get_user_model
from service_object.models import DefaultServices, DefaultServicesPackage, DefaultServiceCoupon, FinancingServices
from enterprise_info.models import BasicEnterpriseInfo

User = get_user_model()

# class ShoppingCart(models.Model):
# 	"""
# 	购物车模型
# 	"""
# 	user_info = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", help_text="用户")
# 	default_services = models.ForeignKey(DefaultServices,blank=True, null=True, on_delete=models.CASCADE,
# 	                                     verbose_name="普适服务", help_text="普适服务")
# 	default_services_package = models.ForeignKey(DefaultServicesPackage, blank=True, null=True,
# 	                                             on_delete=models.CASCADE, verbose_name="普适项目包", help_text="普适项目包")
# 	financing_services = models.ForeignKey(FinancingServices, blank=True, null=True, on_delete=models.CASCADE,
# 	                                       verbose_name="金融服务", help_text="金融服务")
# 	#buy_nums = models.IntegerField(default=1, editable=True, verbose_name="购买数量", help_text="购买数量")
# 	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
#
# 	class Meta:
# 		verbose_name = "用户收藏"
# 		verbose_name_plural = verbose_name
# 		unique_together = (("user_info", "default_services"),("user_info", "default_services_package"),
# 		                   ("user_info", "financing_services"),)
#
# 	def __str__(self):
# 		return self.user_info.username

class UserFav(models.Model):
	"""
	用户收藏
	"""
	user_info = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", help_text="用户")
	default_services = models.ForeignKey(DefaultServices, blank=True, null=True, on_delete=models.CASCADE,
	                                     verbose_name="普适服务", help_text="普适服务id")
	default_services_package = models.ForeignKey(DefaultServicesPackage, blank=True, null=True,
	                                             on_delete=models.CASCADE, verbose_name="普适项目包", help_text="普适项目包id")
	financing_services = models.ForeignKey(FinancingServices, blank=True, null=True, on_delete=models.CASCADE,
	                                       verbose_name="金融服务", help_text="金融服务id")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "用户收藏"
		verbose_name_plural = verbose_name
		unique_together = (("user_info", "default_services"), ("user_info", "default_services_package"),
		                   ("user_info", "financing_services"),)
	
	def __str__(self):
		return "{}的收藏夹".format(self.user_info.username)


class OrderInfo(models.Model):
	"""
	订单信息
	"""
	ORDER_STATUS = (

		('TRADE_SUCCESS', '交易成功'),
		('TRADE_cancel', '交易取消'),
		('WAIT_TRADE_BY', '创建交易'),

	)

	user_info = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order_info", verbose_name="用户",
	                              help_text="用户")
	order_sn = models.UUIDField(auto_created=True, default=uuid.uuid4, verbose_name="订单号uuid", help_text="订单号uuid")
	#trade_sn = models.CharField(max_length=200, verbose_name="交易号") -- 用于网上支付的交易号，目前暂不启用
	order_status = models.CharField(max_length=50, default='WAIT_TRADE_BY', choices=ORDER_STATUS,
	                                verbose_name="交易状态", help_text="交易状态")
	order_message = models.TextField(default="", verbose_name="订单留言", help_text="订单留言")
	order_amount = models.IntegerField(default=0, editable=True, verbose_name="订单金额", help_text="订单金额")
	# default_service_coupon = models.ManyToManyField(DefaultServiceCoupon, blank=True, verbose_name="可用优惠券",
	#                                                 help_text="可用优惠券")
	#pay_time = models.DateTimeField(default=datetime.now(), verbose_name="支付时间", help_text="支付时间")
	#enterprise_info_service = models.ForeignKey(BasicEnterpriseInfo, on_delete=models.CASCADE,
	# verbose_name="企业信息外键", help_text="企业信息外键")
	order_contact_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="订单联系人姓名", help_text="订单联系人姓名")
	order_contact_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="联系人电话", help_text="联系人电话")
	order_remark = models.TextField(blank=True, null=True, verbose_name="订单备注", help_text="订单备注") #不由客户填写，由平台工作人员在后台填写
	industry_commissioner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
	                                          related_name="industry_order_info", verbose_name="分配行业专员",
	                                          help_text="分配行业专员")

	class Meta:
		verbose_name = "订单信息"
		verbose_name_plural = verbose_name

	def __str__(self):
		return "{}的订单{}".format(self.user_info, self.order_sn)

# class OrderCouponRelation(models.Model):
# 	"""
# 	订单优惠券中间模型
# 	"""
# 	order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, related_name="订单id")
# 	default_service_coupon = models.ForeignKey(DefaultServiceCoupon, on_delete=models.CASCADE, verbose_name="普适服务优惠券id")
#


class OrderServiceDetail(models.Model):
	"""
	订单商品详情
	"""
	order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单信息外键", help_text="订单信息外键id")
	default_services = models.ForeignKey(DefaultServices, blank=True, null=True, on_delete=models.CASCADE,
	                                     verbose_name="普适服务外键", help_text="普适服务外键id", related_name="services_detail")
	default_services_package = models.ForeignKey(DefaultServicesPackage, on_delete=models.CASCADE, blank=True,
	                                             null=True, verbose_name="普适服务包外键", help_text="普适服务包外键id")
	financing_services = models.ForeignKey(FinancingServices, blank=True, null=True, on_delete=models.CASCADE,
	                                       verbose_name="金融服务", help_text="金融服务外键id")
	#service_num = models.IntegerField(default=1, verbose_name="商品数量", help_text="商品数量")
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "订单商品详情"
		verbose_name_plural = verbose_name

	def __str__(self):
		return "{}".format(self.order_info)

class WorkbenchParameterConfiguration(models.Model):
	"""
	工作台参数配置
	"""
	name = models.CharField(max_length=100, verbose_name="工作台名称", help_text="工作台名称")
	workbench_img = models.ImageField(upload_to="workbench_img/", blank=True, null=True, verbose_name="工作台图片路径", help_text="工作台图片路径")
	workbench_css = models.FileField(upload_to="workbench_css/", blank=True, null=True, verbose_name="工作台样式CSS文件", help_text="工作台样式CSS文件")

	class Meta:
		verbose_name = "工作台参数配置"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

class WorkbenchNavConfiguration(models.Model):
	"""
	工作台导航配置
	"""
	name = models.CharField(max_length=50, verbose_name="导航名称", help_text="导航名称")
	index = models.IntegerField(default=1, editable=True, verbose_name="导航排序", help_text="导航排序")
	nav_img = models.ImageField(upload_to="workbench_img/", verbose_name="导航图片", help_text="导航图片")
	nav_url = models.URLField(verbose_name="导航链接地址", help_text="导航链接地址")
	display_flag = models.BooleanField(default=True, editable=True, verbose_name="导航显示开关", help_text="导航显示开关")

	class Meta:
		verbose_name = "工作台导航配置"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name
