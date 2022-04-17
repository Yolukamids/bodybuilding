import random
import re
from datetime import timedelta

import jwt, os
from django.conf import settings
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wechatpy.oauth import WeChatOAuth

from bodybuild.models import User, Action
from bodybuild.serializers import ActionSerializer
from bodybuild.utils import check_username, check_password, gen_sha256_digest


def show_index(request: HttpRequest):
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
    return Response({'code': 40001, 'hint': hint})


def logout(request):
    resp = redirect('/')
    resp.delete_cookie('username')
    return resp


def show_action(request):
    queryset = Action.objects.all()
    serializer = ActionSerializer(queryset, many=True)
    return JsonResponse({'actions': serializer.data})


@api_view(('GET', ))
def action_display(request):
    # id = 1
    id = int(request.GET['id'])
    queryset = Action.objects.only('act_vid_url').filter(act_id=id)
    serialize = ActionSerializer(queryset, many=True)
    # queryset = Action.objects.filter(ac)
    data = {'video': serialize.data}
    print(id)
    return JsonResponse(data)


def insert_data(request):
    names = os.listdir('D:/biyesheji/project/body/static/images/actions')
    pic_url = os.listdir('D:/biyesheji/project/body/static/images/actions')
    postions = os.listdir('D:/biyesheji/project/body/static/position')
    lvls = os.listdir('D:/biyesheji/project/body/static/lvl')
    types = os.listdir('D:/biyesheji/project/body/static/type')
    videos = os.listdir(r'D:\biyesheji\project\body\static\video')

    rule = r'[0-9-]+[0-9]+(.*)'
    for url, position, lvl, atype, name, video in zip(pic_url, postions, lvls, types, names, videos):
        url_g = 'images/actions/' + url
        name_g = re.findall(rule, name)[0][:-4]
        atype_g = re.findall(rule, atype)[0][:-4]
        lvl_g = re.findall(rule, lvl)[0][:-4]
        position_g = re.findall(rule, position)[0][:-4]
        video_g = '/static/video/' + video
        Action.objects.create(act_name=name_g, act_lvl=lvl_g, act_type=atype_g, act_position=position_g, act_pic_url=url_g, act_vid_url=video_g)
    return redirect('/')
