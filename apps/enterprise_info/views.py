from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from apiutils.permissions import IsOwnerOrReadOnly

from .models import EnterpriseType, EnterpriseTypeLevel, BasicEnterpriseInfo, EnterpriseReviewFile, \
    EnterpriseAuthManuallyReview
from .serializers import EnterpriseTypeSerializers, BasicEnterpriseInfoSerializers, \
    EnterpriseAuthManuallyReviewSerializers, EnterpriseReviewFileSerializers, EnterpriseAuthUpdateSerializers, \
    BasicEnterpriseInfoUpdateSerializers, EnterpriseInfoOperatorDetailSerializers
from users.serializers import UserInfoDetailSerializers
from HQJY_API.settings import SMS_API_KEY, REAL_API_KEY
from apiutils.yunpiansms import YunPianSmsSend
from .filters import BasicEnterpriseInfoFilter
from users.models import UserPermissionsName, UserInfo


#分页
class EnterpriseInfoPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100
    

class EnterpriseTypeListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    企业分类列表接口
    
    list:
        企业分类列表
    retrieve:
        企业分类详情
    """
    
    queryset = EnterpriseType.objects.all()
    serializer_class = EnterpriseTypeSerializers


class EnterpriseListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    企业列表接口
    
    list:
        企业列表
    retrieve:
        企业详情
    """
    
    queryset = BasicEnterpriseInfo.objects.all().order_by('id')
    serializer_class = BasicEnterpriseInfoSerializers
    pagination_class = EnterpriseInfoPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BasicEnterpriseInfoFilter
    search_fields = ('name', 'credit_no', 'oper_name', 'oper_phone', 'company_area')
    ordering_fields = ('name', 'company_area')
    

class EnterpriseDetailUpdateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                    viewsets.GenericViewSet):
    """
    企业详情更新视图
    注意：此视图只能用于更新企业详情，无法创建，创建过程在审核时就已经完成
    
    list:
        企业详情列表
    retrieve:
        企业详情
    update:
        企业详情更新
        
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = BasicEnterpriseInfoUpdateSerializers
    
    def get_queryset(self):
        user = self.request.user
        return BasicEnterpriseInfo.objects.filter(id=user.user_to_company_id)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({"message":"恭喜，{} 企业信息更新完成".format(instance.enterprise_name)})
        
        
    def perform_update(self, serializer):
        return serializer.save()
    
    
    
    
class EnterpriseAuthFileDownloadViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    企业认证文件下载
    list:
        企业认证文件列表
    """
    queryset = EnterpriseReviewFile.objects.all()
    serializer_class = EnterpriseReviewFileSerializers
    
    
class EnterpriseAuthManuallyReviewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                          viewsets.GenericViewSet):
    """
    企业认证人工审核视图
    list:
        人工审核列表
    retrieve:
        人工审核详情
    create:
        创建人工审核
    delete:
        删除人工审核
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseAuthManuallyReviewSerializers
    
    

    def get_queryset(self):
        user = self.request.user
        return EnterpriseAuthManuallyReview.objects.filter(user_id=user.id)
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_id = request.data['user_id']
        
        if EnterpriseAuthManuallyReview.objects.filter(user_id=user_id).count():
            return Response({'error_message': '您已经认证过，请不要重复提交认证'})
        
        if serializer.is_valid(raise_exception=True):
            print("数据验证成功")
            serializer.validated_data['user_id'] = user_id
            
            if BasicEnterpriseInfo.objects.filter(name=serializer.validated_data['enterprise_name']).count():
                return Response({"error_message": "您提交验证的公司，已经存在，请联系网站管理员或更换公司！"})

            auth_content = self.perform_create(serializer)

            #为当前用户增加验证的关联
            user = get_user_model()

            user_info = user.objects.filter(id=user_id).update(eps_auth_manually_review=auth_content.id)
            print(user_info)
            
        return Response({"message": "创建成功"})
    
    def perform_create(self, serializer):
        return serializer.save()
    
    
class EnterpriseAuthUpdateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
    企业认证人工审核视图
    
    list: 人工审核列表
    
    retrieve: 人工审核详情
    
    update：更新人工审核状态
    
    """
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseAuthUpdateSerializers
    
    def get_queryset(self):
        # return EnterpriseAuthManuallyReview.objects.filter(apply_audit_status=3)
        return EnterpriseAuthManuallyReview.objects.all()
    
    def update(self, request, *args, **kwargs):
        
        #获取当前用户
        user = get_user_model()
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        eps_auth_id = instance.id
        eps_auth_data = self.perform_update(serializer)
        
        #获取当前用户信息及申请企业名称，用于发送短信 -- 这里不要随意更改
        username = list(user.objects.filter(id=eps_auth_data.user_id).values())[0]['username']
        company_name = eps_auth_data.enterprise_name
        user_phone = list(user.objects.filter(id=eps_auth_data.user_id).values())[0]['user_phone']
        
        #临时用的测试代码段，正式代码在下方，短信可以发送后，这段代码即废弃
        if eps_auth_data.apply_audit_status == 1:
            print("审核通过")
            auth_status = "审核通过"
            user_permission_name_id = UserPermissionsName.objects.get(permission_sn="QX004").id
            
            basic_info = BasicEnterpriseInfo.objects.create(name=eps_auth_data.enterprise_name,
                                                            oper_name=eps_auth_data.enterprise_oper_name)
            # 企业认证完成，更新用户权限为：企业用户（QX004)
            user.objects.filter(id=eps_auth_data.user_id).update(user_to_company=basic_info.id,
                                                                 user_permission_name=user_permission_name_id)
        else:
            print("审核不通过")
            auth_status = "审核未通过"
            
        
        
        #根据申请结果发送短信
        # yun_pian = YunPianSmsSend(API_KEY)
		#
        # if eps_auth_data.apply_audit_status == 1:
        #     print("审核通过")
        #     auth_status = "审核通过"
        #     user_permission_name_id = UserPermissionsName.objects.get(permission_sn="QX004").id
		#
        #     basic_info = BasicEnterpriseInfo.objects.create(name=eps_auth_data.enterprise_name,
	    #                                                     oper_name=eps_auth_data.enterprise_oper_name)
        #     # 企业认证完成，更新用户权限为：企业用户（QX004)
        #     user.objects.filter(id=eps_auth_data.user_id).update(user_to_company=basic_info.id,
	    #                                                          user_permission_name=user_permission_name_id)
	    #
        #     sms_send_code = yun_pian.send_sms(username=username, company_name=company_name, success="成功",
        #                                               user_phone=user_phone)
        #     if sms_send_code["code"] != 0:
        #         sms_send_result = "审核短信发送失败！原因：{}".format(sms_send_code['msg'])
        #     else:
        #         sms_send_result = "审核短信发送成功！"
        # else:
        #     print("审核不通过")
        #     auth_status = "审核未通过"
        #     sms_send_code = yun_pian.send_sms(username=username, company_name=company_name, success="未通过",
        #                                         user_phone=user_phone)
        #     if sms_send_code["code"] != 0:
        #         sms_send_result = "审核短信发送失败！原因：{}".format(sms_send_code['msg'])
        #     else:
        #         sms_send_result = "审核短信发送成功！"
        
        
        #拼接返回的json数据
        re_dict = {}
        re_dict['message'] = "人工审核流程完成"
        re_dict['id'] = eps_auth_id
        re_dict['user_id'] = eps_auth_data.user_id
        # re_dict['sms_send_result'] = sms_send_result
        re_dict['auth_status'] = auth_status
        re_dict['enterprise_name'] = eps_auth_data.enterprise_name
        re_dict['enterprise_oper_name'] = eps_auth_data.enterprise_oper_name
        re_dict['auth_failure_reason'] = eps_auth_data.auth_failure_reason
        re_dict['sys_message'] = "系统提示：只有补充完企业信息后，您的权限才能是 企业VIP用户！"
        
        return Response({"result": re_dict})

    def perform_update(self, serializer):
        return serializer.save()

class EnterpriseInfoOperatorDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    企业信息及负责人组合信息接口
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseInfoOperatorDetailSerializers

    def get_queryset(self):
        return UserInfo.objects.all(), BasicEnterpriseInfo.objects.all()