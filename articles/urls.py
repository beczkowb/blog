from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'articles.views.articles', name='articles'),
    url(r'^(?P<article_id>\d+)$', 'articles.views.articles_id', name='articles_id'),
)