from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(min_length=1, max_length=16, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def is_valid(self):
        valid = super(LoginForm, self).is_valid()
        if not valid:
            return valid
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            self.user = user
            return True
        else:
            self._errors['invalid_login_or_password'] = _('Invalid login details supplied')
            return False

    def login(self, request):
        login(request, self.user)