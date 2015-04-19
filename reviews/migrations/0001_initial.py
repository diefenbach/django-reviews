# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField(null=True, verbose_name='Content ID', blank=True)),
                ('session_id', models.CharField(max_length=50, verbose_name='Session ID', blank=True)),
                ('user_name', models.CharField(max_length=50, verbose_name='Name', blank=True)),
                ('user_email', models.EmailField(max_length=254, verbose_name='E-mail', blank=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True)),
                ('score', models.FloatField(default=3.0, verbose_name='Score', choices=[(1.0, '*'), (2.0, '**'), (3.0, '***'), (4.0, '****'), (5.0, '*****')])),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('ip_address', models.GenericIPAddressField(null=True, verbose_name='IP address', blank=True)),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_review', verbose_name='Content type', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='review_comments', verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-creation_date',),
            },
        ),
    ]
