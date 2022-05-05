"""
-*- coding: utf-8 -*-
@Time : 2022/3/30 15:37
@Author : 风落心夜
@File : serializers
@Project : body
"""
from rest_framework.serializers import ModelSerializer

from bodybuild.models import Action, Course, Food, Fdcategory


class ActionSerializer(ModelSerializer):

    class Meta:
        model = Action
        fields = '__all__'


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class FoodSerializer(ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'


class FdcateSerializer(ModelSerializer):

    class Meta:
        model = Fdcategory
        fields = '__all__'
