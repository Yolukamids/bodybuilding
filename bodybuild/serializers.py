"""
-*- coding: utf-8 -*-
@Time : 2022/3/30 15:37
@Author : 风落心夜
@File : serializers
@Project : body
"""
from rest_framework.serializers import ModelSerializer

from bodybuild.models import Action


class ActionSerializer(ModelSerializer):

    class Meta:
        model = Action
        fields = '__all__'
