# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : He Qiang
import re
from django.contrib.auth.backends import ModelBackend
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings

from . import constants
from .models import User

def verify_account(account):
    try:
        if re.match(r'1[3-9]\d{9}',account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

def generate_sign(cache_key):
    max_age = 3600 * 24 * 14
    s = Serializer(settings.SECRET_KEY, max_age)
    sign = s.dumps({'sessionid': cache_key})
    return sign.decode('utf8')

def check_sign(sign):
    max_age = 3600 * 24 * 14
    s = Serializer(settings.SECRET_KEY, max_age)
    try:
        ctx = s.loads(sign)
    except BadData:
        return None
    else:
        sessionid = ctx.get('sessionid')
        return sessionid


def check_verify_email_token(token):
    s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        expected_data = s.loads(token)
    except BadData:
        return None
    else:
        user_id = expected_data.get('user_id')
        email = expected_data.get('email')
        try:
            user = User.objects.get(user_id=user_id,email=email)
        except User.DoesNotExist:
            return None
        else:
            return user

def generate_verify_email_url(user):
    s = Serializer(settings.SECRET_KEY,constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    context = {
        'user_id':user.pk,
        'email':user.email
    }
    token = s.dumps(context).decode('utf8')

    producted_url = f'{settings.EMAIL_VERIFY_URL}?token={token}'

    return producted_url


class CheckAccountModel(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = verify_account(username)

        if user and user.check_password(password):
            return user
        else:
            return None