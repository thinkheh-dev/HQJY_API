"""HQJY_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
import xadmin

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from DjangoUeditor import urls as DjangoUeditor_urls

from service_object.views import DefaultServicesListViewSet, FinancingServicesListViewSet
from users.views import SmsCodeViewset, UserViewset

#实例化Router对象，用于配置路由
router = DefaultRouter()

#配置路由
router.register(r'default-services', DefaultServicesListViewSet, base_name='dslist')
router.register(r'financing-services', FinancingServicesListViewSet, base_name='fnlist')
router.register(r'codes', SmsCodeViewset, base_name='codes')
router.register(r'users', UserViewset, base_name='users')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
	path('ueditor/', include(DjangoUeditor_urls)),
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	
	#drf自带的认证模式
	# path('api-token-auth/', views.obtain_auth_token),
	
	#jwt认证模式
	path('login/', obtain_jwt_token),
	
    path('docs/', include_docs_urls(title='红企家园后端API')),

	
	#path('default-services/', DefaultServicesListView.as_view(), name='ds-list')
]

from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
