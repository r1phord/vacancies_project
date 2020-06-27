from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from vacancies.models import Company, Vacancy


class MainView(View):
    def get(self, request):
        return render(request, 'index.html')


class CompanyView(View):
    def get(self, request, company_id):
        company = Company.objects.filter(id=company_id)
        if len(company) == 0:
            return HttpResponseNotFound('company not found')
        company = company[0]
        company_vacancies = Vacancy.objects.filter(company=company)
        return render(request, 'company.html', context={
            'company': company,
            'company_vacancies': company_vacancies
        })


class AllVacanciesView(View):
    def get(self, request):
        return render(request, 'vacancies.html')


class CategoryVacanciesView(View):
    def get(self, request, category):
        return render(request, 'vacancies.html')


class VacancyView(View):
    def get(self, request, vacancy_id):
        return render(request, 'vacancy.html')
