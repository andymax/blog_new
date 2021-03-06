# Generated by Django 2.0.6 on 2020-03-22 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=40, null=True, verbose_name='标题')),
                ('body', mdeditor.fields.MDTextField(verbose_name='正文')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后修改时间')),
                ('excerpt', models.CharField(blank=True, max_length=200, verbose_name='文章摘要')),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
                ('avatar', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='image/article/%Y%m%d', verbose_name='标题图')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Category', verbose_name='分类')),
            ],
            options={
                'verbose_name_plural': '文章',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='article.Tags', verbose_name='标签'),
        ),
    ]
