from django.shortcuts import render
from django.contrib.auth import get_user_model
import datetime

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from apiutils.permissions import IsOwnerOrReadOnly, IsServiceProvider

from .models import EnterpriseTypeLevel, BasicEnterpriseInfo, EnterpriseReviewFile, EnterpriseAuthManuallyReview, \
	EnterpriseCertification
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
from apiutils.createcertsn import EnterpriseAuthCertification


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


class EnterpriseAuthManuallyReviewViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                                          mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
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
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = EnterpriseAuthManuallyReviewSerializers
	
	# 获取当前用户信息
	user = get_user_model()
	
	def get_queryset(self):
		user = self.request.user
		return EnterpriseAuthManuallyReview.objects.filter(user_id=user.id, audit_valid_flag=True)
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		user_id = request.data['user_id']
		# 获取用户姓名和手机
		user_name = UserInfo.objects.get(id=user_id).user_name
		user_phone = UserInfo.objects.get(id=user_id).user_phone
		
		# <--2019.6.25 测试通过-->
		if serializer.is_valid(raise_exception=True):
			serializer.validated_data['user_id'] = user_id
			enterprise_name = serializer.validated_data['enterprise_name']
			enterprise_code = serializer.validated_data['enterprise_code']
			
			exsited = BasicEnterpriseInfo.objects.filter(credit_no=enterprise_code).count()
			
			# 判断认证的企业是否存在
			if exsited:
				# 先判断此企业是否被认证过
				eps_id = BasicEnterpriseInfo.objects.get(credit_no=enterprise_code).id
				user_ex = UserInfo.objects.filter(user_to_company=eps_id).count()
				if user_ex:
					return Response({"message": "该企业已经被认证！"}, status=status.HTTP_400_BAD_REQUEST)
				else:
					# 企业信息已经存在且未被认证，则直接验证企业名称是否一致！
					enterprise_name_tmp = list(BasicEnterpriseInfo.objects.filter(credit_no=enterprise_code)
					                           .values())[0]['name']
					print(enterprise_name_tmp)
					print(enterprise_name)
					# 验证企业名称是否一致
					if enterprise_name == enterprise_name_tmp:
						# 创建认证
						auth_id = self.perform_create(serializer)
						# 关联企业认证到当前用户
						UserInfo.objects.filter(id=user_id).update(eps_auth_manually_review=auth_id)
						# 更新企业认证的状态
						EnterpriseAuthManuallyReview.objects.filter(id=auth_id.id).update(apply_audit_status=2,
						                                                                  user_name=user_name,
						                                                                  user_phone=user_phone)
						headers = self.get_success_headers(serializer.data)
						return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
					else:
						return Response({"error_message": "您提交认证的企业名称有误，无法认证"}, status=status.HTTP_400_BAD_REQUEST)
			# <-- 2019.6.25 测试通过 -->
			else:
				# <-- 2019.6.25 测试通过 -->
				# 企业信息不存在，则开始调用第三方接口获取企业信息
				juhe_eps_info = EnterpriseInfoAuthInterface(EPS_API_KEY)
				eps_info_result = juhe_eps_info.send_auth(name=enterprise_code)
				
				# 判断接口是否成功获取数据
				if eps_info_result['error_code'] != 0:
					return Response({
						"fail": 0,
						"error_message": eps_info_result['reason']},
						status=status.HTTP_400_BAD_REQUEST)
				else:
					enterprise_name_tmp = eps_info_result["result"]["enterpriseName"]
					enterprise_cancel_date = eps_info_result["result"]["cancelDate"]
					enterprise_revoke_date = eps_info_result["result"]["revokeDate"]
					
					# 验证第三方接口返回的企业名称与用户提供的企业名称是否一致
					if enterprise_name==enterprise_name_tmp:
						# 企业名称验证一致，检测企业是否注销或吊销
						if enterprise_cancel_date != "" and enterprise_revoke_date!="":
							return Response({"error_message": "您提交验证的企业已经注销或者被吊销！"}, status=status.HTTP_400_BAD_REQUEST)
						else:
							print("创建企业--{}".format(eps_info_result["result"]["enterpriseName"]))
							# 根据获取的工商数据创建企业信息
							BasicEnterpriseInfo.objects.create(name=eps_info_result["result"]["enterpriseName"],
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
							# 创建认证
							auth_id = self.perform_create(serializer)
							# 关联企业认证到当前用户
							UserInfo.objects.filter(id=user_id).update(eps_auth_manually_review=auth_id)
							# 更新企业认证的状态
							EnterpriseAuthManuallyReview.objects.filter(id=auth_id.id).update(apply_audit_status=2,
							                                                                  user_name=user_name,
							                                                                  user_phone=user_phone
							                                                                  )
							eps_cert = EnterpriseCertification.objects.get(user_id=user_id)
							headers = self.get_success_headers(serializer.data)
							return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
					else:
						return Response({"error_message": "您提交认证的企业名称有误，无法认证"}, status=status.HTTP_400_BAD_REQUEST)
				# <-- 2019.6.25 测试通过 -->
	
	# <-- 本地测试已经通过，待同前端联调 -->
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		if serializer.is_valid(raise_exception=True):
			print(serializer)
			
			user_id = EnterpriseAuthManuallyReview.objects.get(id=instance.id).user_id
			
			auth_data = self.perform_update(serializer)
			
			# 更新企业认证的状态，并更新3个子状态为False
			EnterpriseAuthManuallyReview.objects.filter(id=instance.id).update(apply_audit_status=3,
			                                                                   idcard_status=False,
			                                                                   license_status=False,
			                                                                   review_status=False,
			                                                                   auth_failure_reason="")
			
			# 获取企业验证提交的文件所在的服务器路径
			eps_idcard_path = auth_data.enterprise_oper_idcard.path
			eps_license_path = auth_data.enterprise_license.path
			eps_review_path = auth_data.enterprise_review.path
			print(eps_idcard_path)
			print(eps_license_path)
			print(eps_review_path)
			
			import os
			
			if eps_idcard_path != "" or eps_idcard_path is not None:
				# 获取文件名
				dirs_idcard_filename = os.path.basename(eps_idcard_path)
				# 获取目录结构
				dirs_idcard = os.path.dirname(eps_idcard_path)
				# 列出企业负责人身份证文件所在目录的目录结构
				for root, dirs, files in os.walk(dirs_idcard):
					print(root)
					print(dirs)
					print(files)
					# 遍历企业负责人身份证文件目录下的所有文件
					for xfile in files:
						# 判断是否是本次上传的文件，如果是：跳过，如果不是：删除
						if xfile == dirs_idcard_filename:
							print("{} 是本次上传，不做删除！".format(xfile))
							pass
						else:
							print("删除以前的文件：{}".format(xfile))
							# 删除不是本次上传的文件
							os.remove(os.path.join(os.path.dirname(eps_idcard_path), xfile))
			
			if eps_license_path != "" or eps_license_path is not None:
				# 获取文件名
				dirs_license_filename = os.path.basename(eps_license_path)
				# 获取目录结构
				dirs_license = os.path.dirname(eps_license_path)
				# 列出企业营业执照文件所在目录的目录结构
				for root, dirs, files in os.walk(dirs_license):
					print(root)
					print(dirs)
					print(files)
					# 遍历企业负责人身份证文件目录下的所有文件
					for xfile in files:
						# 判断是否是本次上传的文件，如果是：跳过，如果不是：删除
						if xfile == dirs_license_filename:
							print("{} 是本次上传，不做删除！".format(xfile))
							pass
						else:
							print("删除以前的文件：{}".format(xfile))
							# 删除不是本次上传的文件
							os.remove(os.path.join(os.path.dirname(eps_license_path), xfile))
			
			if eps_review_path != "" or eps_review_path is not None:
				# 获取文件名
				dirs_review_filename = os.path.basename(eps_review_path)
				# 获取目录结构
				dirs_review = os.path.dirname(eps_review_path)
				# 列出企业申请文件所在目录的目录结构
				for root, dirs, files in os.walk(dirs_review):
					print(root)
					print(dirs)
					print(files)
					# 遍历企业申请文件目录下的所有文件
					for xfile in files:
						# 判断是否是本次上传的文件，如果是：跳过，如果不是：删除
						if xfile == dirs_review_filename:
							print("{} 是本次上传，不做删除！".format(xfile))
							pass
						else:
							print("删除以前的文件：{}".format(xfile))
							# 删除不是本次上传的文件
							os.remove(os.path.join(os.path.dirname(eps_review_path), xfile))
		
		return Response(serializer.data)
	
	# <-- 本地测试已经通过，待同前端联调 -->
	
	def perform_update(self, serializer):
		return serializer.save()
	
	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)
	
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
                                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
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
	
	filter_backends = (DjangoFilterBackend,)
	filter_class = EnterpriseAuthListFilter
	
	# ordering_fields = ('add_time', )
	
	def get_queryset(self):
		
		return EnterpriseAuthManuallyReview.objects.all()
	
	# 进行审核操作
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
			
		apply_audit_status = serializer.validated_data['apply_audit_status']
		idcard_status = serializer.validated_data['idcard_status']
		license_status = serializer.validated_data['license_status']
		review_status = serializer.validated_data['review_status']
		
		eps_auth_data = self.perform_update(serializer)
		
		print(idcard_status, license_status, review_status)
		
		eps_auth_id = instance.id
		
		user_id = EnterpriseAuthManuallyReview.objects.get(id=eps_auth_id).user_id
		
		# 获取机构信息
		eps_code = EnterpriseAuthManuallyReview.objects.get(id=eps_auth_id).enterprise_code
		eps_name = EnterpriseAuthManuallyReview.objects.get(id=eps_auth_id).enterprise_name
		soc_mark = EnterpriseAuthManuallyReview.objects.get(id=eps_auth_id).soc_mark_flag
		
		basic_info = BasicEnterpriseInfo.objects.get(credit_no=eps_code)
		
		# 获取当前用户手机号，用于发送短信 -- 这里不要随意更改
		user_phone = list(UserInfo.objects.filter(id=user_id).values())[0]['user_phone']
		
		# 实例化发送短信函数，根据申请结果发送短信
		juhe = YunPianSmsSend(SMS_API_KEY)
		
		re_dict = {}
		
		if apply_audit_status == 1:
			# 判断是否点选了任何一个提交的文件，如果点击了，则无法审核通过
			if idcard_status or license_status or review_status:
				return Response({"error_message": "出错了，您选择了修改提交的文件，但仍然审核通过！"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				# 审核通过后的代码
				print("审核通过")
				auth_status = "审核通过"
				user_permission_name_id = UserPermissionsName.objects.get(permission_sn="QX004").id
				
				# 创建认证证书
				cert_no_create = EnterpriseAuthCertification(eps_code)
				# 获取编号,证书生效日期及失效日期
				cert_no = cert_no_create.create_cert_sn()
				cert_start = datetime.date.today().strftime('%Y-%m-%d')
				cert_end = (datetime.date.today() + datetime.timedelta(days=366)).strftime('%Y-%m-%d')
				print(cert_no, cert_start, cert_end)
				
				# 创建证书，在数据库内生成证书
				new_cert = EnterpriseCertification.objects.create(user_id=user_id,
				                                                  certificate_sn=cert_no,
				                                                  certificate_effective_date=cert_start,
				                                                  certificate_expiry_date=cert_end,
				                                                  enterprise_name=eps_name,
				                                                  soc_mark_flag=soc_mark)
				# 更新用户审核信息 -- 证书信息
				EnterpriseAuthManuallyReview.objects.filter(id=instance.id).update(certificate_sn=cert_no,
				                                                  certificate_effective_date=cert_start,
				                                                  certificate_expiry_date=cert_end)
				print(new_cert)
				print("企业认证证书创建完成！")
				
				# 判断是否是服务机构认证
				if soc_mark:
					# 是服务机构认证，关联用户所属企业，修改用户权限为“QX004”，并且关联用户证书及开启服务提供商
					UserInfo.objects.filter(id=user_id).update(user_to_company=basic_info.id,
					                                           user_permission_name=user_permission_name_id,
					                                           eps_auth_soc=new_cert.id,
					                                           service_provider=True)
				else:
					# 不是服务机构认证，关联用户所属企业，修改用户权限为“QX004”，并且关联用户证书，但不开启服务提供商
					UserInfo.objects.filter(id=user_id).update(user_to_company=basic_info.id,
					                                           user_permission_name=user_permission_name_id,
					                                           eps_auth_soc=new_cert.id)
				
				# 发送审核成功短信
				sms_success_send = juhe.send_success_sms(user_phone=user_phone)
				if sms_success_send["error_code"] != 0:
					sms_send_result = "审核短信发送失败！原因：{}".format(sms_success_send["result"]['resmsg'])
				else:
					sms_send_result = "审核短信发送成功！"
				
				# 拼接返回的json数据
				re_dict['message'] = "{} -- 人工审核流程完成".format(status.HTTP_201_CREATED)
				re_dict['eps_auth_id'] = eps_auth_id
				re_dict['user_id'] = eps_auth_data.user_id
				re_dict['sms_send_result'] = sms_send_result
				re_dict['auth_status'] = auth_status
				re_dict['enterprise_name'] = eps_name
				re_dict['cert_no'] = cert_no
				re_dict['cert_start'] = cert_start
				re_dict['cert_end'] = cert_end
				re_dict['auth_failure_reason'] = eps_auth_data.auth_failure_reason
		
		elif apply_audit_status == 4:
			print("审核被完全驳回")
			auth_status = "审核被完全驳回"
			# # 将审核置为无效
			# EnterpriseAuthManuallyReview.objects.filter(id=eps_auth_id).update(audit_valid_flag=False)
			
			# 发送审核失败短信
			sms_fail_send = juhe.send_fail_sms(user_phone=user_phone)
			if sms_fail_send["error_code"] != 0:
				sms_send_result = "审核短信发送失败！原因：{}".format(sms_fail_send["result"]['resmsg'])
			else:
				sms_send_result = "审核短信发送成功！"
			
			# 拼接返回的json数据
			re_dict['message'] = "人工审核流程完成"
			re_dict['eps_auth_id'] = eps_auth_id
			re_dict['user_id'] = eps_auth_data.user_id
			re_dict['sms_send_result'] = sms_send_result
			re_dict['auth_status'] = auth_status
			re_dict['auth_failure_reason'] = eps_auth_data.auth_failure_reason
		
		elif apply_audit_status == 5:
			print("审核被驳回,扫描资料有问题，需要修改")
			auth_status = "驳回--修改扫描资料"
			
			# 发送审核失败短信
			sms_fail_send = juhe.send_fail_sms(user_phone=user_phone)
			if sms_fail_send["error_code"] != 0:
				sms_send_result = "审核短信发送失败！原因：{}".format(sms_fail_send["result"]['resmsg'])
			else:
				sms_send_result = "审核短信发送成功！"
			
			# 拼接返回的json数据
			re_dict['message'] = "人工审核流程完成"
			re_dict['eps_auth_id'] = eps_auth_id
			re_dict['user_id'] = eps_auth_data.user_id
			re_dict['sms_send_result'] = sms_send_result
			re_dict['auth_status'] = auth_status
			re_dict['auth_failure_reason'] = eps_auth_data.auth_failure_reason
		else:
			return Response({"error_message": "发生错误，请传入 1，4，5 这三个值，其他值不接受！"}, status=status.HTTP_400_BAD_REQUEST)
		
		return Response({"result": re_dict})
	
	def perform_update(self, serializer):
		return serializer.save()
	
	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)


class EnterpriseAuthComRejectViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                     viewsets.GenericViewSet):
	"""
	完全驳回接口
	"""
	
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = EnterpriseAuthManuallyReviewSerializers
	
	def get_queryset(self):
		user = self.request.user
		# 返回当前用户申请状态为 4（完全驳回），并且审核有效标志为False的结果集
		return EnterpriseAuthManuallyReview.objects.filter(user_id=user.id,
		                                                   apply_audit_status=4,
		                                                   audit_valid_flag=True)
	
	# 进行客户重新认证更新
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		
		self.perform_update(serializer)
		
		# 更新审核信息有效状态为False
		EnterpriseAuthManuallyReview.objects.filter(id=instance.id).update(audit_valid_flag=False)
		
		return Response({"message": "用户认证已经重置！"})
	
	def perform_update(self, serializer):
		return serializer.save()
	
	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)


class EnterpriseInfoOperatorDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
    企业信息及负责人组合信息接口
    """
	
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = EnterpriseInfoOperatorDetailSerializers
	
	filter_backends = (DjangoFilterBackend,)
	filter_class = EnterpriseInfoOperatorDetailFilter
	
	def get_queryset(self):
		return UserInfo.objects.all()


class EnterpriseSelfDefaultServicesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
    普适服务查询
    """
	
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = EnterpriseSelfServicesSerializers
	filter_backends = (DjangoFilterBackend,)
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
	filter_backends = (DjangoFilterBackend,)
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
	
	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)


def update_stock_status():
	start_time = datetime.datetime.now()
	user = UserInfo.objects.filter(id=39)
	print(start_time, "  ", user, ", 开始执行 update_stock_status cron task...")
	
	
def check_or_update_cert():
	now_time = datetime.date.today()
