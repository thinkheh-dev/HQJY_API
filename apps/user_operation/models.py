from django.utils import timezone
import uuid

from django.db import models

from users.models import UserInfo
from service_object.models import DefaultServices, DefaultServicesPackage, DefaultServiceCoupon
from enterprise_info.models import BasicEnterpriseInfo


class ShoppingCart(models.Model):
	"""
	购物车模型
	"""
	user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户")
	default_services = models.ForeignKey(DefaultServices, on_delete=models.CASCADE, verbose_name="普适服务")
	default_services_package = models.ForeignKey(DefaultServicesPackage, on_delete=models.CASCADE, verbose_name="普适项目包")
	buy_nums = models.IntegerField(default=1, editable=True, verbose_name="购买数量")
	
	class Meta:
		verbose_name = "购物车"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.user_info
	
class OrderInfo(models.Model):
	"""
	订单信息
	"""
	ORDER_STATUS = (
		
		('TRADE_SUCCESS', '交易成功'),
		('TRADE_FAIL', '交易失败'),
		('WAIT_TRADE_BY', '创建交易中'),
		('TRADE_END', '交易结束'),
		('PAYING', '支付中'),
		('TRADE_IN_PROGRESS', '交易进行中'),
		
	)
	
	user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="user_order_info", verbose_name="用户")
	order_sn = models.UUIDField(auto_created=True, default=uuid.uuid4, verbose_name="订单号uuid")
	#trade_sn = models.CharField(max_length=200, verbose_name="交易号") -- 用于网上支付的交易号，目前暂不启用
	order_status = models.CharField(max_length=50, choices=ORDER_STATUS, verbose_name="交易状态")
	order_message = models.TextField(verbose_name="订单留言")
	order_amount = models.IntegerField(default=0, editable=True, verbose_name="订单金额")
	default_service_coupon = models.ManyToManyField(DefaultServiceCoupon, verbose_name="可用优惠券")
	pay_time = models.DateTimeField(default=timezone.now, verbose_name="支付时间")
	enterprise_info_service = models.ForeignKey(BasicEnterpriseInfo, on_delete=models.CASCADE, verbose_name="企业信息外键")
	order_contact_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="订单联系人姓名")
	order_contact_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="联系人电话")
	order_remark = models.TextField(blank=True, null=True, verbose_name="订单备注") #不由客户填写，由平台工作人员在后台填写
	industry_commissioner = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="industry_order_info",
	                                          verbose_name="分配行业专员")
	
	class Meta:
		verbose_name = "订单信息"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.order_sn
	
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
	order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单信息外键")
	default_services = models.ForeignKey(DefaultServices, on_delete=models.CASCADE, verbose_name="普适服务外键")
	default_services_package = models.ForeignKey(DefaultServicesPackage, on_delete=models.CASCADE, verbose_name="普适服务包外键")
	service_num = models.IntegerField(default=1, verbose_name="商品数量")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "订单商品详情"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.order_info
	
class WorkbenchParameterConfiguration(models.Model):
	"""
	工作台参数配置
	"""
	name = models.CharField(max_length=100, verbose_name="工作台名称")
	workbench_img = models.ImageField(upload_to="workbench_img/", blank=True, null=True, verbose_name="工作台图片路径")
	workbench_css = models.FileField(upload_to="workbench_css/", blank=True, null=True, verbose_name="工作台样式CSS文件")
	
	class Meta:
		verbose_name = "工作台参数配置"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name
	
class WorkbenchNavConfiguration(models.Model):
	"""
	工作台导航配置
	"""
	name = models.CharField(max_length=50, verbose_name="导航名称")
	index = models.IntegerField(default=1, editable=True, verbose_name="导航排序")
	nav_img = models.ImageField(upload_to="workbench_img/", verbose_name="导航图片")
	nav_url = models.URLField(verbose_name="导航链接地址")
	display_flag = models.BooleanField(default=True, editable=True, verbose_name="导航显示开关")
	
	class Meta:
		verbose_name = "工作台导航配置"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name