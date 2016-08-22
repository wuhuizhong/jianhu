# coding=utf8
"""www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin

import views
import wx_views
from user import views as user_views
from logic import views as logic_views

urlpatterns = [

	url(r'^get_job$', logic_views.get_job, name='get_job'),  #职位详情
	url(r'^get_job_luyin$', logic_views.get_job_luyin, name='get_job_luyin'),  #带录音的职位详情

	url(r'^post_job$', logic_views.post_job, name='post_job'),  #提交表单，发布职位
	url(r'^fabu_job$', logic_views.fabu_job, name='fabu_job'),  #发布职位
	url(r'^recommand_job$', logic_views.recommand_job, name='recommand_job'),  #推荐职位

	url(r'^msg$', logic_views.msg, name='msg'),  #首页消息
	url(r'^chat$', logic_views.chat, name='chat'),  #聊天消息
	 ]
