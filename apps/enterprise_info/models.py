from django.db import models
from datetime import datetime

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
# class EnterpriseTypeFirst(models.Model):
# 	"""
# 	企业行业一级分类py
# 	"""
# 	first_type_name = models.CharField(max_length=20, verbose_name="分类名称")
#
# 	class Meta:
# 		verbose_name = "企业行业一级分类"
# 		verbose_name_plural = verbose_name
#
# 	def __str__(self):
# 		return self.first_type_name
#
#
# class EnterpriseTypeSecond(models.Model):
# 	"""
# 	企业行业二级分类
# 	"""
# 	second_type_name = models.CharField(max_length=20, verbose_name="分类名称")
# 	enterprise_type_first = models.ForeignKey(EnterpriseTypeFirst, on_delete=models.CASCADE, verbose_name="一级分类外键")
#
# 	class Meta:
# 		verbose_name = "企业行业二级分类"
# 		verbose_name_plural = verbose_name
#
# 	def __str__(self):
# 		return self.second_type_name


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
	regist_capi = models.IntegerField(blank=True, null=True, verbose_name="注册资金", help_text="注册资金")
	scope = models.CharField(max_length=255, blank=True, null=True, verbose_name="经营范围", help_text="经营范围")
	status = models.CharField(max_length=50, blank=True, null=True, verbose_name="公司状态(开业/注销)", help_text="公司状态(开业/注销)")
	address = models.CharField(max_length=200, blank=True, null=True, verbose_name="企业地址", help_text="企业地址")
	start_date = models.DateField(blank=True, null=True, verbose_name="成立日期", help_text="成立日期")
	term_start = models.DateField(blank=True, null=True, verbose_name="营业开始日期", help_text="营业开始日期")
	term_end = models.DateField(blank=True, null=True, verbose_name="营业结束日期", help_text="营业结束日期")
	belong_org = models.CharField(max_length=50, blank=True, null=True, verbose_name="登记机关", help_text="登记机关")
	company_area = models.CharField(max_length=20, choices=COUNTY_CHOICES, verbose_name="企业归属地", help_text="企业归属地")
	enterprise_type = models.ForeignKey(EnterpriseType, on_delete=models.CASCADE,
	                                          related_name="entype_first", verbose_name="企业分类", help_text="企业分类")
	enterprise_label = models.ForeignKey(EnterpriseLabel, on_delete=models.CASCADE, related_name="enlabel",
	                                     verbose_name="企业标签", help_text="企业标签")
	oper_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="企业联系人", help_text="企业联系人")
	scan_of_company_license = models.ImageField(upload_to="company_license/", blank=True, null=True,
	                                            verbose_name="营业执照复印件", help_text="营业执照复印件")
	scan_of_id_card = models.ImageField(upload_to="id_card/", blank=True, null=True, verbose_name="法人身份复印件", help_text="法人身份复印件")
	
	class Meta:
		verbose_name = "企业基础信息"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name


