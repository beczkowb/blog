from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name=_('title'))
    preface = models.CharField(max_length=10000, verbose_name=_('preface'))
    content = models.TextField(max_length=500000, verbose_name=_('content'))
