# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang
from datetime import date


from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


class UserTotalCountView(APIView):
    '''
    用户总数统计
    '''

    # 仅后台用户访问
    permission_classes = (IsAdminUser,)

    def get(self,request):
        # 获取当天日期
        now_date = date.today()

        count = User.objects.count()

        return Response({
            'count':count,
            'data':now_date
        })


class DayUserIncrementCountView(APIView):
    '''
    用户日增统计
    '''

    # 仅后台用户访问
    permission_classes = (IsAdminUser,)

    def get(self, request):
        # 获取当天日期
        now_date = date.today()

        count = User.objects.filter(date_joined__gte=now_date).count()

        return Response({
            'count': count,
            'data': now_date
        })