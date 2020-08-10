# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

def get_breadcrumb(category):
    breadcrumb = {}

    if category.parent is None:
        # 一级菜单
        breadcrumb['cat1'] = category
    elif category.subs.count() == 0:
        # 三级菜单
        cat2 = category.parent
        breadcrumb['cat1'] =cat2.parent
        breadcrumb['cat2'] =cat2
        breadcrumb['cat3'] =category

    else:
        # 二级菜单
        breadcrumb['cat1'] = category.parent
        breadcrumb['cat2'] = category

    return breadcrumb