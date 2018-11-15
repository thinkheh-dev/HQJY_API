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
from DjangoUeditor import urls as DjangoUeditor_urls
# from django.contrib import admin

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
	path('ueditor/', include(DjangoUeditor_urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('doc/', include_docs_urls(title='红企家园后端API'))
]

from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
