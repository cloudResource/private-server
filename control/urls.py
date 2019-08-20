"""yysb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/video_address$', views.video_address),  # 视频播放
    url(r'^v1/cover_image$', views.cover_image),  # 封面地址
    url(r'^v1/video_start$', views.video_start),  # 开始录制视频
    url(r'^v1/video_stop$', views.video_stop),  # 停止录制视频
    url(r'^v1/intercept_image$', views.intercept_image),  # 截取保存视频图片
]
