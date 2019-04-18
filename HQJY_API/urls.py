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
from django.urls import path, include, re_path
import xadmin

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from DjangoUeditor import urls as DjangoUeditor_urls

from service_object.views import DefaultServicesListViewSet, FinancingServicesListViewSet, DefaultCategoryViewset, \
	 FinancingCategoryViewset, HotSearchsViewset, DefaultServicesBannerViewset, FinancingServicesBannerViewset, \
	 ServicesBrandViewset, EnterpriseDemandViewset, CorporateFinanceDemandViewset, DefaultCategoryNavViewset, \
	 FinancingCategoryNavViewset
from users.views import SmsCodeViewset, FindPasswordSmsCodeViewset, UserViewset, UserPhoneViewSet, \
						UserPasswordModifyViewSet, UserProtocolViewSet, UserRealNameAuthViewSet, UserPasswordOwnerViewSet
from enterprise_info.views import EnterpriseListViewSet, EnterpriseTypeListViewset, \
	EnterpriseAuthFileDownloadViewSet, EnterpriseAuthManuallyReviewViewSet, EnterpriseAuthUpdateViewSet, \
	EnterpriseDetailUpdateViewSet

from user_operation.views import UserFavViewSet, OrderViewSet, OrderDetailViewSet, OrderCancelViewSet

from platform_operation.views import WeMediaArticlesCreateViewSet, WeMediaArticlesDetailViewSet, \
	WeMediaArticlesFavViewSet

from page_control.models import SystemAdminURL

#获取最新的后台管理指定的管理地址
admin_url = SystemAdminURL.objects.all().first() #无论后台地址有多少条，只取最后编辑保存的那一条（数据库记录）




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
router.register(r'userphone', UserPhoneViewSet, base_name='userphone')
router.register(r'codes', SmsCodeViewset, base_name='codes')
router.register(r'users', UserViewset, base_name='users')
router.register(r'user-protocol', UserProtocolViewSet, base_name='userprotocol')
router.register(r'user_real_name', UserRealNameAuthViewSet, base_name='userrealname')

#用户密码相关路由
router.register(r'change-password-code', FindPasswordSmsCodeViewset, base_name='changepasswordcode')
router.register(r'change-password', UserPasswordModifyViewSet, base_name='changepassword')
router.register(r'change-password-owner', UserPasswordOwnerViewSet, base_name="changepasswordowner")


#配置企业信息路由
router.register(r'enterprise-info', EnterpriseListViewSet, base_name='enterpriselist')
router.register(r'enterprise-type', EnterpriseTypeListViewset, base_name='enterprisetype')
router.register(r'enterprise_update', EnterpriseDetailUpdateViewSet, base_name='enterpriseupdate')

#配置企业认证相关路由
router.register(r'eps-auth-fdownload', EnterpriseAuthFileDownloadViewSet, base_name='epsafdown')
router.register(r'eps-auth-review', EnterpriseAuthManuallyReviewViewSet, base_name='epsar')
router.register(r'eps-auth-update', EnterpriseAuthUpdateViewSet, base_name='epsau')

#配置文件库路由
# router.register(r'file-repository', OrderImageViewSet, base_name='filereplist')

#配置用户收藏路由
router.register(r'user-fav', UserFavViewSet, base_name='user-fav')

#配置用户订单生成路由
router.register(r'order-send', OrderViewSet, base_name='ordersend')
router.register(r'order-detail', OrderDetailViewSet, base_name='orderdetail')
router.register(r'order-cancel', OrderCancelViewSet, base_name='ordercancel')

#配置平台自媒体文章相关路由
router.register(r'wemedia-detail', WeMediaArticlesDetailViewSet, base_name='wemediadetail')
router.register(r'wemedia-create', WeMediaArticlesCreateViewSet, base_name='wemediacreate')


urlpatterns = [
	#后台管理地址（初始）
	
	# path('xadmin/', xadmin.site.urls), #第一次配置，请启用这一条
	
    re_path(r'^%s/' % (admin_url), xadmin.site.urls), #在后台修改过系统管理地址后，则可以启用这条
	
	path('ueditor/', include(DjangoUeditor_urls)),
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	
	#drf自带的认证模式
	#path('api-token-auth/', views.obtain_auth_token),
	
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
