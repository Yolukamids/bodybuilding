import random
import re
from datetime import timedelta

import jwt, os
from django.conf import settings
from django.db import DatabaseError
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from wechatpy.oauth import WeChatOAuth

from bodybuild.models import User, Action, Course, Food, Fdcategory
from bodybuild.serializers import ActionSerializer, CourseSerializer, FoodSerializer, FdcateSerializer
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


# @api_view(('POST', ))
# def register(request):
#     username, tel, hint = '', '', ''
#     if request.method == 'POST':
#         agreement = request.POST.get('agreement')
#         username = request.POST.get('username', '').strip()
#         password = request.POST.get('password', '')
#         tel = request.POST.get('tel', '').strip()
#         if agreement == 'on':
#             redis_cli = get_redis_connection()
#             code_from_user = request.POST.get('mobilecode', '0')
#             code_from_redis = redis_cli.get(f'vote2003:polls:mobile:valid:{tel}').decode()
#             if code_from_user == code_from_redis:
#                 if check_username(username) and check_password(password) and check_tel(tel):
#                     password = gen_sha256_digest(password)
#                     try:
#                         user = User(username=username, password=password, tel=tel)
#                         user.last_visit = timezone.now()
#                         user.save()
#                         # 验证码只能消费一次，注册成功用过的验证码立即失效
#                         redis_cli.delete(f'vote2003:polls:mobile:valid:{tel}')
#                         hint = '注册成功，请登录'
#                         return redirect(f'/login/?hint={hint}')
#                     except DatabaseError:
#                         hint = '注册失败，用户名或手机号已被使用'
#                 else:
#                     hint = '请输入有效的注册信息'
#             else:
#                 hint = '请输入正确的手机验证码'
#         else:
#             hint = '请勾选同意网站用户协议及隐私政策'
#     return render(request, 'body_register.html', {'hint': hint, 'username': username, 'tel': tel})


def logout(request):
    resp = redirect('/')
    resp.delete_cookie('username')
    return resp


class ActionPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 20


class ActionView(ListAPIView):
    serializer_class = ActionSerializer
    pagination_class = ActionPagination

    def get_queryset(self):
        try:
            queryset = Action.objects.all()
            return queryset
        except (ValueError, DatabaseError):
            return redirect('/static/lyear_pages_error.html')


@api_view(('GET', ))
def action_display(request):
    # id = 1
    id = int(request.GET['id'])
    queryset = Action.objects.only('act_vid_url').filter(act_id=id)
    serialize = ActionSerializer(queryset, many=True)
    # queryset = Action.objects.filter(ac)
    data = {'video': serialize.data}
    return JsonResponse(data)


def show_course(request):
    courses = Course.objects.all()
    serialize = CourseSerializer(courses, many=True)
    return JsonResponse({'courses': serialize.data})


@api_view(('GET', ))
def course_details(request):
    # id = 1
    id = int(request.GET['id'])
    queryset_day1 = Action.objects.filter(act_of_cour_id=id, act_of_day1=1).order_by('act_day1_order')
    serialize_day1 = ActionSerializer(queryset_day1, many=True)
    queryset_day2 = Action.objects.filter(act_of_cour_id=id, act_of_day2=1).order_by('act_day2_order')
    serialize_day2 = ActionSerializer(queryset_day2, many=True)
    queryset_day3 = Action.objects.filter(act_of_cour_id=id, act_of_day3=1).order_by('act_day3_order')
    serialize_day3 = ActionSerializer(queryset_day3, many=True)
    # queryset = Action.objects.filter(ac)
    data = {'day1': serialize_day1.data, 'day2': serialize_day2.data, 'day3': serialize_day3.data}
    return JsonResponse(data)


@api_view(('GET', ))
def food_category(request):
    queryset = Fdcategory.objects.all()
    serialize = FdcateSerializer(queryset, many=True)
    # queryset = Action.objects.filter(ac)
    data = {'fdcategory': serialize.data}
    return JsonResponse(data)


@api_view(('GET', ))
def food_details(request):
    # id = 1
    group_id = int(request.GET['group_id'])
    fdcate_name = Fdcategory.objects.only('fdcate_name').filter(fdcate_id=group_id)
    queryset = Food.objects.filter(group_id=group_id)
    serialize = FoodSerializer(queryset, many=True)
    fd_serialize = FdcateSerializer(fdcate_name, many=True)
    # queryset = Action.objects.filter(ac)
    data = {'food': serialize.data, 'fdcate_name': fd_serialize.data}
    return JsonResponse(data)


def insert_data(request):
    imgs = os.listdir(r'D:\biyesheji\project\body\static\courses\img')
    names = os.listdir(r'D:\biyesheji\project\body\static\courses\name')
    lvls = os.listdir(r'D:\biyesheji\project\body\static\courses\lvl')
    positions = os.listdir(r'D:\biyesheji\project\body\static\courses\position')
    types = os.listdir(r'D:\biyesheji\project\body\static\courses\type')

    rule = r'[0-9-]+(.*)'
    for img, position, lvl, atype, name in zip(imgs, positions, lvls, types, names):
        img_g = 'courses/img/' + img
        name_g = re.findall(rule, name)[0][:-4]
        atype_g = re.findall(rule, atype)[0][:-4]
        lvl_g = re.findall(rule, lvl)[0][:-4]
        position_g = re.findall(rule, position)[0][:-4]
        # video_g = '/static/video/' + video
        Course.objects.create(cour_name=name_g, cour_lvl=lvl_g, cour_type=atype_g, cour_position=position_g, cour_pic_url=img_g)
    return redirect('/')
