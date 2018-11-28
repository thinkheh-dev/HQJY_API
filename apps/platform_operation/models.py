from django.db import models
from datetime import datetime

from DjangoUeditor.models import UEditorField
from users.models import UserInfo


class InfoCategories(models.Model):
	"""
	信息版块一级分类
	"""
	section_name = models.CharField(max_length=50, verbose_name="一级分类名称")
	
	class Meta:
		verbose_name = "信息一级分类"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.section_name


class InfoCategoriesSecond(models.Model):
	"""
	信息版块二级分类
	"""
	section_name = models.CharField(max_length=50, verbose_name="二级分类名称")
	info_categories = models.ForeignKey(InfoCategories, on_delete=models.CASCADE, verbose_name="所属一级分类")
	
	class Meta:
		verbose_name = "信息二级分类"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.section_name


class WeMediaArticles(models.Model):
	"""
	平台自媒体文章
	"""
	title = models.CharField(max_length=200, verbose_name="标题")
	subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name="副标题")
	info_categories = models.ForeignKey(InfoCategories, on_delete=models.CASCADE,
	                                    verbose_name="信息版块一级分类")
	info_categories_second = models.ForeignKey(InfoCategoriesSecond, on_delete=models.CASCADE, verbose_name="信息板块二级分类")
	abstract = models.TextField(max_length=200, blank=True, null=True, verbose_name="摘要")
	content = UEditorField(default="", width=1000, height=300, filePath="platform_op/files/",
	                       imagePath="platform_op/images/", verbose_name="正文")
	attachment = models.FileField(upload_to="we_media_articles/", verbose_name="附件")
	publish_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
	author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="作者")
	read_nums = models.IntegerField(default=0, editable=True, verbose_name="阅读计数")
	
	class Meta:
		verbose_name = "平台自媒体文章"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.title


class PlatformActivity(models.Model):
	"""
	平台活动
	"""
	activity_title = models.CharField(max_length=200, verbose_name="活动名称")
	activity_posters = models.ImageField(upload_to="platform_activity/", blank=True, null=True, verbose_name="封面图片")
	activity_organizer = models.CharField(max_length=200, blank=True, null=True, verbose_name="活动发布人")
	activity_start_time = models.DateTimeField(default=datetime.now, editable=True, verbose_name="活动开始时间")
	activity_end_time = models.DateTimeField(default=datetime.now, editable=True, verbose_name="活动结束时间")
	activity_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="活动地址")
	activity_desc = UEditorField(default="", width=1000, height=300, filePath="platform_act/files/",
	                       imagePath="platform_act/images/", verbose_name="活动详情")
	activity_tickets = models.IntegerField(default=0, editable=True, verbose_name="门票价格")
	meals_flag = models.BooleanField(default=False, editable=True, verbose_name="是否供餐")
	accommodation_flag = models.BooleanField(default=False, editable=True, verbose_name="是否提供住宿")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	class Meta:
		verbose_name = "平台活动"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.activity_title


class ActivityRegList(models.Model):
	"""
	参加活动名单
	"""
	SEX_CHOICE = (
		("男", "男"),
		("女", "女")
	)
	
	NATIONAL_CHOICE = (
		('1', '汉族'),
		('2', '蒙古族'),
		('3', '回族'),
		('4', '藏族'),
		('5', '维吾尔族'),
		('6', '苗族'),
		('7', '彝族'),
		('8', '壮族'),
		('9', '布依族'),
		('10', '朝鲜族'),
		('11', '满族'),
		('12', '侗族'),
		('13', '瑶族'),
		('14', '白族'),
		('15', '土家族'),
		('16', '哈尼族'),
		('17', '哈萨克族'),
		('18', '傣族'),
		('19', '黎族'),
		('20', '傈僳族'),
		('21', '佤族'),
		('22', '畲族'),
		('23', '高山族'),
		('24', '拉祜族'),
		('25', '水族'),
		('26', '东乡族'),
		('27', '纳西族'),
		('28', '景颇族'),
		('29', '柯尔克孜族'),
		('30', '土族'),
		('31', '达斡尔族'),
		('32', '仫佬族'),
		('33', '羌族'),
		('34', '布朗族'),
		('35', '撒拉族'),
		('36', '毛难族'),
		('37', '仡佬族'),
		('38', '锡伯族'),
		('39', '阿昌族'),
		('40', '普米族'),
		('41', '塔吉克族'),
		('42', '怒族'),
		('43', '乌孜别克族'),
		('44', '俄罗斯族'),
		('45', '鄂温克族'),
		('46', '崩龙族'),
		('47', '保安族'),
		('48', '裕固族'),
		('49', '京族'),
		('50', '塔塔尔族'),
		('51', '独龙族'),
		('52', '鄂伦春族'),
		('53', '赫哲族'),
		('54', '门巴族'),
		('55', '珞巴族'),
		('56', '基诺族'),
		('57', '其他未标明民族'),
		('58', '入籍外国人')

	)
	
	name = models.CharField(max_length=50, verbose_name="姓名")
	sex = models.CharField(max_length=10, choices=SEX_CHOICE, verbose_name="性别")
	national = models.IntegerField(choices=NATIONAL_CHOICE, verbose_name="民族")
	phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="联系方式")
	
	class Meta:
		verbose_name = "参加活动名单"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name


class ActivityRegistration(models.Model):
	"""
	活动报名
	"""
	reg_account = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="reg_account", verbose_name="报名帐号")
	reg_company = models.CharField(max_length=200, blank=True, null=True, verbose_name="报名的公司")
	reg_number = models.IntegerField(default=0, editable=False, verbose_name="报名人数")
	meals_number = models.IntegerField(default=0, editable=True, verbose_name="用餐人数")
	accommodation_number = models.IntegerField(default=0, editable=True, verbose_name="住宿人数")
	# 多对多字段，不会在后台显示，也不可在后台维护
	reg_list = models.ManyToManyField(ActivityRegList, related_name="reg_list", verbose_name="活动名单")
	
	class Meta:
		verbose_name = "活动报名"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.reg_company