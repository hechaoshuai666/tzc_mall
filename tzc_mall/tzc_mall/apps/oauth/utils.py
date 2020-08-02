# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang

from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData

from . import constants_oauth

def generate_signed_openid(openid):
    s = Serializer(settings.SECRET_KEY,constants_oauth.ACCESS_TOKEN_EXPIRES)
    context = {'openid':openid}
    signed_openid = s.dumps(context)

    return signed_openid.decode('utf8')


def check_signed_openid(context):
    s = Serializer(settings.SECRET_KEY, constants_oauth.ACCESS_TOKEN_EXPIRES)
    try:
        result = s.loads(context)
    except BadData:
        return None
    else:
        return result.get('openid')