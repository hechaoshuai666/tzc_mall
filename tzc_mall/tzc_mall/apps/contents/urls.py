# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url

from . import views

urlpatterns = [
    # 注册
    url(r'^$', views.IndexView.as_view(), name='index'),
]