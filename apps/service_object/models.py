from datetime import datetime
from django.utils import timezone
import random
from django.db import models
# from DjangoUeditor.models import UEditorField
from enterprise_info.models import BasicEnterpriseInfo
from page_control.models import HomeNav


class ServiceAbstractClass(models.Model):
	"""
	服务项目基类
	"""
	
	def create_sn():
		header = datetime.now().strftime("%Y%m%d%H%M%S")
		r_letter = chr(random.randint(97, 122))
		r_num = random.randint(100, 999)
		sn_str = header + r_letter + str(r_num)
		return sn_str
		
	service_sn = models.CharField(max_length=64, primary_key=True, default=create_sn, verbose_name="服务产品编号")
	service_belong_to_company = models.ForeignKey(BasicEnterpriseInfo, on_delete=models.CASCADE, verbose_name="所属企业")
	service_name = models.CharField(max_length=100, verbose_name="服务名称")
	service_describe = models.CharField(max_length=200, blank=True, null=True, verbose_name="简短描述")
	service_clicks = models.IntegerField(default=0, editable=True, verbose_name="被点击数")
	service_sales = models.IntegerField(default=0, editable=True, verbose_name="销量")
	service_fav_nums = models.IntegerField(default=0, editable=True, verbose_name="被收藏数")
	service_detailed_description = models.TextField(blank=True, null=True, verbose_name="详细内容")
	service_additional_costs = models.IntegerField(default=0, editable=True, verbose_name="额外费用")
	service_cover_photo = models.ImageField(upload_to="service_cover/", blank=True, null=True, verbose_name="封面图片")
	is_new = models.BooleanField(default=True, verbose_name="是否新品")
	is_hot = models.BooleanField(default=False, verbose_name="是否热销品")
	is_shelf = models.BooleanField(default=False, verbose_name="是否上架")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	class Meta:
		abstract=True
		
class ServiceClassification(models.Model):
	"""
	普适服务一级分类
	"""
	classio_name = models.CharField(max_length=50, verbose_name="分类名称")
	belong_nav_sc = models.ForeignKey(HomeNav,blank=True, null=True, on_delete=models.CASCADE,
	                               related_name="belong_nav_home",
	                               verbose_name="所属导航")
	
	class Meta:
		verbose_name = "普适服务一级分类"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.classio_name

class ServiceClassificationSecond(models.Model):
	"""
	普适服务二级分类
	"""
	classis_name = models.CharField(max_length=50, verbose_name="分类名称")
	service_classification = models.ForeignKey(ServiceClassification, on_delete=models.CASCADE,
	                                           related_name="service_classification", verbose_name="所属一级分类")
	
	class Meta:
		verbose_name = "普适服务二级分类"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.classis_name
	
class DefaultServices(ServiceAbstractClass):
	"""
	普适服务产品
	"""
	service_classification = models.ForeignKey(ServiceClassification, on_delete=models.CASCADE, verbose_name="普适服务一级分类")
	service_classification_second = models.ForeignKey(ServiceClassificationSecond, on_delete=models.CASCADE,
	                                                  verbose_name="普适服务二级分类")
	service_inventory = models.IntegerField(editable=True, verbose_name="库存数")
	service_market_price = models.FloatField(verbose_name="市场价格")
	service_platform_price = models.FloatField(verbose_name="平台价格")
	
	class Meta:
		verbose_name = "普适服务产品"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.service_name
	
class FinancingServiesClassification(models.Model):
	"""
	融资服务一级分类
	"""
	name = models.CharField(max_length=50, verbose_name="融资服务一级分类")
	belong_nav_fsc = models.ForeignKey(HomeNav,blank=True, null=True, on_delete=models.CASCADE,
	                               related_name="financing_to_nav",
	                               verbose_name="所属导航")
	
	class Meta:
		verbose_name = "融资服务一级分类"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name

class FinancingServicesClassificationSecond(models.Model):
	"""
	融资服务二级分类
	"""
	name = models.CharField(max_length=50, verbose_name="融资服务二级分类")
	fscs = models.ForeignKey(FinancingServiesClassification, on_delete=models.CASCADE, verbose_name="所属一级分类")
	
	class Meta:
		verbose_name = "融资服务二级分类"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.name
	
class FinancingServices(ServiceAbstractClass):
	"""
	融资服务产品
	"""
	fsc = models.ForeignKey(FinancingServiesClassification, on_delete=models.CASCADE, related_name="financing_sc",
	                        verbose_name="融资服务一级外键")
	fscs = models.ForeignKey(FinancingServicesClassificationSecond, on_delete=models.CASCADE,
	                         related_name="financing_scs", verbose_name="融资服务二级外键")
	time_limit = models.CharField(max_length=10, verbose_name="期限")
	annual_interest_rate = models.CharField(max_length=10, verbose_name="年利率")
	approval_lines = models.CharField(max_length=10, verbose_name="审批额度")
	
	class Meta:
		verbose_name = "融资服务产品"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.service_name
	
