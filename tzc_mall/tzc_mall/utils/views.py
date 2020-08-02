# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

from tzc_mall.utils.response_code import RETCODE


class LoginRequiredJSONMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
