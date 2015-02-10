from django.contrib import admin
from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Article, Tag, Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'preface', 'content', 'category', 'tags', ]
        widgets = {
            'content': AdminPagedownWidget
        }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm


admin.site.register(Tag)
admin.site.register(Category)
