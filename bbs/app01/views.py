from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
from app01 import forms, models
from io import BytesIO
from app01.comment import get_color
from random import randint, choice
from django.contrib import auth
from django.utils.safestring import mark_safe
from django.db.models import F
import json


# Create your views here.
def register(request):
    dic = {'code': '', 'msg': ''}
    form_obj = forms.Register()
    if request.method == 'POST':
        form_obj = forms.Register(request.POST)
        errors = form_obj.errors
        if errors:
            dic['code'] = 401
            dic['msg'] = errors
            return JsonResponse(dic)
        cleaned_data = form_obj.cleaned_data
        cleaned_data.pop('re_password')
        file = request.FILES.get('image')
        print(cleaned_data)
        if file:
            cleaned_data['avatar'] = file

        models.User.objects.create_user(**cleaned_data)
        dic['code'] = 200
        dic['msg'] = reverse('login')
        return JsonResponse(dic)
    return render(request, 'register.html', locals())


def login(request):
    dic = {'code': '', 'msg': ''}
    if request.method == 'POST':
        if request.session.get('code').lower() == request.POST.get('code').lower():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                auth.login(request, user_obj)
                dic['code'] = 200
                dic['msg'] = reverse('home')
            else:
                dic['code'] = 402
                dic['msg'] = '账号或者密码错误'
        else:
            dic['code'] = 403
            dic['msg'] = '验证码错误'
        return JsonResponse(dic)
    return render(request, 'login.html')


def home(request):
    article_list = models.Article.objects.all()
    return render(request, 'home.html', locals())


def get_image(request):
    image_obj = Image.new('RGB', (360, 36), get_color())
    image_draw = ImageDraw.Draw(image_obj)
    image_font = ImageFont.truetype('static/font/222.ttf', size=36)
    io_obj = BytesIO()

    code = ''
    for i in range(0, 5):
        upper = chr(randint(65, 90))
        lower = chr(randint(97, 122))
        int_obj = str(randint(0, 9))
        choose = choice([upper, lower, int_obj])
        code += choose
        image_draw.text((50 + i * 50, -5), choose, get_color(), image_font)

    print(code)
    request.session['code'] = code

    image_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


def site(request, username, **kwargs):
    article_list = models.Article.objects.filter(blog__site_name=username)
    # tag_list = models.Tag.objects.filter(blog__site_name=username).\
    #     annotate(c=Count('article')).values('name', 'c', 'id')
    # category_list = models.Category.objects.filter(blog__site_name=username).\
    #     annotate(c=Count('article')).values('name', 'c', 'id')
    # archive_list = article_list.annotate(c_time=TruncMonth('create_time')).values('c_time').\
    #     annotate(c=Count('c_time')).values('c_time', 'c')
    if kwargs:
        if kwargs.get('method') == 'tag':
            article_list = article_list.filter(tag=kwargs.get('id'))
        elif kwargs.get('method') == 'category':
            article_list = article_list.filter(category=kwargs.get('id'))
        else:
            date = kwargs.get('id')
            year, month = date.split("-")
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    return render(request, 'site.html', locals())


def article_detail(request, username, article_id):
    article = models.Article.objects.filter(id=article_id, blog__site_name=username).first()
    comment_list = models.Comment.objects.filter(article=article)
    return render(request, 'article_detail.html', locals())


def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


def check_password(request):
    pass


def up_down(request):
    if request.is_ajax():
        dic = {'code': 100, 'msg': ''}
        flag = request.POST.get('flag')
        article_id = request.POST.get('article_id')
        article = models.Article.objects.filter(pk=article_id).first()
        if request.user.is_authenticated:
            if models.User.objects.filter(blog__article=article).first() == request.user:
                dic['code'] = 102
                dic['msg'] = '凑不要脸的，不能点评自己的文章'
            else:
                up_down_obj = models.UpAndDown.objects.filter(article_id=article_id).first()
                if up_down_obj:
                    user_id = up_down_obj.user_id
                    if user_id == request.user.id:
                        dic['code'] = 103
                        dic['msg'] = '亲，只能点一次哦'
                    else:
                        flag = json.loads(flag)
                        models.UpAndDown.objects.create(user=request.user, article_id=article_id, is_up=flag)
                        if flag:
                            dic['msg'] = '感谢亲的支持，点赞成功'
                            models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                        else:
                            dic['msg'] = '亲，欢迎一起讨论哟'
                            models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                else:
                    flag = json.loads(flag)
                    models.UpAndDown.objects.create(user=request.user, article_id=article_id, is_up=flag)
                    if flag:
                        dic['msg'] = '感谢亲的支持，点赞成功'
                        models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                    else:
                        dic['msg'] = '亲，欢迎一起讨论哟'
                        models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
        else:
            dic['code'] = 101
            dic['msg'] = mark_safe('请先<a href="%s">登陆<a/>' % reverse('login'))
        return JsonResponse(dic)


def comment(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            parent_id = request.POST.get('parent_id', None)
            content = request.POST.get('content')
            user_id = request.user.id
            article_id = request.POST.get('article_id')
            models.Comment.objects.create(content=content, user_id=user_id, article_id=article_id, parent_id=parent_id)
            models.Article.objects.filter(id=article_id).update(comment_num=F('comment_num') + 1)
        return JsonResponse({123:1232})
