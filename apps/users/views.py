from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt

from .serializers import SmsSerializer, FindPasswordSmsSerializer, UserRegSerializer, UserInfoDetailSerializers, \
						 UserPhoneSerializers, UserFindPasswordSerizlizers
from HQJY_API.settings import API_KEY
from apiutils.yunpiansms import YunPianSms
from .models import VerifyCode

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
		
		if not serializer.validated_data["user_phone"]:
			return Response({
				"user_phone": mobile
			}, status=status.HTTP_400_BAD_REQUEST)
			
		if sms_status["code"] != 0:
			return Response({
				"mobile": sms_status["msg"]
			}, status=status.HTTP_400_BAD_REQUEST)
		else:
			code_record = VerifyCode(code=code, user_phone=mobile)
			code_record.save()
			return Response({
				"mobile": mobile
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
				"mobile": sms_status["msg"]
			}, status=status.HTTP_400_BAD_REQUEST)
		else:
			code_record = VerifyCode(code=code, user_phone=mobile)
			code_record.save()
			return Response({
				"user_id": user_id, "mobile": mobile
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
		serializer.is_valid(raise_exception=True)
		user = self.perform_create(serializer)
		
		re_dict = serializer.data
		payload = jwt_payload_handler(user)
		re_dict["token"] = jwt_encode_handler(payload)
		re_dict["name"] = user.user_name if user.user_name else user.username
		
		headers = self.get_success_headers(serializer.data)
		return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
	
	def get_object(self):
		return self.request.user
	
	def perform_create(self, serializer):
		return serializer.save()
	

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
	
	
	
class UserPasswordModifyViewSet(viewsets.ModelViewSet):
	"""
	用户通过手机号修改密码
	update:
		更新用户信息
	partial：
		部分更新用户信息
	"""
	serializer_class = UserFindPasswordSerizlizers
	queryset = User.objects.all()

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
	
	
