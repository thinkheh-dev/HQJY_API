from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status, mixins, exceptions, parsers, renderers
from rest_framework.response import Response
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.throttling import SimpleRateThrottle

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt

from .serializers import SmsSerializer, FindPasswordSmsSerializer, UserRegSerializer, UserInfoDetailSerializers, \
						 UserPhoneSerializers, UserFindPasswordSerizlizers, UserProtocolSerializers, \
						 UserRealNameAuthSerializers, UserChangPasswordSerizlizers
from HQJY_API.settings import API_KEY
from apiutils.yunpiansms import YunPianSms
from apiutils.realnameauth import RealNameAuthInterface
from .models import VerifyCode, UserProtocol, UserPermissionsName

User = get_user_model()

class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
	"""
    发送短信验证码
    """
	serializer_class = SmsSerializer
	
	def generate_code(self):
		"""
        生成六数字的验证码
        :return:
        """
		seeds = "1234567890"
		random_str = []
		for i in range(6):
			random_str.append(choice(seeds))
		
		return "".join(random_str)
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		mobile = serializer.validated_data["user_phone"]
		
		yun_pian = YunPianSms(API_KEY)
		
		code = self.generate_code()
		
		sms_status = yun_pian.send_sms(code=code, user_phone=mobile)
		

		if sms_status["code"] != 0:
			return Response({
				"user_phone": sms_status["msg"]
			}, status=status.HTTP_400_BAD_REQUEST)
		else:
			code_record = VerifyCode(code=code, user_phone=mobile)
			code_record.save()
			return Response({
				"user_phone": mobile
			}, status=status.HTTP_201_CREATED)


class FindPasswordSmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
	"""
    找回密码-发送短信验证码
    """
	serializer_class = FindPasswordSmsSerializer
	
	def generate_code(self):
		"""
        生成六数字的验证码
        :return:
        """
		seeds = "1234567890"
		random_str = []
		for i in range(6):
			random_str.append(choice(seeds))
		
		return "".join(random_str)
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		mobile = serializer.validated_data["user_phone"]
		user_id = list(User.objects.filter(user_phone=mobile).values('id'))[0]['id']
		
		yun_pian = YunPianSms(API_KEY)
		
		code = self.generate_code()
		
		sms_status = yun_pian.send_sms(code=code, user_phone=mobile)
		
		if sms_status["code"] != 0:
			return Response({
				"user_phone": sms_status["msg"]
			}, status=status.HTTP_400_BAD_REQUEST)
		else:
			code_record = VerifyCode(code=code, user_phone=mobile)
			code_record.save()
			return Response({
				"user_id": user_id, "user_phone": mobile
			}, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	create:
		用户注册
	list:
		用户列表
	retrieve:
		用户详情
	update:
		用户信息更新
	partial：
		部分更新用户信息
    """
	serializer_class = UserRegSerializer
	queryset = User.objects.all()
	
	authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

	def get_serializer_class(self):
		if self.action == "retrieve":
			return UserInfoDetailSerializers
		elif self.action == "create":
			return UserRegSerializer

		return UserInfoDetailSerializers

	def get_permissions(self):
		if self.action == "retrieve":
			return [permissions.IsAuthenticated()]
		elif self.action == "create":
			return []
		return []

	def create(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
		
			serializer.validated_data['user_permission_name'] = UserPermissionsName.objects.filter(
				permission_sn="QX001").first()
			
			#print(serializer.validated_data['user_labels'])
		
		user = self.perform_create(serializer)
		
		re_dict = serializer.data
		payload = jwt_payload_handler(user)
		#获取token
		re_dict["token"] = jwt_encode_handler(payload)
		#获取用户id
		re_dict['user_id'] = user.id
		#获取用户权限
		re_dict['user_permission_name'] = user.user_permission_name.permission_sn
		#获取用户头像
		re_dict['user_logo'] = user.user_logo.url
		#获取用户归属地
		re_dict['user_home'] = user.user_home
		#获取管理员模式
		re_dict['is_staff'] = user.is_staff
		
		
		headers = self.get_success_headers(serializer.data)
		return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
	
	def get_object(self):
		return self.request.user
	
	def perform_create(self, serializer):
		return serializer.save()
	
	def update(self, request, *args, **kwargs):
		print("开始更新")
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		pupdate_data = self.perform_update(serializer)
		
		#获取用户头像文件所在的服务器路径
		user_logo_path = pupdate_data.user_logo.path
		print(user_logo_path)
		
		
		import os
		# 获取头像文件的文件名
		dirs_logo_filename = os.path.basename(user_logo_path)
		# 获取头像文件所在的绝对路径
		dirs_logo = os.path.dirname(user_logo_path)
		print(dirs_logo_filename)
		
		#列出头像文件所在目录的目录结构
		for root, dirs, files in os.walk(dirs_logo):
			print(root)
			print(dirs)
			print(files)
			#遍历头像目录下的所有文件
			for xfile in files:
				#判断是否是本次上传的头像文件，如果是：跳过，如果不是：删除
				if xfile == dirs_logo_filename:
					print("{} 是本次上传，不做删除！".format(xfile))
					pass
				else:
					print("删除以前的文件：{}".format(xfile))
					os.remove(os.path.join(os.path.dirname(user_logo_path), xfile))
		
		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}
		
		return Response(serializer.data)
	
	def perform_update(self, serializer):
		return serializer.save()
	
	
	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)
	

class UserPhoneViewSet(CreateModelMixin, viewsets.GenericViewSet):
	"""
	用户手机号注册验证
	"""
	serializer_class = UserPhoneSerializers
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		user_phone = serializer.validated_data["user_phone"]
		return Response({"user_phone":user_phone})


class UserChangePasswordThrottle(SimpleRateThrottle):
	"""
	限制用户登录60s尝试次数-阀值类
	"""
	scope = 'user_change_password_scope'  # 显示频率的Key,在配置文件里需要有个跟这个同名
	
	def get_cache_key(self, request, view):
		return self.get_ident(request)  # 获取请求IP
	
	
class UserPasswordModifyViewSet(mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
	"""
	用户通过手机号修改密码
	update:
		更新用户信息
	partial：
		部分更新用户信息
	"""
	serializer_class = UserFindPasswordSerizlizers
	queryset = User.objects.all()
	
	throttle_classes = [UserChangePasswordThrottle, ]
	

	@action(detail=True, methods=['post'])
	def set_password(self, request, pk=None):
		user = self.get_object()
		serializer = UserFindPasswordSerizlizers(data=request.data)
		print(serializer)
		if serializer.is_valid():
			user.set_password(serializer.data['password'])
			user.save()
			return Response({"user_phone": user.user_phone, "user_id": pk},
			                status=status.HTTP_202_ACCEPTED)
		else:
			return Response(serializer.errors,
			                status=status.HTTP_400_BAD_REQUEST)
	
	def throttled(self, request, wait):
		"""
		访问次数被限制时，定制错误信息
		"""
		
		class Throttled(exceptions.Throttled):
			default_detail = '系统检测到您的操作太过于频繁，'
			extra_detail_singular = '请在 {wait} 秒之后再操作.'
			extra_detail_plural = '请在 {wait} 秒之后再操作.'
		
		raise Throttled(wait)


class UserPasswordOwnerViewSet(mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
	"""
	登录用户修改密码
	update:
		更新用户信息
	partial：
		部分更新用户信息
	"""
	serializer_class = UserChangPasswordSerizlizers
	queryset = User.objects.all()
	
	@action(detail=True, methods=['post'])
	def set_password(self, request, pk=None):
		user = self.get_object()
		serializer = UserChangPasswordSerizlizers(data=request.data)
		print(serializer)
		if serializer.is_valid():
			user.set_password(serializer.data['password'])
			user.save()
			return Response({"user_id": pk}, status=status.HTTP_202_ACCEPTED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

class UserProtocolViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	用户协议视图
	list:
		协议列表
	retrieve:
		协议详情
	"""
	
	serializer_class = UserProtocolSerializers
	queryset = UserProtocol.objects.all()


class UserRealNameAuthThrottle(SimpleRateThrottle):
	"""
	限制用户实名认证每天的尝试次数-阀值类
	"""
	scope = 'user_realname_auth_scope'  # 显示频率的Key,在配置文件里需要有个跟这个同名
	
	def get_cache_key(self, request, view):
		return self.get_ident(request)  # 获取请求IP
	

class UserRealNameAuthViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
	"""
	用户实名认证视图
	"""
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = UserRealNameAuthSerializers
	
	throttle_classes = [UserRealNameAuthThrottle, ]
	
	def get_user_birth(self, idcard):
		
		useridcard = idcard
		
		user_year = useridcard[6:10]
		user_month = useridcard[10:12]
		user_day = useridcard[12:14]
		
		user_birth = "{}-{}-{}".format(user_year, user_month, user_day)
		
		return user_birth
		
		
	def get_queryset(self):
		return User.objects.all()
	
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', True)
		user = self.get_object()
		serializer = self.get_serializer(user, data=request.data, partial=partial)
		if serializer.is_valid(raise_exception=True):
			user_name = serializer.validated_data['user_name']
			user_id_card = serializer.validated_data['user_id_card']
			user_phone = serializer.validated_data['user_phone']
			
			real_name_auth = RealNameAuthInterface(API_KEY)
			auth_status = real_name_auth.send_auth(user_phone=user_phone, realname=user_name, idcard=user_id_card)
			
			if auth_status['error_code'] != 0:
				return Response({
					"error_message": auth_status["result"]['resmsg']
				}, status=status.HTTP_400_BAD_REQUEST)
			else:
				user.user_name = user_name
				user.user_id_card = user_id_card
				user.user_permission_name = UserPermissionsName.objects.filter(permission_sn="QX002").first()
				
				#判断身份证性别
				if int(list(user_id_card)[-2]) % 2 :
					user.user_sex = "male"
				else:
					user.user_sex = "female"
				
				#调用获取身份证生日的函数
				user.user_birthday = self.get_user_birth(idcard=user_id_card)
				user.save()
				
				return Response({
					"success":"验证完成",
					"auth_status": auth_status['result']['resmsg']
				})
		
	def throttled(self, request, wait):
		"""
		访问次数被限制时，定制错误信息
		"""
		class Throttled(exceptions.Throttled):
			default_detail = '实名认证每天只能提交1次，'
			extra_detail_singular = '请在 {wait} 秒之后再操作.'
			extra_detail_plural = '请在 {wait} 秒之后再操作.'
		
		raise Throttled(wait)
	
