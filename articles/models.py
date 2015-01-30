from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name=_('title'))
    preface = models.TextField(max_length=10000, verbose_name=_('preface'))
    content = models.TextField(max_length=500000, verbose_name=_('content'))

    category = models.ForeignKey('Category', verbose_name=_('category'))

    tags = models.ManyToManyField('Tag', blank=True, null=True, verbose_name=_('tags'))

    created_at = models.DateField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return '%s' % self.title


class Tag(models.Model):
    name = models.CharField(max_length=1000, unique=True, verbose_name=_('name'))

    def __str__(self):
        return '%s' % self.name


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name=_('name'))

    def __str__(self):
        return '%s' % self.name
