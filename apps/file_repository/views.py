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
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.throttling import SimpleRateThrottle

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt

from .serializers import AttachResourcesSerializers, AttachLibraryManagerSerializers
from .models import AttachResources, AttachLibraryManager



User = get_user_model()


class AttachLibraryManagerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	资源库序列化视图
	"""
	serializer_class = AttachLibraryManagerSerializers
	queryset = AttachLibraryManager.objects.all()
