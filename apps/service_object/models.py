from datetime import datetime
import random
from django.db import models
from enterprise_info.models import BasicEnterpriseInfo

class ServiceAbstractClass(models.Model):
	"""
	服务项目基类
	"""
	
	def create_sn(self):
		header = datetime.now().strftime("%Y%m%d%H%M%S")
		r_letter = chr(random.randint(97, 122))
		r_num = random.randint(100, 999)
		sn_str = header + r_letter + str(r_num)
		return sn_str
		
	service_sn = models.CharField(max_length=64, primary_key=True, default=create_sn(), verbose_name="需求编号")
	service_belong_to_company = models.ForeignKey(BasicEnterpriseInfo, on_delete=models.CASCADE,
	                                              related_name="company_info", verbose_name="所属企业")
	service_name = models.CharField(max_length=100, verbose_name="服务名称")
	service_describe = models.CharField(max_length=200, blank=True, null=True, verbose_name="简短描述")
	service_clicks = models.IntegerField(default=0, editable=True, verbose_name="被点击数")
	service_sales = models.IntegerField(default=0, editable=True, verbose_name="销量")
	service_fav_nums = models.IntegerField(default=0, editable=True, verbose_name="被收藏数")
	service_detailed_description = models.TextField(blank=True, null=True, verbose_name="详细内容")
	service_additional_costs = models.IntegerField(default=0, editable=True, verbose_name="额外费用")
	service_cover_photo = models.ImageField(upload_to="/service_cover", blank=True, null=True, verbose_name="封面图片")
	is_new = models.BooleanField(default=True, verbose_name="是否新品")
	is_hot = models.BooleanField(default=False, verbose_name="是否热销品")
	is_shelf = models.BooleanField(default=False, verbose_name="是否上架")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	
	class Meta:
		abstract=True
		

	