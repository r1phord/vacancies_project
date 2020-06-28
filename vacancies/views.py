from django.http import HttpResponseNotFound, HttpResponseServerError
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
        if not Company.objects.filter(id=company_id).exists():
            return HttpResponseNotFound('company not found')

        company = Company.objects.filter(id=company_id).prefetch_related('vacancies')

        return render(request, 'company.html', context={
            'company': company[0]
        })


class AllVacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all().select_related('company', 'specialty')
        return render(request, 'vacancies.html', context={
            'title': 'Все вакансии',
            'vacancies': vacancies
        })


class SpecialtyVacanciesView(View):
    def get(self, request, specialty_code):
        if not Specialty.objects.filter(code=specialty_code).exists():
            return HttpResponseNotFound('no such specialty')

        spec = Specialty.objects.filter(code=specialty_code)[0]
        vacancies = Vacancy.objects.filter(specialty=spec).select_related('company')

        return render(request, 'vacancies.html', context={
            'title': spec.title,
            'vacancies': vacancies
        })


class VacancyView(View):
    def get(self, request, vacancy_id):
        if not Vacancy.objects.filter(id=vacancy_id).exists():
            return HttpResponseNotFound('vacancy not found')

        vacancy = Vacancy.objects.filter(id=vacancy_id).select_related('company', 'specialty')

        return render(request, 'vacancy.html', context={
            'vacancy': vacancy[0]
        })
