from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request):
        return render(request, 'index.html')


class CompanyView(View):
    def get(self, request, company_id):
        return render(request, 'company.html')


class AllVacanciesView(View):
    def get(self, request):
        return render(request, 'vacancies.html')


class CategoryVacanciesView(View):
    def get(self, request, category):
        return render(request, 'vacancies.html')


class VacancyView(View):
    def get(self, request, vacancy_id):
        return render(request, 'vacancy.html')
