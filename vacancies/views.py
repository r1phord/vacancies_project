from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from django.views import View

from vacancies.models import Company, Vacancy, Specialty


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
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id)

        if len(vacancy) == 0:
            raise Http404('no such vacancy')

        vacancy.select_related('company', 'specialty')
        return render(request, 'vacancy.html', context={
            'vacancy': vacancy.first()
        })
