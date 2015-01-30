from django.shortcuts import render
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Tag
from .forms import ArticleForm


def home(request):
    three_newest_articles = Article.objects.all().order_by('-id')[:3]
    return render(request, 'blog/home.html', {'articles': three_newest_articles})


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
        return render(request, 'articles/articles.html', {'articles': articles_page, 'title': 'All articles'})
    elif request.method == 'POST':
        if request.user.is_authenticated():
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
            created_at = single_article.created_at
            return render(request, 'articles/article.html', {
                'title': title,
                'preface': preface,
                'content': content,
                'created_at': created_at
            })
        except ObjectDoesNotExist:
            return HttpResponseNotFound(_('Article not found'))
    else:
        return HttpResponseNotAllowed(['GET'])


def articles_dates(request):
    if request.method == 'GET':
        try:
            sorted_articles = Article.objects.all().order_by('created_at')
            first_date = sorted_articles[0].created_at
            last_date = sorted_articles[len(sorted_articles) - 1].created_at
            return render(request, 'articles/article.html', {
                'dates': dates,
            })
        except ObjectDoesNotExist:
            return HttpResponseNotFound(_('Zero articles yet'))
    else:
        return HttpResponseNotAllowed(['GET'])


def tags(request):
    try:
        all_tags = Tag.objects.all()
        return render(request, 'articles/tags.html', {
            'tags': all_tags,
        })
    except ObjectDoesNotExist:
        pass


def articles_tag_id(request, tag_id):
    if request.method == 'GET':
        articles_by_tag = Article.objects.filter(tags__in=[tag_id])
        paginator = Paginator(articles_by_tag, 20)
        page = request.GET.get('page')
        try:
            articles_page = paginator.page(page)
        except PageNotAnInteger:
            articles_page = paginator.page(1)
        except EmptyPage:
            articles_page = paginator.page(paginator.num_pages)
        except ObjectDoesNotExist:
            return HttpResponse('Tag not found', status=404)
        return render(request, 'articles/articles.html', {'articles': articles_page, 'title': 'Articles with tag'})
    else:
        return HttpResponseNotAllowed(['GET'])