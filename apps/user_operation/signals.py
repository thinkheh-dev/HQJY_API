#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019/8/19 下午4:59
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : signals.py
# @software: PyCharm

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserFav
from service_object.models import DefaultServices
from service_object.models import FinancingServices


@receiver(post_save, sender=UserFav)
def create_user_fav(sender, instance=UserFav, created=False, **kwargs):

	if created:
		if instance.default_services is not None:
			
			print("服务产品 {} 被收藏 ".format(instance.default_services.service_sn))
			fav_num = DefaultServices.objects.get(service_sn=instance.default_services.service_sn).service_fav_nums
			print("服务产品 {} 当前收藏数为: {} ".format(instance.default_services.service_sn, fav_num))
			fav_num += 1
	
			DefaultServices.objects.filter(service_sn=instance.default_services.service_sn).update(service_fav_nums=fav_num)
			print("服务产品 {} 收藏数更新后为: {} ".format(instance.default_services.service_sn, fav_num))
		else:
			print("服务产品 {} 被收藏 ".format(instance.financing_services.service_sn))
			fav_num = FinancingServices.objects.get(service_sn=instance.financing_services.service_sn).service_fav_nums
			print("服务产品 {} 当前收藏数为: {} ".format(instance.financing_services.service_sn, fav_num))
			fav_num += 1
			
			FinancingServices.objects.filter(service_sn=instance.financing_services.service_sn).update(
				service_fav_nums=fav_num)
			print("服务产品 {} 收藏数更新后为: {} ".format(instance.financing_services.service_sn, fav_num))


@receiver(post_delete, sender=UserFav)
def delete_user_fav(sender, instance=UserFav, **kwargs):
	if instance.default_services is not None:
		
		print("服务产品 {} 被收藏 ".format(instance.default_services.service_sn))
		fav_num = DefaultServices.objects.get(service_sn=instance.default_services.service_sn).service_fav_nums
		print("服务产品 {} 当前收藏数为: {} ".format(instance.default_services.service_sn, fav_num))
		if fav_num != 0:
			fav_num -= 1
		else:
			fav_num = 0
		
		DefaultServices.objects.filter(service_sn=instance.default_services.service_sn).update(service_fav_nums=fav_num)
		print("服务产品 {} 收藏数更新后为: {} ".format(instance.default_services.service_sn, fav_num))
	else:
		print("服务产品 {} 被收藏 ".format(instance.financing_services.service_sn))
		fav_num = FinancingServices.objects.get(service_sn=instance.financing_services.service_sn).service_fav_nums
		print("服务产品 {} 当前收藏数为: {} ".format(instance.financing_services.service_sn, fav_num))
		if fav_num != 0:
			fav_num -= 1
		else:
			fav_num = 0
		
		FinancingServices.objects.filter(service_sn=instance.financing_services.service_sn).update(
			service_fav_nums=fav_num)
		print("服务产品 {} 收藏数更新后为: {} ".format(instance.financing_services.service_sn, fav_num))
