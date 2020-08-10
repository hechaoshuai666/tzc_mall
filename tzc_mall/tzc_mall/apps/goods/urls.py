# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url

from . import views

urlpatterns = [
    # 商品首页
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/',views.ListView.as_view(),name='list'),
    # 热销排行
    url(r'^hot/(?P<category_id>\d+)/',views.HotView.as_view())

]