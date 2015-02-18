from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'articles.views.articles', name='articles'),
    url(r'^(?P<article_id>\d+)$', 'articles.views.articles_id', name='articles_id'),
    url(r'^archive$', 'articles.views.articles_archive', name='articles_archive'),
    url(r'^tags$', 'articles.views.tags', name='tags'),
    url(r'^tag/(?P<tag_id>\d+)$', 'articles.views.articles_tag_id', name='articles_tag_id'),
    url(r'^category/(?P<category_id>\d+)$', 'articles.views.articles_category_id', name='articles_category_id'),
    url(r'^archive/(?P<year>\d+)$', 'articles.views.articles_year', name='articles_year'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', 'articles.views.articles_year_month', name='articles_year_month'),
)
