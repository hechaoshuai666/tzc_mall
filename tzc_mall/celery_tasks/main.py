# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

import os

# celery启动文件
from celery import Celery

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tzc_mall.settings.dev'

# 创建celery实例
celery_app = Celery('tzc_mall')

# 加载celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

