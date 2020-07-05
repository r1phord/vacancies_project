from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from vacancies.forms import ApplicationForm
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
        create = False
        if create:
            return render(request, 'company-create.html')
        else:
            return render(request, 'company-edit.html')


class MyCompanyVacanciesView(View):
    def get(self, request):
        return render(request, 'vacancy-list.html')


class MyCompanyVacancyView(View):
    def get(self, request, vacancies_id):
        return render(request, 'vacancy-edit.html', context={
            'vacancies_id': vacancies_id
        })


class MyLoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = request.POST
        return HttpResponseRedirect('/')




class LogoutView(View):
    def get(self, request):
        return HttpResponse('LogoutView')
