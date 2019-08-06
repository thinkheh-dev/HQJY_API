from django.shortcuts import render


from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from apiutils.permissions import IsOwnerOrReadOnly, IsServiceProvider

from .models import WebFooterLink, WebFooterInfo, WebName, WebLogo
from .serializers import WebFooterInfoSerializers, WebFooterLinkSerializers, WebLogoSerializers, WebNameSerializers


class WebLogoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	网站logo接口视图
	
	list:
		网站logo列表
	retrieve:
        网站logo详情
	"""
	queryset = WebLogo.objects.filter(img_enable=True)
	serializer_class = WebLogoSerializers
	

class WebNameViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	网站名称接口视图
	
	list:
		网站名称列表
	retrieve:
		网站名称详情
	"""
	queryset = WebName.objects.filter(name_display=True)
	serializer_class = WebNameSerializers
	
	
class WebFooterInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	网站页脚信息接口视图
	
	list:
		网站页脚信息列表
	retrieve:
		网站页脚信息详情
	"""
	queryset = WebFooterInfo.objects.all()
	serializer_class = WebFooterInfoSerializers
	
	
class WebFooterLinkViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	网站友情链接接口视图
	
	list:
		网站友情链接列表
	retrieve:
		网站友情链接详情
	"""
	queryset = WebFooterLink.objects.all()
	serializer_class = WebFooterLinkSerializers
