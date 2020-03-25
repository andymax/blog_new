from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mdeditor.fields import MDTextField
from django.utils import timezone
from imagekit.processors import ResizeToFit
from imagekit.models import ProcessedImageField

from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural='分类'
    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural='标签'
    def __str__(self):
        return self.name

class Post(models.Model):

    # 标题
    title = models.CharField(max_length=40,blank=True,null=True,verbose_name='标题')

    # 正文
    body = MDTextField(verbose_name='正文')
    # 作者
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    # 创建时间
    create_time = models.DateTimeField(verbose_name='创建时间',default=timezone.now)

    # 最后发布时间
    modified = models.DateTimeField(verbose_name='最后修改时间',default=timezone.now)

    # 文章摘要
    excerpt = models.CharField(max_length=200,blank=True,verbose_name='文章摘要')

    # 浏览量
    views = models.PositiveIntegerField(default=0,editable=False)
    # 分类
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='分类')

    # 标签

    tags = models.ManyToManyField(Tags,blank=True,verbose_name='标签')

    # 标题图
    avatar = ProcessedImageField(upload_to='image/article/%Y%m%d',
                                           processors=[ResizeToFit(width=500)],
                                           format='JPEG',
                                           options={'quality': 100},
                                           blank=True,
                                           null=True,
                                           verbose_name='标题图'
                                           )

    class Meta:
        ordering=['-create_time',]
        verbose_name_plural = '文章'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:detail',kwargs={'pk':self.pk})

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])



