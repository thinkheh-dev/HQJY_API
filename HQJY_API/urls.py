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

from service_object.views import DefaultServicesListViewSet, FinancingServicesListViewSet, DefaultCategoryViewset, \
	FinancingCategoryViewset, HotSearchsViewset, DefaultServicesBannerViewset, FinancingServicesBannerViewset, \
	ServicesBrandViewset, EnterpriseDemandViewset, CorporateFinanceDemandViewset, DefaultCategoryNavViewset, \
	FinancingCategoryNavViewset

from users.views import SmsCodeViewset, UserViewset

from enterprise_info.views import EnterpriseListViewSet, EnterpriseTypeListViewset

#实例化Router对象，用于配置路由
router = DefaultRouter()

#配置路由
#下面这些router很重要，不要随便修改，不然你会后悔！！

#配置服务接口路由
router.register(r'default-services', DefaultServicesListViewSet, base_name='dslist')
router.register(r'financing-services', FinancingServicesListViewSet, base_name='fnlist')

#配置服务分类路由
router.register(r'default-categorys', DefaultCategoryViewset, base_name='dcategorys')
router.register(r'financing-categorys', FinancingCategoryViewset, base_name='fcategorys')

router.register(r'default-nav', DefaultCategoryNavViewset, base_name='dnavcategroys')
router.register(r'financing-nav', FinancingCategoryNavViewset, base_name='fnavcategorys')

#配置热搜词路由
router.register(r'hotsearchs', HotSearchsViewset, base_name='hotsearchs')

#配置轮播图路由
router.register(r'default-banner', DefaultServicesBannerViewset, base_name='dbanner')
router.register(r'financing-banner', FinancingServicesBannerViewset, base_name='fbanner')

#配置服务品牌路由
router.register(r'service-brand', ServicesBrandViewset, base_name='sbrand')

#配置企业需求路由
router.register(r'en-demand', EnterpriseDemandViewset, base_name='endemand')
router.register(r'fi-demand', CorporateFinanceDemandViewset, base_name='fidemand')

#配置用户相关路由
router.register(r'codes', SmsCodeViewset, base_name='codes')
router.register(r'users', UserViewset, base_name='users')

#配置企业信息理由
router.register(r'enterprise-info', EnterpriseListViewSet, base_name='enterpriselist')
router.register(r'enterprise-type', EnterpriseTypeListViewset, base_name='enterprisetype')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
	path('ueditor/', include(DjangoUeditor_urls)),
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	
	#drf自带的认证模式
	path('api-token-auth/', views.obtain_auth_token),
	
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
