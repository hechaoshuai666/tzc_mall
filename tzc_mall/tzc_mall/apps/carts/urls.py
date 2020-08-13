# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url

from . import views

urlpatterns = [
    # 购物车
    url(r'^carts/$', views.CartsView.as_view(), name='info'),
    # 全选购物车
    url(r'^carts/selection/',views.CartsSelectAllView.as_view()),
    # 购物车悬浮提示
    url(r'^carts/simple/',views.CartsSimpleView.as_view()),
]
