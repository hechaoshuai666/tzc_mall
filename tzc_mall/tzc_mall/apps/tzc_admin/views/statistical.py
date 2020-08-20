# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang
from datetime import date, timedelta

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from goods.models import GoodsVisitCount
from ..serializers.statistical import GoodsVisitCountSerializer

class UserTotalCountView(APIView):
    '''
    用户总数统计
    '''

    # 仅后台用户访问
    permission_classes = (IsAdminUser,)

    def get(self, request):
        # 获取当天日期
        now_date = date.today()

        count = User.objects.count()

        return Response({
            'count': count,
            'data': now_date
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


class DayUserActiveCountView(APIView):
    '''
    当日登录用户数量统计
    '''

    # 仅后台用户访问
    permission_classes = (IsAdminUser,)

    def get(self, request):
        # 获取当天日期
        now_date = date.today()

        count = User.objects.filter(last_login__gte=now_date).count()

        return Response({
            'count': count,
            'data': now_date
        })


class DayUserOrderCountView(APIView):
    '''
    当日下单用户数量统计
    '''

    # 仅后台用户访问
    permission_classes = (IsAdminUser,)

    def get(self, request):
        # 获取当天日期
        now_date = date.today()

        count = User.objects.filter(orderinfo__create_time__gte=now_date).distinct().count()

        return Response({
            'count': count,
            'data': now_date
        })


class DayMonthIncrementCountView(APIView):
    '''
    月增用户数量统计
    '''

    # 仅后台用户访问
    permission_classes = (IsAdminUser,)

    def get(self, request):
        # 获取当天日期
        now_date = date.today()

        last_date = now_date - timedelta(days=29)

        data_list = []

        for i in range(30):
            begin_date = last_date + timedelta(days=i)
            end_date = last_date + timedelta(days=i + 1)

            count = User.objects.filter(date_joined__gte=begin_date, date_joined__lt=end_date).count()
            data_list.append({
                'count': count,
                'date': begin_date
            })

        return Response(data_list)

class DayGoodsCountView(APIView):
    '''
    商品日访问量统计
    '''

    # 仅后台用户访问
    permission_classes = (IsAdminUser,)

    def get(self,request):

        now_date = date.today()

        goods_queryset = GoodsVisitCount.objects.filter(date__gte=now_date)

        ser = GoodsVisitCountSerializer(goods_queryset,many=True)

        return Response(ser.data)
