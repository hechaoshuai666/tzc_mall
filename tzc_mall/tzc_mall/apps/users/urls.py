# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url

from . import views

urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 登录
    url(r'^login/$', views.LoginView.as_view()),
    # 退出登录
    url(r'^logout/$', views.LogoutView.as_view()),
    # 用户中心
    url(r'^user_profile/$', views.UserProfile.as_view()),
]
