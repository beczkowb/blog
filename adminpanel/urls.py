from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^articles/add$', 'adminpanel.views.articles_add', name='articles_add'),
    url(r'^login$', 'adminpanel.views.admin_login', name='admin_login'),
)
