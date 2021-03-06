"""body URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bodybuild import views
from bodybuild.views import show_index, login, logout, insert_data, action_display, ActionView, show_course, \
    course_details, food_details, food_category # register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_index),
    path('login/', login),
    path('logout/', logout),
    # path('register/', register),
    path('insert/', insert_data),
    path('actions/', ActionView.as_view()),
    path('video/', action_display, name='action'),
    path('courses/', show_course),
    path('details/', course_details, name='course'),
    path('fdcategory/', food_category),
    path('food/', food_details, name='food')
]
