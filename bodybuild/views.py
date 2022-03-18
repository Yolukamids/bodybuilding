import random
from datetime import timedelta

import jwt
from django.conf import settings
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response


from bodybuild.models import User
from bodybuild.utils import check_username, check_password, gen_sha256_digest


def show_index(request: HttpRequest):
    html_code = '<h1>hello world!</h1>'
    fruits = [1, 2, 3, 4, 5, 6, 7]
    select_fruits = random.sample(fruits, 4)
    return redirect('/static/index.html')


@api_view(('POST', ))
def login(request):
    hint = request.GET.get('hint') or ''
    if request.method == 'POST':
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        if check_username(username) and check_password(password):
            password = gen_sha256_digest(password)
            user = User.objects.filter(Q(username=username) | Q(usertel=username)) \
                .filter(userpass=password).first()
            if user:
                user.last_visit = timezone.now()
                user.save()
                payload = {
                    'userid': user.user_id,
                    'exp': timezone.now() + timedelta(days=1)
                }
                # 通过PyJWT的encode函数生成用户身份令牌（bytes，可以通过decode方法处理成str）
                token = jwt.encode(payload, settings.SECRET_KEY)
                return Response({'code': 40000, 'hint': '登录成功', 'token': token, 'username': user.username, 'nickname': user.nickname, 'avatar': user.avatar})
            else:
                hint = '登录失败，用户名或密码错误'
        else:
            hint = '请输入有效的登录信息'
    print(2)
    return Response({'code': 40001, 'hint': hint})


def logout(request):
    request.session.flush()
    resp = redirect('/static/lyear_pages_login_3.html')
    resp.delete_cookie('username')
    return resp
