# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang


from collections import OrderedDict
from goods import models

def get_categories():
    categories = OrderedDict()

    # 提取37个频道
    channels = models.GoodsChannel.objects.order_by('group_id', 'sequence')

    for channel in channels:
        group_id = channel.group_id

        # 构造排序的结构
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        # 获取一级菜单
        cat1 = channel.category

        # 添加一级菜单
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })

        for cat2 in cat1.subs.all():
            cat2.sub_cats = []
            for cat3 in cat2.subs.all():
                cat2.sub_cats.append(cat3)

            categories[group_id]['sub_cats'].append(cat2)

    return categories