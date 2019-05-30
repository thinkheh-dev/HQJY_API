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
from apiutils.permissions import IsOwnerOrReadOnly, IsServiceProvider

from .models import EnterpriseTypeLevel, BasicEnterpriseInfo, EnterpriseReviewFile, EnterpriseAuthManuallyReview
from .serializers import BasicEnterpriseInfoSerializers, EnterpriseAuthManuallyReviewSerializers, \
    EnterpriseReviewFileSerializers, EnterpriseAuthUpdateSerializers, BasicEnterpriseInfoUpdateSerializers, \
    EnterpriseInfoOperatorDetailSerializers, EnterpriseSelfServicesSerializers, EnterpriseSelfOrderSerializers, \
    EnterpriseSelfOrderUpdateSerializers, BasicEnterpriseInfoTempSerializers
from users.serializers import UserInfoDetailSerializers
from HQJY_API.settings import SMS_API_KEY, REAL_API_KEY, EPS_API_KEY
from apiutils.yunpiansms import YunPianSmsSend
from apiutils.epsinfoauth import EnterpriseInfoAuthInterface
from .filters import BasicEnterpriseInfoFilter, EnterpriseInfoOperatorDetailFilter, \
    EnterpriseSelfDefaultServicesFilter, EnterpriseSelfFinancingServicesFilter, EnterpriseSelfOrderFilter, \
    EnterpriseAuthListFilter
from users.models import UserPermissionsName, UserInfo
from service_object.models import DefaultServices, FinancingServices
from user_operation.models import OrderInfo


# 分页
class EnterpriseInfoPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


class EnterpriseAuthPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = "p"
    max_page_size = 100


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
    search_fields = ('name', 'credit_no', 'oper_name', 'oper_phone', 'province', 'city', 'county')
    ordering_fields = ('name', 'city')
    

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
        
        return Response({"message": "恭喜，{} 企业信息更新完成".format(instance.enterprise_name)})

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
    企业认证创建人工审核视图
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
            serializer.validated_data['user_id'] = user_id
            
            if BasicEnterpriseInfo.objects.filter(name=serializer.validated_data['enterprise_code']).count():
                return Response({"error_message": "您提交验证的公司，已经存在，请联系网站管理员或检查公司信息！"})

            auth_content = self.perform_create(serializer)

            # 为当前用户增加验证的关联
            user = get_user_model()

            user_info = user.objects.filter(id=user_id).update(eps_auth_manually_review=auth_content.id)
            print(user_info)

        return Response({"message": "创建成功"})
    
    def perform_create(self, serializer):
        return serializer.save()
    

class EnterpriseAuthReadInterfaceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    """
    连接第三方接口，获取数据并保存在数据库中
    """

    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = BasicEnterpriseInfoTempSerializers
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
     
    
class EnterpriseAuthUpdateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
    企业认证人工审核更新视图
    
    list: 人工审核列表
    
    retrieve: 人工审核详情
    
    update：更新人工审核状态
    
    """
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseAuthUpdateSerializers
    pagination_class = EnterpriseAuthPagination

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = EnterpriseAuthListFilter
    ordering_fields = ('add_time', )
    
    def get_queryset(self):
        # return EnterpriseAuthManuallyReview.objects.filter(apply_audit_status=3)
        return EnterpriseAuthManuallyReview.objects.all()
    
    def update(self, request, *args, **kwargs):
        
        # 获取当前用户
        user = get_user_model()
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        eps_auth_id = instance.id
        eps_auth_data = self.perform_update(serializer)
        
        # 获取当前用户手机号，用于发送短信 -- 这里不要随意更改
        user_phone = list(user.objects.filter(id=eps_auth_data.user_id).values())[0]['user_phone']

        # 实例化发送短信函数，根据申请结果发送短信
        juhe = YunPianSmsSend(SMS_API_KEY)

        if eps_auth_data.apply_audit_status == 1:
            print("审核通过")
            auth_status = "审核通过"
            user_permission_name_id = UserPermissionsName.objects.get(permission_sn="QX004").id

            # 人工审核通过后，使用第三方接口获取企业工商数据，并存储到数据库
            juhe_eps_info = EnterpriseInfoAuthInterface(EPS_API_KEY)
            eps_info_result = juhe_eps_info.send_auth(name=eps_auth_data.enterprise_code)
            print(eps_info_result)

            # 判断接口是否成功获取数据
            if eps_info_result['error_code'] != 0:
                # basic_info = BasicEnterpriseInfo.objects.create(credit_no=eps_auth_data.enterprise_code,
                #                                                 oper_name=eps_auth_data.enterprise_oper_name)
                return Response({
                    "fail": 0,
                    "error_message": eps_info_result['reason']
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("创建企业信息--({})".format(eps_info_result["result"]["enterpriseName"]))
                # 根据获取的工商数据创建企业信息
                basic_info = BasicEnterpriseInfo.objects.create(name=eps_info_result["result"]["enterpriseName"],
                                                                credit_no=eps_info_result["result"]["creditCode"],
                                                                oper_name=eps_info_result["result"]["frName"],
                                                                reg_no=eps_info_result["result"]["regNo"],
                                                                econ_kind=eps_info_result["result"]["enterpriseType"],
                                                                regist_capi=eps_info_result["result"]["regCap"],
                                                                reg_capcur=eps_info_result["result"]["regCapCur"],
                                                                status=eps_info_result["result"]["enterpriseStatus"],
                                                                cancel_date=eps_info_result["result"]["cancelDate"],
                                                                revoke_date=eps_info_result["result"]["revokeDate"],
                                                                address=eps_info_result["result"]["address"],
                                                                start_date=eps_info_result["result"]["esDate"],
                                                                term_start=eps_info_result["result"]["openFrom"],
                                                                term_end=eps_info_result["result"]["openTo"],
                                                                belong_org=eps_info_result["result"]["regOrg"],
                                                                abu_item=eps_info_result["result"]["abuItem"],
                                                                cbu_item=eps_info_result["result"]["cbuItem"],
                                                                operate_scope=eps_info_result["result"]["operateScope"],
                                                                operate_scope_and_form=eps_info_result["result"][
                                                                                       "operateScopeAndForm"],
                                                                org_code=eps_info_result["result"]["orgCode"],
                                                                appr_date=eps_info_result["result"]["apprDate"],
                                                                province=eps_info_result["result"]["province"],
                                                                city=eps_info_result["result"]["city"],
                                                                county=eps_info_result["result"]["county"],
                                                                area_code=eps_info_result["result"]["areaCode"],
                                                                industry_phycode=eps_info_result["result"][
                                                                                 "industryPhyCode"],
                                                                industry_phyname=eps_info_result["result"][
                                                                                 "industryPhyName"],
                                                                industry_code=eps_info_result["result"]["industryCode"],
                                                                industry_name=eps_info_result["result"]["industryName"])

                print("创建企业信息完成！")

                # 企业认证完成，更新用户权限为：企业用户（QX004)
                user.objects.filter(id=eps_auth_data.user_id).update(user_to_company=basic_info.id,
                                                                     user_permission_name=user_permission_name_id)
                # 发送审核成功短信
                sms_success_send = juhe.send_success_sms(user_phone=user_phone)
                if sms_success_send["error_code"] != 0:
                    sms_send_result = "审核短信发送失败！原因：{}".format(sms_success_send["result"]['resmsg'])
                else:
                    sms_send_result = "审核短信发送成功！"

        else:
            print("审核不通过")
            auth_status = "审核未通过"
            sms_fail_send = juhe.send_fail_sms(user_phone=user_phone)
            if sms_send_code["error_code"] != 0:
                sms_send_result = "审核短信发送失败！原因：{}".format(sms_fail_send["result"]['resmsg'])
            else:
                sms_send_result = "审核短信发送成功！"

        # 拼接返回的json数据
        re_dict = {}
        re_dict['message'] = "人工审核流程完成"
        re_dict['id'] = eps_auth_id
        re_dict['user_id'] = eps_auth_data.user_id
        re_dict['sms_send_result'] = sms_send_result
        re_dict['auth_status'] = auth_status
        re_dict['enterprise_name'] = list(BasicEnterpriseInfo.objects.filter(
                                     credit_no=eps_auth_data.enterprise_code).values())[0]['name']
        re_dict['enterprise_oper_name'] = eps_auth_data.enterprise_oper_name
        re_dict['auth_failure_reason'] = eps_auth_data.auth_failure_reason
        
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

    filter_backends = (DjangoFilterBackend, )
    filter_class = EnterpriseInfoOperatorDetailFilter

    def get_queryset(self):
        return UserInfo.objects.all()



class EnterpriseSelfDefaultServicesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    普适服务查询
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseSelfServicesSerializers
    filter_backends = (DjangoFilterBackend, )
    filter_class = EnterpriseSelfDefaultServicesFilter

    def get_queryset(self):
        # 获取普适服务
        return DefaultServices.objects.all()


class EnterpriseSelfFinancingServicesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    金融服务查询
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseSelfFinancingServicesFilter
    filter_backends = (DjangoFilterBackend, )
    filter_class = EnterpriseSelfFinancingServicesFilter

    def get_queryset(self):
        # 获取金融服务
        return FinancingServices.objects.all()


class EnterpriseSelfOrderListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    企业订单查询
    """
    permission_classes = (IsAuthenticated, IsServiceProvider)
    pagination_class = EnterpriseInfoPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseSelfOrderSerializers
    filter_backends = (DjangoFilterBackend,)
    filter_class = EnterpriseSelfOrderFilter

    def get_queryset(self):
        # 获取企业订单
        userinfo = self.request.user
        return OrderInfo.objects.filter(order_belong_company=userinfo.user_to_company).order_by("-order_end_time")


class EnterpriseSelfOrderUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    企业订单状态更新
    """
    permission_classes = (IsAuthenticated, IsServiceProvider)
    pagination_class = EnterpriseInfoPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EnterpriseSelfOrderUpdateSerializers

    def get_queryset(self):
        return OrderInfo.objects.all()

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"message": "订单更新成功"})

    def perform_update(self, serializer):
        return serializer.save()
