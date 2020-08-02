import logging
import re

from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.contrib.auth import login

from django.views import View
from django import http
from django_redis import get_redis_connection

from tzc_mall.utils.response_code import RETCODE
from .utils import generate_signed_openid,check_signed_openid
from .models import OAuthQQUser
from users.models import User

logger = logging.getLogger('django')

class QQAuthUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 提取code请求参数
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('缺少code')

        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI)

        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)

            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')
        # 提取state参数


        # 判断openid是否存在数据库中
        try:
           qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在时,则将openid传入前端页面中
            signed_openid = generate_signed_openid(openid)
            return render(request,'oauth_callback.html',{'access_token_openid':signed_openid})
        else:
            # 存在时,则直接跳转到相关的页面,保存会话内容
            state = request.GET.get('state') or '/'
            login(request,qq_user.user)
            response = redirect(state)
            response.set_cookie('username',qq_user.user.username,3600*24*14)

            return response


    def post(self,request):
        # 接收参数
        mobile = request.POST.get('mobile')
        pwd = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token = request.POST.get('access_token')

        # 校验参数
        # 判断参数是否齐全
        if not all([mobile, pwd, sms_code_client]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断短信验证码是否一致
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '无效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '输入短信验证码有误'})
        # 判断openid是否有效：错误提示放在sms_code_errmsg位置
        openid = check_signed_openid(access_token)
        if not openid:
            return render(request, 'oauth_callback.html', {'openid_errmsg': '无效的openid'})



        # 判断手机号是否存在
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 手机号不存在,则新建一个用户
            user = User.objects.create_user(username=mobile,password=pwd,mobile=mobile)
        else:
            # 手机号存在,则校验密码是否正确
            if not user.check_password(pwd):
                return render(request,'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})
        # 将用户的信息和openid绑定

        try:
            OAuthQQUser.objects.create(openid=openid,user=user)
        except DatabaseError as e:
            logger.error(e)
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': 'QQ登录失败'})

        state = request.GET.get('state') or '/'
        response = redirect(state)

        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        return response

class QQAuthURLView(View):
    """提供QQ登录页面网址
    https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=xxx&redirect_uri=xxx&state=xxx
    """
    def get(self, request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next = request.GET.get('next')

        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        login_url = oauth.get_qq_url()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url':login_url})