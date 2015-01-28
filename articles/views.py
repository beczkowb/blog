from django.shortcuts import render
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article
from .forms import ArticleForm


def articles(request):
    if request.method == 'GET':
        all_articles = Article.objects.all()
        paginator = Paginator(all_articles, 20)
        page = request.GET.get('page')
        try:
            articles_page = paginator.page(page)
        except PageNotAnInteger:
            articles_page = paginator.page(1)
        except EmptyPage:
            articles_page = paginator.page(paginator.num_pages)
        return render(request, 'articles/articles.html', {'articles': articles_page})
    elif request.method == 'POST':
        if not request.user.is_authenticated():
            article_form = ArticleForm(request.POST)
            if article_form.is_valid():
                article_form.save()
                return HttpResponse(_('Article created'), status=201)
            else:
                pass  # !!!
        else:
            return HttpResponse(_("You are not logged in."), status=401)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def articles_id(request, article_id):
    if request.method == 'GET':
        try:
            single_article = Article.objects.get(id=article_id)
            title = single_article.title
            preface = single_article.preface
            content = single_article.content
            return render(request, 'articles/article.html', {'title': title, 'preface': preface, 'content': content})
        except ObjectDoesNotExist:
            return HttpResponseNotFound(_('Article not found'))
    else:
        return HttpResponseNotAllowed(['GET'])