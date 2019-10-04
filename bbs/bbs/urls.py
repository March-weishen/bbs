"""bbs URL Configuration

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
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    path('home/', views.home, name='home'),
    path('get_image/', views.get_image, name='get_image'),
    path('up_down/', views.up_down, name='up_down'),
    path('comment/', views.comment, name='comment'),

    path('<str:username>/', views.site, name='site'),
    path('<str:username>/article_detail/<str:article_id>/', views.article_detail, name='article_detail'),
    path('<str:username>/<str:method>/<str:id>/', views.site, name='site'),

]
