# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url

from . import views

urlpatterns = [
    # 支付接口
    url(r'^payment/(?P<order_id>\d+)/$', views.PaymentView.as_view()),
    # 响应结果
    url(r'^payment/status/$', views.PaymentStatusView.as_view()),

]
