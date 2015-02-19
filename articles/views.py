from collections import OrderedDict
import markdown
from django.shortcuts import render
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Tag, Category, Owner, BlogName, Greeting
from .forms import ArticleForm


def home(request):
    three_newest_articles = Article.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    blog_name = BlogName.objects.first()
    owner = Owner.objects.first()
    greeting = Greeting.objects.first()
    return render(request, 'blog/home.html', {'articles': three_newest_articles, 'categories': categories,
                                              'blog_name': blog_name.name, 'owner': owner.name,
                                              'greeting': greeting})


def articles(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        blog_name = BlogName.objects.first()
        owner = Owner.objects.first()
        all_articles = Article.objects.all()
        paginator = Paginator(all_articles, 20)
        page = request.GET.get('page')
        try:
            articles_page = paginator.page(page)
        except PageNotAnInteger:
            articles_page = paginator.page(1)
        except EmptyPage:
            articles_page = paginator.page(paginator.num_pages)
        return render(request, 'articles/articles.html', {
            'articles': articles_page, 'title': 'All articles', 'categories': categories, 'blog_name': blog_name.name,
            'owner': owner.name,
        })
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
            categories = Category.objects.all()
            blog_name = BlogName.objects.first()
            owner = Owner.objects.first()
            single_article = Article.objects.get(id=article_id)
            tags = single_article.tags.all()
            title = single_article.title
            preface = single_article.preface
            content = markdown.markdown(single_article.content)
            created_at = single_article.created_at
            return render(request, 'articles/article.html', {
                'title': title,
                'preface': preface,
                'content': content,
                'created_at': created_at,
                'categories': categories,
                'tags': tags,
                'blog_name': blog_name.name,
                'owner': owner.name,
            })
        except ObjectDoesNotExist:
            return HttpResponseNotFound(_('Article not found'))
    else:
        return HttpResponseNotAllowed(['GET'])


def articles_archive(request):
    if request.method == 'GET':
        try:
            blog_name = BlogName.objects.first()
            owner = Owner.objects.first()
            categories = Category.objects.all()
            sorted_articles = Article.objects.all().order_by('created_at')
            if not sorted_articles:
                return render(request, 'articles/archive.html', {
                    'dates': [],
                    'categories': categories,
                    'title': 'Archive'
                })
            first_date = sorted_articles[0].created_at
            last_date = sorted_articles[len(sorted_articles) - 1].created_at
            dates = OrderedDict()
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
            for i in range(int(last_date.year) - int(first_date.year)+1):
                dates[first_date.year + i] = months
            return render(request, 'articles/archive.html', {
                'dates': dates,
                'categories': categories,
                'title': 'Archive',
                'blog_name': blog_name.name,
                'owner': owner.name,
            })
        except ObjectDoesNotExist:
            return HttpResponseNotFound(_('Zero articles yet'))
    else:
        return HttpResponseNotAllowed(['GET'])


def tags(request):
    try:
        categories = Category.objects.all()
        blog_name = BlogName.objects.first()
        owner = Owner.objects.first()
        all_tags = Tag.objects.all()
        return render(request, 'articles/tags.html', {
            'tags': all_tags,
            'categories': categories,
            'blog_name': blog_name.name,
            'owner': owner.name,
        })
    except ObjectDoesNotExist:
        pass


def articles_tag_id(request, tag_id):
    if request.method == 'GET':
        categories = Category.objects.all()
        blog_name = BlogName.objects.first()
        owner = Owner.objects.first()
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
        return render(request, 'articles/articles.html', {
            'articles': articles_page, 'title': 'Articles with tag',
            'categories': categories, 'blog_name': blog_name.name, 'owner': owner.name})
    else:
        return HttpResponseNotAllowed(['GET'])


def articles_category_id(request, category_id):
    if request.method == 'GET':
        categories = Category.objects.all()
        blog_name = BlogName.objects.first()
        owner = Owner.objects.first()
        category = Category.objects.get(id=category_id)
        articles_by_category = Article.objects.filter(category=category)
        paginator = Paginator(articles_by_category, 20)
        page = request.GET.get('page')
        try:
            articles_page = paginator.page(page)
        except PageNotAnInteger:
            articles_page = paginator.page(1)
        except EmptyPage:
            articles_page = paginator.page(paginator.num_pages)
        except ObjectDoesNotExist:
            return HttpResponse('Tag not found', status=404)
        return render(request, 'articles/articles.html', {
            'articles': articles_page, 'title': str(category),
            'categories': categories, 'blog_name': blog_name.name, 'owner': owner.name})
    else:
        return HttpResponseNotAllowed(['GET'])


def articles_year(request, year):
    if request.method == 'GET':
        categories = Category.objects.all()
        blog_name = BlogName.objects.first()
        owner = Owner.objects.first()
        articles_by_year = Article.objects.filter(created_at__year=year)
        paginator = Paginator(articles_by_year, 20)
        page = request.GET.get('page')
        try:
            articles_page = paginator.page(page)
        except PageNotAnInteger:
            articles_page = paginator.page(1)
        except EmptyPage:
            articles_page = paginator.page(paginator.num_pages)
        except ObjectDoesNotExist:
            return HttpResponse('Tag not found', status=404)
        return render(request, 'articles/articles.html', {
            'articles': articles_page, 'title': 'Articles from ' + str(year),
            'categories': categories, 'blog_name': blog_name.name, 'owner': owner.name})
    else:
        return HttpResponseNotAllowed(['GET'])


def articles_year_month(request, year, month):
    if request.method == 'GET':
        categories = Category.objects.all()
        blog_name = BlogName.objects.first()
        owner = Owner.objects.first()
        articles_by_month = Article.objects.filter(created_at__year=year, created_at__month=month)
        paginator = Paginator(articles_by_month, 20)
        page = request.GET.get('page')
        try:
            articles_page = paginator.page(page)
        except PageNotAnInteger:
            articles_page = paginator.page(1)
        except EmptyPage:
            articles_page = paginator.page(paginator.num_pages)
        except ObjectDoesNotExist:
            return HttpResponse('Articles not found', status=404)
        return render(request, 'articles/articles.html', {
            'articles': articles_page, 'title': 'Articles from ' + str(year) + '/' + str(month),
            'categories': categories, 'blog_name': blog_name.name, 'owner': owner.name})
    else:
        return HttpResponseNotAllowed(['GET'])