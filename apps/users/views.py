from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import SmsSerializer, UserRegSerializer, UserInfoDetailSerializers
from HQJY_API.settings import API_KEY
from apiutils.yunpiansms import YunPianSms
from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
	"""
    自定义用户验证
    """
	
	def authenticate(self, request, username=None, password=None, **kwargs):
		
		print('in pass')
		
		# def get_ip(request):
		# 	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		# 	if x_forwarded_for:
		# 		ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
		# 		print("realip:", ip)
		# 	else:
		# 		ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
		# 		print("proxyip:", ip)
		# 	return ip
		
		try:
			user = User.objects.get(Q(username=username) | Q(user_phone=username))
			print(user)
			print(password)
			print(user.check_password(password))
			if user.check_password(password):
				
				# #获取用户的浏览器及IP地址
				# agent = request.META.get('HTTP_USER_AGENT')
				#
				# user_ip_now = get_ip(request)
				#
				# #保存用户ip地址及浏览器
				# user.user_ip = user_ip_now
				# user.user_browser = agent
				# user.save()
				
				print("password pass", user.user_ip)
				return user
			else:
				print("password not pass")
				return None
		except Exception as e:
			return None


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
				"mobile": sms_status["msg"]
			}, status=status.HTTP_400_BAD_REQUEST)
		else:
			code_record = VerifyCode(code=code, user_phone=user_phone)
			code_record.save()
			return Response({
				"mobile": mobile
			}, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	create:
		用户注册
	list:
		用户列表
	retrieve:
		用户详情
	update:
		用户信息更新
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

	# permission_classes = (permissions.IsAuthenticated, )
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
		print(self.request.user)
		return self.request.user
	
	def perform_create(self, serializer):
		return serializer.save()
