# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url

from . import views

urlpatterns = [
    # qq登录
    url(r'^qq/login/$', views.QQAuthURLView.as_view()),
    # qq登录后的回调地址
    url(r'^oauth_callback/$', views.QQAuthUserView.as_view()),
]
