from django import forms

from vacancies.models import Application


class RegisterForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']
