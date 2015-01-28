from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from articles.forms import ArticleForm
from .forms import LoginForm


@login_required
def articles_add(request):
    article_form = ArticleForm()
    return render(request, 'adminpanel/articles_add.html', {'article_form': article_form})


def admin_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.login(request)
            return HttpResponseRedirect('/adminpanel/articles/add')
        else:
            return render(request, 'adminpanel/login.html', {'login_form': login_form})
    elif request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'adminpanel/login.html', {'login_form': login_form})


@login_required
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/')