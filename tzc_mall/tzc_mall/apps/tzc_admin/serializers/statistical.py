# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from rest_framework import serializers


class GoodsVisitCountSerializer(serializers.Serializer):
    category = serializers.StringRelatedField(read_only=True)
    count = serializers.IntegerField(read_only=True)


