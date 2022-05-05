# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Action(models.Model):
    act_id = models.AutoField(primary_key=True)
    act_name = models.CharField(max_length=20)
    act_lvl = models.CharField(max_length=20)
    act_type = models.CharField(max_length=50)
    act_position = models.CharField(max_length=50)
    act_pic_url = models.CharField(max_length=1024)
    act_vid_url = models.CharField(max_length=1024)
    act_of_cour_id = models.IntegerField()
    act_of_day1 = models.IntegerField(blank=True, null=True)
    act_of_day2 = models.IntegerField(blank=True, null=True)
    act_of_day3 = models.IntegerField(blank=True, null=True)
    act_day1_order = models.IntegerField(blank=True, null=True)
    act_day2_order = models.IntegerField(blank=True, null=True)
    act_day3_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_action'


class Course(models.Model):
    cour_id = models.AutoField(primary_key=True)
    cour_name = models.CharField(max_length=20)
    cour_lvl = models.CharField(max_length=20)
    cour_type = models.CharField(max_length=50)
    cour_position = models.CharField(max_length=50)
    cour_pic_url = models.CharField(max_length=1024)
    cour_details_url = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'tb_course'


class Fdcategory(models.Model):
    fdcate_id = models.AutoField(primary_key=True)
    fdcate_name = models.CharField(max_length=100)
    fdcate_pic_url = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'tb_fdcategory'


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=100)
    food_energy = models.CharField(max_length=50)
    food_pic_url = models.CharField(max_length=1024)
    group_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'tb_food'


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    userpass = models.CharField(max_length=64)
    nickname = models.CharField(max_length=20)
    avatar = models.CharField(max_length=1024)
    usertel = models.CharField(unique=True, max_length=20)
    reg_date = models.DateTimeField()
    last_visit = models.DateTimeField()

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