class ServiceBrand(models.Model):
	"""
	服务品牌
	"""
	brand_name = models.CharField(max_length=20, verbose_name="品牌名称")
	brand_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="品牌描述")
	brand_img = models.ImageField(upload_to="brand_image/", blank=True, null=True, verbose_name="品牌图片")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "服务品牌"
		verbose_name_plural = verbose_name
		
	def __str__(self):
		return self.brand_name

class DefaultServicesPackage(models.Model):
	"""
	普适服务项目包
	"""
	package_name = models.CharField(max_length=200, verbose_name="普适服务包名称")
	package_img = models.ImageField(upload_to="package_img/", blank=True, null=True, verbose_name="包封面图片")
	package_desc = models.TextField(blank=True, null=True, verbose_name="包详细描述")
	default_service = models.ManyToManyField(DefaultServices, related_name="default_service",
	                                         through="ServicePackageMiddle")
	
	class Meta:
		verbose_name = "普适服务项目包"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.package_name
	
class ServicePackageMiddle(models.Model):
	"""
	普适服务包中间模型
	"""
	SP_id = models.ForeignKey(DefaultServicesPackage, on_delete=models.CASCADE)
	S_id = models.ForeignKey(DefaultServices, on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	class Meta:
		db_table = "service_package_relationship"
		
class DefaultCouponType(models.Model):
	"""
	普适服务优惠券类型
	"""
	
	name = models.CharField(max_length=50, verbose_name="类型名称")
	
	class Meta:
		verbose_name = "普适服务优惠券类型"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name

class DefaultServiceCoupon(models.Model):
	"""
	普适服务优惠券
	"""
	coupon_name = models.CharField(max_length=200, verbose_name="优惠券名称")
	coupon_amount = models.IntegerField(default=0, verbose_name="优惠金额")
	coupon_img = models.ImageField(upload_to="counpon_img/", blank=True, null=True, verbose_name="优惠券图片")
	coupon_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name="详细描述")
	coupon_start_time = models.DateField(default=timezone.now, verbose_name="开始时间")
	coupon_end_time = models.DateField(default=timezone.now, verbose_name="结束时间")
	belong_coupon = models.ForeignKey(DefaultServices, on_delete=models.CASCADE, related_name="belong_coupon",
	                                  verbose_name="对应的普适项目")
	default_coupon_type = models.ForeignKey(DefaultCouponType, on_delete=models.CASCADE,
	                                        related_name="default_coupon_type", verbose_name="对应的普适项目类型")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	default_num = models.IntegerField(default=0, editable=True, verbose_name="优惠券数量")
	remain_num = models.IntegerField(default=0, editable=True, verbose_name="优惠券剩余数量")
	
	class Meta:
		verbose_name = "普适服务优惠券"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.coupon_name
	
class HotSearchWords(models.Model):
	"""
	热搜词
	"""
	keywords = models.CharField(max_length=30, verbose_name="热搜词")
	key_index = models.IntegerField(default=1, editable=True, verbose_name="排序")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "热搜词"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.keywords


class EnterpriseDemandAbstract(models.Model):
	"""
	企业需求（父级）
	"""
	company_info = models.ForeignKey(BasicEnterpriseInfo, on_delete=models.CASCADE, verbose_name="关联的企业")
	demand_desc = models.TextField(verbose_name="需求描述（文字/图片）")
	contact_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="联系人姓名")
	contact_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="联系人手机")
	
	class Meta:
		abstract = True


class EnterpriseDemand(EnterpriseDemandAbstract):
	"""
	企业普适需求信息
	"""
	sv_class = models.ForeignKey(ServiceClassification, on_delete=models.CASCADE, related_name="sv_class",
	                             verbose_name="普适服务需求一级分类")
	sv_class_s = models.ForeignKey(ServiceClassificationSecond, on_delete=models.CASCADE, related_name="sv_class_s",
	                               verbose_name="普适服务需求二级分类")
	
	class Meta:
		verbose_name = "企业普适需求"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.company_name


class CorporateFinanceDemand(EnterpriseDemandAbstract):
	"""
	企业融资需求信息
	"""
	fsc = models.ForeignKey(FinancingServiesClassification, on_delete=models.CASCADE, verbose_name="金融服务一级分类")
	fscs = models.ForeignKey(FinancingServicesClassificationSecond, on_delete=models.CASCADE, verbose_name="金融服务二级分类")
	financing_amount = models.IntegerField(blank=True, null=True, verbose_name="融资金额")
	financing_to = models.CharField(max_length=100, blank=True, null=True, verbose_name="融资投向")
	financing_maturity = models.CharField(max_length=20, blank=True, null=True, verbose_name="融资期限")
	
	class Meta:
		verbose_name = "企业融资需求"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.company_name