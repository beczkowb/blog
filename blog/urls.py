from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^articles/', include('articles.urls')),
    url(r'^markdown/', include('django_bootstrap_markdown.urls')),
    url(r'^$', 'articles.views.home', name='home'),
)
