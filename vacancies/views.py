from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from st_vacancies.settings import LOGIN_REDIRECT_URL
from vacancies.forms import ApplicationForm, RegisterForm, LoginForm, CompanyForm
from vacancies.models import Company, Vacancy, Specialty, Application


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена.')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера.')


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all().prefetch_related('vacancies')
        companies = Company.objects.all().prefetch_related('vacancies')
        return render(request, 'index.html', context={
            'specialties': specialties,
            'companies': companies
        })


class CompanyView(View):
    def get(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise Http404('company not found')

        vacancies = Vacancy.objects.filter(company=company).select_related('specialty')
        return render(request, 'company.html', context={
            'company': company,
            'vacancies': vacancies
        })


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all().select_related('company', 'specialty')
        return render(request, 'vacancies.html', context={
            'title': 'Все вакансии',
            'vacancies': vacancies
        })


class SpecialtyVacanciesView(View):
    def get(self, request, specialty_code):
        # spec = Specialty.objects.filter(code=specialty_code)
        # if len(spec) == 0:
        #     raise Http404('no such specialty')
        #
        # spec = spec.first()

        if len(spec := Specialty.objects.filter(code=specialty_code)) == 0:
            raise Http404('no such specialty')

        spec = spec.first()
        vacancies = Vacancy.objects.filter(specialty=spec).select_related('company')

        return render(request, 'vacancies.html', context={
            'title': spec.title,
            'spec': spec,
            'vacancies': vacancies
        })


class VacancyView(View):
    def get_vacancy(self, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id)
        if len(vacancy) == 0:
            raise Http404('no such vacancy')

        vacancy.select_related('company', 'specialty')
        return vacancy

    def get(self, request, vacancy_id):
        vacancy = self.get_vacancy(vacancy_id).first()
        application_form = ApplicationForm()
        return render(request, 'vacancy.html', context={
            'vacancy': vacancy,
            'form': application_form
        })

    def post(self, request, vacancy_id):
        vacancy = self.get_vacancy(vacancy_id).first()
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            data = application_form.cleaned_data
            Application.objects.create(written_username=data['written_username'],
                                       written_phone=data['written_phone'],
                                       written_cover_letter=data['written_cover_letter'],
                                       vacancy=vacancy,
                                       user=User.objects.get(id=1))  # Заглушка. Поменять!
            return HttpResponseRedirect(redirect_to='send')
        return render(request, 'vacancy.html', context={
            'vacancy': vacancy,
            'form': application_form
        })


class SendApplicationView(View):
    def get(self, request, vacancy_id):
        return render(request, 'sent.html', context={
            'vacancy_id': vacancy_id
        })


class MyCompanyView(View):
    def get(self, request):
        user = request.user
        company = Company.objects.filter(owner=user).first()
        success = True
        if company:
            return render(request, 'company-edit.html', context={
                'company': company,
                'success': success
            })
        else:
            return render(request, 'company-create.html', context={
                'success': success
            })

    def post(self, request):
        company_form = CompanyForm(request.POST)
        user = request.user
        company = Company.objects.filter(owner=user).first()
        success = False
        if company_form.is_valid():
            data = company_form.cleaned_data
            if company:
                for attr, value in data.items():
                    setattr(company, attr, value)
                company.save()
            else:
                Company.objects.create(owner=user, **data)
            success = True
        return render(request, 'company-edit.html', context={
            'form': company_form,
            'company': company,
            'success': success
        })


class MyCompanyVacanciesView(View):
    def get(self, request):
        user = request.user
        company = Company.objects.get(owner=user)
        vacancies = Vacancy.objects.filter(company=company)  # .prefetch_related('applications')
        return render(request, 'vacancy-list.html', context={
            'vacancies': vacancies
        })


class MyCompanyVacancyView(View):
    def get(self, request, vacancies_id):
        return render(request, 'vacancy-edit.html', context={
            'vacancies_id': vacancies_id
        })

    def post(self, request, vacancies_id):
        return render(request, 'vacancy-edit.html', context={
            'vacancies_id': vacancies_id
        })


class MyLoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('success')
                    return HttpResponseRedirect(LOGIN_REDIRECT_URL)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        return render(request, 'login.html', context={
            'form': login_form
        })


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            User.objects.create_user(username=data['username'],
                                     first_name=data['first_name'],
                                     last_name=data['last_name'],
                                     password=data['password'])
            return HttpResponseRedirect('/')
        return render(request, 'register.html', context={
            'form': register_form
        })
