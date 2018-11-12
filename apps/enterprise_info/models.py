from django.db import models



class EnterpriseTypeFirst(models.Model):
	"""
	企业行业一级分类py
	"""
	first_type_name = models.CharField(max_length=20, verbose_name="分类名称")
	
	class Meta:
		verbose_name = "企业行业一级分类"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.first_type_name

	
class EnterpriseTypeSecond(models.Model):
	"""
	企业行业二级分类
	"""
	second_type_name = models.CharField(max_length=20, verbose_name="分类名称")
	enterprise_type_first = models.ForeignKey(EnterpriseTypeFirst, on_delete=models.CASCADE, verbose_name="一级分类外键")
	
	class Meta:
		verbose_name = "企业行业二级分类"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.second_type_name
		

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
	
	name = models.CharField(max_length=50, blank=True, null=True, verbose_name="企业名称")
	credit_no = models.CharField(max_length=18, blank=True, null=True, verbose_name="统一社会信用代码")
	oper_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="企业法人")
	econ_kind = models.CharField(max_length=20, blank=True, null=True, verbose_name="公司类型")
	regist_capi = models.IntegerField(blank=True, null=True, verbose_name="注册资金")
	scope = models.CharField(max_length=255, blank=True, null=True, verbose_name="经营范围")
	status = models.CharField(max_length=50, blank=True, null=True, verbose_name="公司状态(开业/注销)")
	address = models.CharField(max_length=200, blank=True, null=True, verbose_name="企业地址")
	start_date = models.DateField(blank=True, null=True, verbose_name="成立日期")
	term_start = models.DateField(blank=True, null=True, verbose_name="营业开始日期")
	term_end = models.DateField(blank=True, null=True, verbose_name="营业结束日期")
	belong_org = models.CharField(max_length=50, blank=True, null=True, verbose_name="登记机关")
	company_area = models.CharField(max_length=20, choices=COUNTY_CHOICES, verbose_name="企业归属地")
	enterprise_type_first = models.ForeignKey(EnterpriseTypeFirst, on_delete=models.CASCADE,
	                                          related_name="entype_first", verbose_name="企业一级分类")
	enterprise_type_second = models.ForeignKey(EnterpriseTypeSecond, on_delete=models.CASCADE,
	                                           related_name="entype_second", verbose_name="企业二级分类")
	oper_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="法人联系人")
	scan_of_company_license = models.ImageField(upload_to="company_license/", blank=True, null=True,
	                                            verbose_name="营业执照复印件")
	scan_of_id_card = models.ImageField(upload_to="id_card/", blank=True, null=True, verbose_name="法人身份复印件")
	
	class Meta:
		verbose_name = "企业基础信息"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name


