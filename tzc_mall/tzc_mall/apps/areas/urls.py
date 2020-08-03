# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^areas/',views.AreasView.as_view()),
]
