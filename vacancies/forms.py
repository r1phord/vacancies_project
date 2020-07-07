from django import forms

from vacancies.models import Application, Company, Vacancy


class RegisterForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']
