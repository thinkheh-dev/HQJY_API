from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apiutils.permissions import IsOwnerOrReadOnly


from .serializers import UserFavSerializers, UserFavDetailSerializers, OrderInfoSerializers, \
	OrderServiceDetailSerializers, OrderCancelSerializers
from file_repository.serializers import AttachResourceListSerializers

from .models import UserFav, OrderInfo, OrderServiceDetail
from file_repository.models import AttachResources, AttachLibraryManager
from service_object.models import DefaultServices, FinancingServices, DefaultServicesPackage
from .filters import OrderInfoFilter



class UserFavViewSet(viewsets.ModelViewSet):
	"""
	用户收藏视图
	list:
		获取用户收藏详情
	create:
		创建用户收藏
	delete:
		删除用户收藏
	"""
	
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = UserFavSerializers
	
	def get_serializer_class(self):
		if self.action == "list":
			return UserFavDetailSerializers
		else:
			return UserFavSerializers
	
	def get_queryset(self):
		return UserFav.objects.filter(user_info=self.request.user)


class OrderViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
	"""
	用户订单管理视图
	list:
		获取订单
	create:
		生成订单
	delete:
		删除订单
	"""
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = OrderInfoSerializers
	
	filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
	filter_class = OrderInfoFilter
	
	def get_queryset(self):
		return OrderInfo.objects.filter(user_info=self.request.user)
	
	def get_serializer_class(self):
		if self.action == "retrieve":
			return OrderInfoDetailSerializers
		return OrderInfoSerializers
	
	def create(self, request, *args, **kwargs):
		
		#定义临时变量接收产品ID
		default_services_tmp =''
		financing_services_tmp = ''
		default_services_package_tmp = ''
		
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			
			#将接收到的产品ID，赋值给临时变量备用
			default_services_tmp = serializer.validated_data['default_services']
			financing_services_tmp = serializer.validated_data['financing_services']
			default_services_package_tmp = serializer.validated_data['default_services_package']
			
			#从验证数据中删除产品ID
			del serializer.validated_data['default_services']
			del serializer.validated_data['financing_services']
			del serializer.validated_data['default_services_package']
			

		order_info = self.perform_create(serializer)
		
		#print(order_info)
		
		order_service_detail = OrderServiceDetail()
		order_service_detail.order_info = order_info
		
		if DefaultServices.objects.get(pk=default_services_tmp):
			
			order_service_detail.default_services = DefaultServices.objects.get(pk=default_services_tmp)
			order_service_detail.financing_services = None
			order_service_detail.default_services_package = None
			
		elif FinancingServices.objects.get(pk=financing_services_tmp):
			
			order_service_detail.default_services = None
			order_service_detail.financing_services = FinancingServices.objects.get(pk=financing_services_tmp)
			order_service_detail.default_services_package = None
			
		elif DefaultServicesPackage.objects.get(pk=default_services_package_tmp) :
			
			order_service_detail.default_services = None
			order_service_detail.financing_services = None
			order_service_detail.default_services_package = DefaultServicesPackage.objects.get(
				pk=default_services_package_tmp)
		else:
			raise ValueError("出错啦！必须传任意一个服务的值")
		
		
		order_service_detail.save()
		
		re_dict = {}
		
		# 获取普适服务id
		re_dict['default_services'] = default_services_tmp
		
		# 获取金融服务id
		re_dict['financing_services'] = financing_services_tmp
		
		# 获取普适服务包id
		re_dict['default_services_package_tmp'] = default_services_package_tmp
		
		#获取订单号
		re_dict['order_sn'] = order_info.order_sn
		
		#获取订单金额
		re_dict['order_amount'] = order_info.order_amount
		
		
		headers = self.get_success_headers(serializer.data)
		return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
		
		
	def perform_create(self, serializer):
		return serializer.save()
	

class OrderDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	订单详情视图
	"""
	
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = OrderServiceDetailSerializers
	
	
	def get_queryset(self):
		return OrderServiceDetail.objects.all()
	

class OrderCancelViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
	"""
	取消订单视图
	"""
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = OrderCancelSerializers

	def get_queryset(self):
		return OrderInfo.objects.filter(cancel_order=False)


#此视图方法暂时不启用
class OrderImageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
	"""
	订单上传图片视图
	"""
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	serializer_class = AttachResourceListSerializers
	
	def get_queryset(self):
		return AttachResources.objects.filter(attach_author=self.request.user)
