#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @version : v1.0
# @time    : 2019-01-30 10:26
# @author  : warlock921
# @contact : caoyu921@163.com
# @file    : serializers.py
# @software: PyCharm

from rest_framework import serializers, status
from django.db.models import Q

from .models import EnterpriseTypeLevel, BasicEnterpriseInfo, EnterpriseLabel, EnterpriseAuthManuallyReview, \
    EnterpriseReviewFile
from users.models import UserInfo
from user_operation.models import OrderInfo


class EnterpriseLabelSerializers(serializers.ModelSerializer):
    """
    企业标签序列化
    """

    class Meta:
        model = EnterpriseLabel
        fields = "__all__"


class EnterpriseTypeLevelSerializers(serializers.ModelSerializer):
    """
    企业级别序列化
    """

    class Meta:
        model = EnterpriseTypeLevel
        fields = "__all__"


# #企业类型序列化 -- 开始
# class EnterpriseTypeSerializers3(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = EnterpriseType
# 		fields = "__all__"
#
#
# class EnterpriseTypeSerializers2(serializers.ModelSerializer):
# 	sub_type = EnterpriseTypeSerializers3(many=True)
#
# 	class Meta:
# 		model = EnterpriseType
# 		fields = "__all__"
#
# class EnterpriseTypeSerializers(serializers.ModelSerializer):
# 	sub_type = EnterpriseTypeSerializers2(many=True)
#
# 	class Meta:
# 		model = EnterpriseType
# 		fields = "__all__"
# #企业类型序列化 -- 结束


class EnterpriseReviewFileSerializers(serializers.ModelSerializer):
    """
    企业认证文件序列化
    """

    class Meta:
        model = EnterpriseReviewFile
        fields = ['eps_review_template_file', ]


class EnterpriseAuthManuallyReviewSerializers(serializers.ModelSerializer):
    """
    企业认证人工审核序列化
    """

    apply_audit_status = serializers.CharField(default=3, required=False, read_only=True, label="审核状态")
    soc_mark_flag = serializers.BooleanField(default=False, required=False, write_only=True, label="服务机构认证标志")

    # 检测用户是否存在，不存在则报错
    def validate_user_id(self, user_id):
        user = UserInfo.objects.filter(id=user_id).count()
        if not user:
            raise serializers.ValidationError(detail={"error_message": "该用户不存在,请刷新页面重试！", "error_code":
                status.HTTP_400_BAD_REQUEST})

    class Meta:
        model = EnterpriseAuthManuallyReview
        fields = ['id', 'user_id', 'enterprise_code', 'enterprise_oper_name', 'enterprise_oper_idcard',
                  'enterprise_license', 'enterprise_review', 'apply_audit_status', 'soc_mark_flag']


class EnterpriseAuthUpdateSerializers(serializers.ModelSerializer):
    """
    企业认证人工审核（完成审核）序列化
    """
    apply_audit_status = serializers.ChoiceField(choices=[1, 2], label="审核状态", help_text="1是审核通过 2是审核不通过")

    class Meta:
        model = EnterpriseAuthManuallyReview
        fields = "__all__"


class BasicEnterpriseInfoSerializers(serializers.ModelSerializer):
    """
    企业基本信息序列化
    """

    enterprise_label = EnterpriseLabelSerializers()

    class Meta:
        model = BasicEnterpriseInfo
        fields = "__all__"


class BasicEnterpriseInfoUpdateSerializers(serializers.ModelSerializer):
    """
    企业基本信息序列化
    """

    class Meta:
        model = BasicEnterpriseInfo
        fields = "__all__"


class BasicEnterpriseInfoNameSerializers(serializers.ModelSerializer):
    """
    企业名称序列化
    """

    class Meta:
        model = BasicEnterpriseInfo
        fields = ("id", "name")


class EnterpriseInfoOperatorDetailSerializers(serializers.Serializer):
    """
    显示企业信息及负责人组合序列化
    """
    id = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(read_only=True)
    user_logo = serializers.FileField(read_only=True)
    user_introduce = serializers.CharField(read_only=True)
    user_important_qualification1 = serializers.FileField(read_only=True)
    user_important_qualification2 = serializers.FileField(read_only=True)
    user_important_qualification3 = serializers.FileField(read_only=True)
    userinfo_flag = serializers.BooleanField(read_only=True)
    user_to_company = BasicEnterpriseInfoSerializers(many=False, read_only=True)


class EnterpriseSelfServicesSerializers(serializers.Serializer):
    """
    企业归属产品序列化
    """
    service_sn = serializers.CharField(read_only=True)
    service_belong_to_company = serializers.CharField(read_only=True)
    service_name = serializers.CharField(read_only=True)
    service_describe = serializers.CharField(read_only=True)
    service_cover_photo = serializers.FileField(read_only=True)


class EnterpriseSelfOrderSerializers(serializers.Serializer):
    """
    企业订单序列化
    """
    id = serializers.IntegerField(read_only=True)
    user_info = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_belong_company = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    order_status = serializers.CharField(read_only=True)
    order_amount = serializers.FloatField(read_only=True)
    order_message = serializers.CharField(read_only=True)
    order_remark = serializers.CharField(read_only=True)
    cancel_order = serializers.CharField(read_only=True)
    order_add_time = serializers.DateTimeField(read_only=True)


class EnterpriseSelfOrderUpdateSerializers(serializers.ModelSerializer):
    """
    企业变更订单信息
    """

    class Meta:
        model = OrderInfo
        fields = ("id", "order_status", "order_remark")


