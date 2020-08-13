# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url

from . import views

urlpatterns = [
    # 结算订单
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view(),name='settlement'),
    # 提交订单
    url(r'^orders/commit/$', views.OrderCommitView.as_view(),name='commit'),

]
