from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    avatar = models.FileField(upload_to='avatar/', default='avatar/1.jpg')

    blog = models.OneToOneField(to='Blog', on_delete=models.CASCADE, null=True)

    def __str(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    content = models.TextField()
    create_time = models.DateField(auto_now_add=True)

    # 优化字段
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)

    tag = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'))
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    site_title = models.CharField(max_length=255)
    site_name = models.CharField(max_length=255)
    site_theme = models.CharField(max_length=255)

    def __str__(self):
        return self.site_name


class UpAndDown(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    create_time = models.DateField(auto_now=True)
    is_up = models.BooleanField()


class Comment(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateField(auto_now=True)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tag', on_delete=models.CASCADE)
