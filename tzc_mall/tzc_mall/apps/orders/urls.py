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
    # 提交订单成功页面
    url(r'^orders/success/$', views.OrderSuccessView.as_view(),name='success'),
    # 查看我的订单
    url(r'^orders/info/(?P<page_num>\d+)/$', views.UserOrderInfoView.as_view(),name='info'),

]
